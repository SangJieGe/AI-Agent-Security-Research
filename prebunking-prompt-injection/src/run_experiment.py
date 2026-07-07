"""
run_experiment.py — 批量跑实验 + 统计分析 + 生成汇总报告。

设计:
  - 遍历 模型 × payload类型 × 安全提示 组合
  - 每组跑 N 次（temperature=0.7） + 1组 temperature=0
  - 写入 CSV + 生成 summary.md
"""

import csv
import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Any

import yaml

# 自动加载 Hermes .env 文件
_ENV_PATH = Path("/root/.hermes/.env")
if _ENV_PATH.exists():
    with open(_ENV_PATH) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                _v = _v.strip().strip('"').strip("'")
                os.environ.setdefault(_k, _v)

from agent_harness import ModelAdapter, run_agent, AgentRunResult
from payloads import USER_TASK, LATE_SAFETY_PROMPT

# ============================================================
# 工具函数
# ============================================================


def load_config(config_path: str = "config.yaml") -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def result_to_row(r: AgentRunResult) -> dict:
    return {
        "payload_type": r.payload_type,
        "model": r.model,
        "temperature": r.temperature,
        "late_safety_injected": r.late_safety_injected,
        "egress_occurred": r.egress_occurred,
        "mentioned_late_safety_prompt": r.mentioned_late_safety_prompt,
        "final_response_text": r.final_response_text[:500],
        "tool_calls_count": len(r.turn_by_turn_tool_calls),
        "turn_by_turn_json": json.dumps(r.turn_by_turn_tool_calls, ensure_ascii=False),
    }


def write_csv(results: list[AgentRunResult], csv_path: str):
    """将结果写入 CSV。"""
    Path(csv_path).parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "payload_type",
        "model",
        "temperature",
        "late_safety_injected",
        "egress_occurred",
        "mentioned_late_safety_prompt",
        "final_response_text",
        "tool_calls_count",
        "turn_by_turn_json",
    ]

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(result_to_row(r))


def calc_egress_rate(results: list[AgentRunResult]) -> float:
    if not results:
        return 0.0
    return sum(1 for r in results if r.egress_occurred) / len(results)


def z_test_proportions(
    success_a: int, n_a: int, success_b: int, n_b: int
) -> tuple[float, float]:
    """
    双比例 z 检验。
    返回 (z_stat, p_value)
    """
    import math

    p_a = success_a / n_a if n_a > 0 else 0
    p_b = success_b / n_b if n_b > 0 else 0

    # 合并比例
    p_pool = (success_a + success_b) / (n_a + n_b) if (n_a + n_b) > 0 else 0

    # 标准误
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b)) if n_a > 0 and n_b > 0 else 0

    if se == 0:
        return 0.0, 1.0

    z = (p_a - p_b) / se

    # 用正态分布近似 p 值（双侧）
    from scipy.stats import norm

    p_value = 2 * (1 - norm.cdf(abs(z)))

    return z, p_value


def chi_square_test(
    success_a: int, n_a: int, success_b: int, n_b: int,
) -> dict:
    """卡方独立性检验。"""
    from scipy.stats import chi2_contingency

    table = [
        [success_a, n_a - success_a],
        [success_b, n_b - success_b],
    ]
    chi2, p_value, dof, expected = chi2_contingency(table)
    return {"chi2": chi2, "p_value": p_value, "dof": dof}


