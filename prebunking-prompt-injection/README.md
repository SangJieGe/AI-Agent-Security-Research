# Preemptive Prompt Injection: Does "Prebunking" Amplify Indirect Prompt Injection Success?

> An Empirical Study — **Work in Progress**

**TL;DR:** We borrow the "prebunking" concept from disinformation psychology and test whether telling an LLM *in advance* that "future safety warnings are forged by an attacker" increases the success rate of indirect prompt injection attacks against runtime safety defenses.

---

## Core Findings (Preliminary, DeepSeek-V3 only)

1. **Attribution narratives have a significant standalone effect** (OR = 13.5, p < 0.0001). Merely labeling the injected content as originating from a trusted source boosts egress rates from 10% → 60%.
2. **Strong override instructions already hit ceiling** (96.7% egress rate). The "prebunking" framing adds little marginal effect in this regime.
3. **Attribution narrative × weak override interaction is ambiguous across statistical scales:**
   - Firth's penalized logistic regression: interaction p = 0.067 (marginal, CI crosses zero on log-odds scale)
   - Bootstrap interaction difference (probability scale): 28.3pp synergy, 95% CI [8.3pp, 51.7pp], p = 0.013
   - Fisher OR ratio: 5.0×, p < 0.0001
   - **Interpretation:** The interaction is real on the probability scale, but quasi-separation inflates standard errors on the log-odds scale. Larger samples and cross-model validation are needed.
4. **Single-model limitation:** All experiments run on DeepSeek-V3 only. Cross-model generalizability has not been tested — this is the primary limitation of the current work.

---

## Status

⚠️ **This is preliminary work in progress.** The current repository contains initial experimental results, not final conclusions. Discussion and replication are welcome.

---

## Quick Start

### Requirements

- Python 3.10+
- FastAPI + uvicorn
- openai Python SDK (for DeepSeek/Qwen/GPT via OpenAI-compatible API)
- scipy (for statistical tests)

```bash
pip install fastapi uvicorn openai scipy pyyaml
```

### Configuration

Copy `src/config.example.yaml` to `src/config.yaml` and fill in your API credentials:

```bash
cp src/config.example.yaml src/config.yaml
# Edit config.yaml: set your api_key_env or base_url
```

### Run a Single Test

```bash
# Terminal 1: start mock server
python src/mock_server.py

# Terminal 2: run a single test
export DEEPSEEK_API_KEY="your-key"
python src/test_single.py --payload standard --safety
```

### Run Full Experiment

```bash
python src/run_experiment.py
```

Results are written to `results/raw_results.csv`.

---

## Citation & Acknowledgments

We draw on conceptual frameworks from:

- Greshake et al. — "Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection" (arXiv:2302.12173)
- Silent Egress (arXiv:2602.22450) — methodology for measuring prompt injection egress
- McGuire & Papageorgis (1961) — inoculation theory (original "prebunking" concept in persuasion psychology)

---

## License

MIT. See repository root for full license text.

---

# 预先接种式提示词注入：预先告知能否放大间接提示词注入成功率？

> 实证研究 — **进行中**

**一句话摘要：** 本研究借鉴诈骗心理学中的"预先接种"概念，实证测试在间接提示词注入中预先告知模型"未来的安全提示是伪造的"这一叙事，是否会提升绕过运行时安全防御的成功率。

---

## 核心发现（初步，仅 DeepSeek-V3）

1. **归因叙事有显著独立效应**（OR = 13.5, p < 0.0001）。仅将注入内容标注为来自可信来源，即可将数据外发率从 10% 提升至 60%。
2. **强制型 override 指令已接近天花板**（96.7% 外发率）。"预先接种"框架在此区间的边际效应有限。
3. **归因叙事 × 弱化 override 的交互效应在不同统计尺度下不一致：**
   - Firth 惩罚 logistic 回归：交互项 p = 0.067（边界，对数几率尺度 CI 跨零）
   - Bootstrap 交互差值（概率尺度）：28.3pp 协同增益，95% CI [8.3pp, 51.7pp]，p = 0.013
   - Fisher OR ratio：5.0×，p < 0.0001
   - **解读：** 概率尺度上交互效应真实存在，但对数几率尺度因准分离导致标准误膨胀。需更大样本和跨模型验证。
4. **单模型局限：** 所有实验仅在 DeepSeek-V3 上完成，跨模型泛化性尚未验证——这是当前工作的主要局限。

---

## 状态

⚠️ **本仓库内容为初步实验结果，非最终结论。** 欢迎讨论和复现。

---

## 复现方式

见上方 Quick Start 部分。

---

## 引用与致谢

借鉴了 Greshake et al. 的间接提示词注入框架、Silent Egress 的外发测量方法，以及 McGuire & Papageorgis 的接种理论原始概念。

---

## 许可

MIT。完整许可文本参见仓库根目录。
