"""
test_single.py — 单次测试脚本，支持命令行参数。

用法：
    # 从 prebunking-prompt-injection/ 根目录运行:
    python src/test_single.py --payload standard --safety
    python src/test_single.py --payload prebunking --safety
    python src/test_single.py --payload standard --no-safety
    python src/test_single.py --payload narrative_only --safety -n 3

可用 payload 类型：
    standard, standard_padded, narrative_only, weak_override,
    weak_override_plus_narrative, generic_override, prebunking
"""
import argparse
import json
import os
import sys
import yaml
from pathlib import Path

# 确保能从 prebunking-prompt-injection/ 根目录 import src/ 下的模块
_THIS_DIR = Path(__file__).resolve().parent  # src/
_PROJ_DIR = _THIS_DIR.parent                  # prebunking-prompt-injection/
sys.path.insert(0, str(_THIS_DIR))

from agent_harness import ModelAdapter, run_agent
from payloads import USER_TASK, LATE_SAFETY_PROMPT

VALID_PAYLOADS = [
    "standard", "standard_padded", "narrative_only",
    "weak_override", "weak_override_plus_narrative",
    "generic_override", "prebunking",
]


def load_config():
    config_path = _THIS_DIR / "config.yaml"
    if not config_path.exists():
        config_path = _THIS_DIR / "config.example.yaml"
    if not config_path.exists():
        print(f"❌ 找不到配置文件: {_THIS_DIR}/config.yaml")
        print("   请复制 config.example.yaml → config.yaml 并填入 API 密钥")
        sys.exit(1)
    with open(config_path) as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(
        description="单次提示词注入对照实验测试"
    )
    parser.add_argument(
        "--payload", type=str, required=True,
        choices=VALID_PAYLOADS,
        help="注入 payload 类型"
    )
    parser.add_argument(
        "--safety", dest="safety", action="store_true", default=True,
        help="注入迟来安全提示（默认开启）"
    )
    parser.add_argument(
        "--no-safety", dest="safety", action="store_false",
        help="不注入迟来安全提示"
    )
    parser.add_argument(
        "-n", "--n-runs", type=int, default=1,
        help="重复运行次数（默认 1）"
    )
    parser.add_argument(
        "--temperature", type=float, default=0.7,
        help="采样温度（默认 0.7，设为 0 表示确定性输出）"
    )
    parser.add_argument(
        "--model-index", type=int, default=0,
        help="使用 config 中第几个模型（默认 0，即第一个）"
    )
    args = parser.parse_args()

    config = load_config()
    models = config.get("models", [])
    if not models:
        print("❌ config.yaml 中没有配置模型")
        sys.exit(1)
    if args.model_index >= len(models):
        print(f"❌ 模型索引 {args.model_index} 超出范围（共 {len(models)} 个模型）")
        sys.exit(1)

    model_cfg = models[args.model_index]
    print(f"🔧 模型: {model_cfg['name']} ({model_cfg.get('model_id', 'N/A')})")
    print(f"🎯 Payload: {args.payload}")
    print(f"🛡️  安全提示: {'是' if args.safety else '否'}")
    print(f"🌡️  温度: {args.temperature}")
    print(f"🔁 运行次数: {args.n_runs}")
    print()

    adapter = ModelAdapter(model_cfg)

    for run_i in range(args.n_runs):
        if args.n_runs > 1:
            print(f"--- 第 {run_i + 1}/{args.n_runs} 次 ---")

        user_task = USER_TASK.format(variant=args.payload)
        result = run_agent(
            model_adapter=adapter,
            user_task=user_task,
            payload_type=args.payload,
            inject_late_safety=args.safety,
            late_safety_prompt=LATE_SAFETY_PROMPT if args.safety else "",
            temperature=args.temperature,
            max_turns=config.get("experiment", {}).get("max_turns", 5),
        )

        print(f"  egress_occurred:           {result.egress_occurred}")
        print(f"  mentioned_late_safety:     {result.mentioned_late_safety_prompt}")
        print(f"  tool_calls:                {len(result.turn_by_turn_tool_calls)}")
        print(f"  final_response (前200字):  {result.final_response_text[:200].replace(chr(10), ' ')}")
        print()


if __name__ == "__main__":
    main()