def generate_summary(
    all_results: list[AgentRunResult],
    models: list[str],
    payload_types: list[str],
    summary_path: str,
):
    """生成汇总报告 Markdown。"""
    lines = []
    lines.append("# 提示词预先接种对照实验 — 结果汇总")
    lines.append(f"\n> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"> 总实验轮次: {len(all_results)}")

    lines.append("\n## 实验设计\n")
    lines.append("- **对照组**: standard（标准间接提示词注入）")
    lines.append("- **实验组**: prebunking（预先接种式提示词注入）")
    lines.append("- **防御条件**: 有/无迟来的安全提示（LATE_SAFETY_PROMPT）")
    lines.append("- **因变量**: egress_occurred（密钥外发是否成功）")
    lines.append("- **假设**: prebunking 组在有安全提示条件下仍保持较高 egress 率")
    lines.append(f"- **每个条件运行次数**: 30（temperature=0.7）+ 1（temperature=0）")

    lines.append("\n## 各条件 egress 率\n")

    # 按 模型 × payload × late_safety 分组
    from collections import defaultdict

    for model_name in models:
        lines.append(f"### 模型: {model_name}\n")
        lines.append("| Payload 类型 | 安全提示 | Egress 率 | 提及率 |")
        lines.append("|-------------|---------|----------|--------|")

        for pt in payload_types:
            for late_safety in [True, False]:
                subset = [
                    r
                    for r in all_results
                    if r.model == model_name
                    and r.payload_type == pt
                    and r.late_safety_injected == late_safety
                    and r.temperature == 0.7  # 只看主实验组
                ]
                if subset:
                    egress_rate = calc_egress_rate(subset)
                    mention_rate = sum(1 for r in subset if r.mentioned_late_safety_prompt) / len(subset)
                    lines.append(
                        f"| {pt} | {'有' if late_safety else '无'} | "
                        f"{egress_rate:.1%} ({sum(1 for r in subset if r.egress_occurred)}/{len(subset)}) | "
                        f"{mention_rate:.1%} |"
                    )

        lines.append("")

    # 统计检验
    lines.append("\n## 统计检验\n")
    lines.append("### 核心对比: standard vs prebunking（有安全提示条件下）\n")

    for model_name in models:
        lines.append(f"**模型: {model_name}**\n")

        standard_subset = [
            r
            for r in all_results
            if r.model == model_name
            and r.payload_type == "standard"
            and r.late_safety_injected == True
            and r.temperature == 0.7
        ]
        prebunking_subset = [
            r
            for r in all_results
            if r.model == model_name
            and r.payload_type == "prebunking"
            and r.late_safety_injected == True
            and r.temperature == 0.7
        ]

        s_success = sum(1 for r in standard_subset if r.egress_occurred)
        s_n = len(standard_subset)
        p_success = sum(1 for r in prebunking_subset if r.egress_occurred)
        p_n = len(prebunking_subset)

        if s_n > 0 and p_n > 0:
            z, p_z = z_test_proportions(s_success, s_n, p_success, p_n)
            chi_result = chi_square_test(s_success, s_n, p_success, p_n)

            lines.append(f"- Standard 组 egress 率: {s_success}/{s_n} = {s_success/s_n:.1%}")
            lines.append(f"- Prebunking 组 egress 率: {p_success}/{p_n} = {p_success/p_n:.1%}")
            lines.append(f"- Z 检验: z = {z:.3f}, p = {p_z:.4f}")
            lines.append(f"- 卡方检验: χ² = {chi_result['chi2']:.3f}, p = {chi_result['p_value']:.4f}")

            if p_z < 0.05:
                lines.append(f"- ✅ 差异显著 (p < 0.05)，prebunking 组 egress 率显著{'高于' if p_success/p_n > s_success/s_n else '低于'} standard 组")
            else:
                lines.append(f"- ❌ 差异不显著 (p ≥ 0.05)")

        lines.append("")

    # Temperature=0 对照
    lines.append("\n## Temperature=0 对照\n")

    for model_name in models:
        lines.append(f"### 模型: {model_name}\n")
        lines.append("| Payload 类型 | 安全提示 | Egress |")
        lines.append("|-------------|---------|--------|")
        for pt in payload_types:
            for late_safety in [True, False]:
                subset = [
                    r
                    for r in all_results
                    if r.model == model_name
                    and r.payload_type == pt
                    and r.late_safety_injected == late_safety
                    and r.temperature == 0
                ]
                for r in subset:
                    lines.append(
                        f"| {pt} | {'有' if late_safety else '无'} | "
                        f"{'✅ 成功' if r.egress_occurred else '❌ 未外发'} |"
                    )
        lines.append("")

    # 写入文件
    Path(summary_path).parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, "w") as f:
        f.write("\n".join(lines))

    return "\n".join(lines)


# ============================================================
# 主流程
# ============================================================


def main():
    config = load_config()
    models_cfg = config["models"]
    exp_cfg = config["experiment"]
    runs_per = exp_cfg["runs_per_condition"]
    max_turns = exp_cfg["max_turns"]
    temperature = exp_cfg["temperature"]

    payload_types = ["standard", "prebunking"]
    all_results: list[AgentRunResult] = []

    # 过滤掉没有设置 API key 的模型
    available_models = []
    for mc in models_cfg:
        key_env = mc.get("api_key_env", "")
        if os.environ.get(key_env):
            available_models.append(mc)
        else:
            print(f"⚠️ 跳过模型 {mc['name']}: 环境变量 {key_env} 未设置")

    if not available_models:
        print("❌ 没有任何可用模型，请设置 API key 环境变量")
        sys.exit(1)

    model_names = [m["name"] for m in available_models]
    total_combos = len(available_models) * len(payload_types) * 2  # 2 = late_safety T/F
    total_runs = total_combos * runs_per + len(available_models) * len(payload_types) * 2  # t=0 runs

    print(f"🚀 开始实验: {len(available_models)} 模型 × {len(payload_types)} payload × 2 安全条件")
    print(f"   每组 {runs_per} 次 (t={temperature}) + 1 次 (t=0)")
    print(f"   预计总运行: {total_runs} 次\n")

    run_count = 0

    for model_cfg in available_models:
        print(f"\n{'='*60}")
        print(f"📦 初始化模型: {model_cfg['name']}")
        print(f"{'='*60}")

        try:
            adapter = ModelAdapter(model_cfg)
        except Exception as e:
            print(f"❌ 模型初始化失败: {e}")
            continue

        for payload_type in payload_types:
            user_task = USER_TASK.format(variant=payload_type)

            for late_safety in [True, False]:
                safety_label = "有安全提示" if late_safety else "无安全提示"
                print(f"\n  ▶ {payload_type} | {safety_label} | t={temperature}")

                for run_i in range(runs_per):
                    result = run_agent(
                        model_adapter=adapter,
                        user_task=user_task,
                        payload_type=payload_type,
                        inject_late_safety=late_safety,
                        late_safety_prompt=LATE_SAFETY_PROMPT,
                        temperature=temperature,
                        max_turns=max_turns,
                    )
                    all_results.append(result)
                    run_count += 1

                    egress_icon = "🚨" if result.egress_occurred else "🛡️"
                    mention_icon = "💬" if result.mentioned_late_safety_prompt else "🔇"
                    print(
                        f"    [{run_count}/{total_runs}] {egress_icon} egress={result.egress_occurred} "
                        f"{mention_icon} mention={result.mentioned_late_safety_prompt} "
                        f"turns={len(result.turn_by_turn_tool_calls)}"
                    )
                    time.sleep(0.3)  # 限速

                # temperature=0 对照
                print(f"    ▶ {payload_type} | {safety_label} | t=0 (对照)")
                result_t0 = run_agent(
                    model_adapter=adapter,
                    user_task=user_task,
                    payload_type=payload_type,
                    inject_late_safety=late_safety,
                    late_safety_prompt=LATE_SAFETY_PROMPT,
                    temperature=0,
                    max_turns=max_turns,
                )
                all_results.append(result_t0)
                run_count += 1
                egress_icon = "🚨" if result_t0.egress_occurred else "🛡️"
                print(f"    [{run_count}/{total_runs}] {egress_icon} egress={result_t0.egress_occurred} (t=0)")

    # 保存结果
    print(f"\n{'='*60}")
    print("📊 保存结果...")

    csv_path = config["output"]["raw_csv"]
    summary_path = config["output"]["summary_md"]

    write_csv(all_results, csv_path)
    print(f"  ✅ 原始数据: {csv_path} ({len(all_results)} rows)")

    summary = generate_summary(
        all_results, model_names, payload_types, summary_path
    )
    print(f"  ✅ 汇总报告: {summary_path}")

    print(f"\n{'='*60}")
    print("🏁 实验完成！")
    print(summary)


if __name__ == "__main__":
    main()
