Abstract: This article analyzes the ongoing divergence of AI security into three distinct research and practice directions as of 2026: (1) LLM Security — focused on model-level attacks including prompt injection evolution, MCP protocol vulnerabilities, and long-term memory poisoning; (2) Agentic Security — addressing system-level risks from AI agents with real-world permissions, tool chaining, and emergent组合式 vulnerabilities; (3) AI for Security — covering the rapidly maturing applications of AI in vulnerability research, penetration testing, SOC operations, and compliance automation. Provides directional context for this repository's focus on Agentic Security.

> **仓库说明：** 本文从方向演进视角分析 AI 安全的三大分支。本仓库核心研究聚焦于**第二方向（Agentic Security）**，其余两个方向作为行业背景与技术语境存在。

# AI Security 正在分裂成三个方向（2026）

2023 年以前，"AI 安全"几乎等同于：

* 模型越狱（Jailbreak）
* Prompt Injection（提示词注入）
* 幻觉（Hallucination）
* 内容安全（Content Safety）

但进入 2025~2026 年后，AI 安全的边界已经开始快速扩张。

随着：

* MCP（Model Context Protocol）
* AI Agent
* 长期记忆系统（Long-term Memory）
* 自动化工作流
* Tool Calling
* AI Coding Agent
* 多 Agent 协同系统

开始进入真实生产环境，AI 安全已经不再只是"大模型安全"。

今天的 AI Security，实际上正在演变成三个不同的方向：

---

# 1. LLM Security：大模型自身安全

这是目前最主流、讨论最多、也是研究最成熟的 AI 安全方向。

核心问题是：

> "模型本身是否会被操控？"

目前主流研究主要集中在：

* Prompt Injection
* Jailbreak
* Tool Injection
* MCP Security
* Memory Poisoning
* RAG Security
* Model Alignment
* Agent Prompt Manipulation

等方向。

---

# Prompt Injection 已经进入第二阶段

早期 Prompt Injection 非常简单：

Ignore previous instructions.

这种攻击本质上只是"覆盖系统提示词"。

但到了 2026 年，真正危险的已经不是 Direct Prompt Injection，而是：

# Indirect Prompt Injection（间接提示词注入）

攻击者不再直接与模型对话。

而是通过：

* 恶意网页
* 恶意 Markdown
* 恶意 PR
* 恶意知识库
* 恶意 MCP Metadata
* 恶意文档
* 恶意 RAG 数据

去污染模型"读取的数据"。

这是一个非常重要的变化。

因为传统 Web 安全里：

"输入"通常来自用户。

但在 Agent 系统中：

模型会主动读取外部环境。

于是：

> 外部环境本身，
> 开始成为攻击面。

微软在 2026 年关于 Agent Framework 的研究中，已经明确提到：

Prompt Injection 正在从"语言攻击"演变为"系统攻击"，甚至可能进一步转化为宿主机级别的 RCE 风险。

---

# MCP：AI Agent 时代的"USB 协议"

MCP（Model Context Protocol）正在快速成为 AI Agent 的标准接口层。

它解决的问题是：

LLM 如何安全、标准化地调用工具。

本质上：

MCP 正在扮演 AI 世界中的：

* USB
* RPC
* Plugin Interface
* Tool Bus

这样的角色。

但与此同时：

MCP 也引入了新的攻击面。

目前已经公开讨论的问题包括：

* Tool Poisoning
* Capability Spoofing
* Context Pollution
* Permission Escalation
* Multi-Agent Trust Propagation
* Metadata Prompt Injection

其中最危险的问题之一在于：

# MCP 的攻击很多是"协议级"的

也就是说：

即使单个 MCP Server 写得没有漏洞，

整个协议架构依然可能因为：

* 上下文拼接
* Tool 描述注入
* 权限继承
* 信任链传播

而产生系统性风险。

目前已有研究开始专门分析 MCP 与 Tool-integrated Agent 的安全问题。

---

# Long-term Memory：AI 开始拥有"长期状态"

这是目前很多人低估的问题。

过去的大模型：

本质上是"无状态"的。

但现在：

Agent 开始拥有：

* Persistent Memory
* RAG
* Vector Database
* Session Storage
* Memory File
* Cross-session Context

于是 AI 第一次真正拥有了：

# "长期状态"

这意味着：

攻击者可以开始研究：

# Memory Poisoning（记忆投毒）

包括：

* 污染长期记忆
* 持久化注入
* 植入错误事实
* 操控历史上下文
* 跨 Session 持续影响 Agent

传统 Prompt Injection 的影响通常是一次性的。

但 Memory Poisoning：

可能是长期的。

甚至会形成：

> "持续性的行为偏移"

目前已有研究开始讨论 Retrieval-Augmented Agent 的长期记忆投毒问题。

---

# 2. Agentic Security：AI Agent 系统安全

这是我认为未来两年会快速爆发的方向。

因为：

AI 已经开始从"聊天"变成"执行"。

例如：

* OpenAI 的 Codex
* Anthropic 的 Claude Code
* Cursor
* GitHub Copilot Agent
* LangGraph
* CrewAI
* Semantic Kernel

这些系统已经开始拥有：

* Shell 权限
* Git 权限
* Browser 权限
* 文件系统权限
* 云平台权限
* CI/CD 权限
* API 权限

于是问题开始发生本质变化：

过去：

AI 只是"说错话"

现在：

AI 开始真正执行危险操作

---

# Agent 的真正风险不是单点漏洞

而是"组合式漏洞"

这是 AI Agent 与传统软件最大的区别。

传统漏洞：

通常是：

* 一个输入
* 一个缺陷
* 一个利用点

但 AI Agent 是：

LLM
+ Tools
+ Memory
+ Workflow
+ Browser
+ Shell
+ MCP
+ Plugins
+ CI/CD
+ Vector DB

单个组件可能都没有问题。

但：

* 上下文拼接
* Tool chaining
* 权限继承
* 多 Agent 协同
* 自动化流程组合

会产生新的风险。

这类问题其实非常接近：

# Emergent Vulnerability（涌现式漏洞）

即：

> 每个模块单独看都安全，
> 但系统组合后出现高危问题。

这也是 AI Agent 最危险、同时最难审计的问题。

---

# AI Coding Agent 最大的问题之一：上下文并不等于真正记忆

目前很多模型宣传：

* 128K Context
* 1M Context
* 10M Context

但超长上下文并不等于稳定长期记忆。

实际上：

上下文越长，

越容易出现：

* Context Drift
* Attention Dilution
* Earlier Context Loss
* Hallucinated Reconstruction
* Instruction Collapse

于是：

AI Coding Agent 在大型项目中经常会：

* 忘记前面的安全约束
* 错误继承历史代码
* 拼接危险逻辑
* 覆盖旧权限校验
* 引入新的逻辑缺陷

这一点在复杂工程项目中已经非常明显。

特别是：

当项目是：

# "拆分生成"的

问题会更加严重。

因为：

很多开发者会：

* 分模块生成代码
* 分阶段生成逻辑
* 分 Session 修改系统
* 多 Agent 协同开发

最终：

系统整体安全性可能已经偏离最初设计。

---

# AI Agent 已经开始改变漏洞发现方式

目前很多研究人员已经开始：

# AI-assisted Vulnerability Research

包括：

* Patch Diff 分析
* Variant Analysis
* Code Review
* Binary Analysis
* Fuzzing
* Exploit Chain Discovery

一些长期存在、复杂度较高的漏洞：

正在因为 AI 的辅助分析能力而被重新发现。

这里需要强调：

目前更准确的说法是：

AI-assisted Research

而不是：

AI autonomously discovered vulnerabilities

因为现阶段：

真正完成：

* 环境理解
* 利用链构建
* Exploit 稳定化

仍然高度依赖研究人员。

但 AI 已经显著提升了：

* 分析速度
* Patch 理解能力
* 大规模代码关联能力
* 变种漏洞挖掘效率

---

# 3. AI for Security：AI 驱动的网络安全

这是目前落地最快、商业化速度最快的方向。

核心问题不再是：

> "AI 是否安全"

而是：

# "AI 是否能增强安全能力"

---

# 当前最主流的 AI 安全应用

## 1. AI 漏洞挖掘

AI 已经开始被广泛用于：
* Static Analysis
* Dynamic Analysis
* Fuzzing
* Binary Reverse Engineering
* Patch Diff
* Variant Discovery

尤其是在：

* 大型代码库
* 内核
* Browser
* 驱动
* 云原生组件

中，AI 已经明显提高了分析效率。

---

## 2. AI 渗透测试

目前已经出现：

* AI Recon
* AI Payload Generation
* AI Web Pentest
* AI Agentic Pentest
* AI Exploit Assistance

但目前：

AI 更像：

# "高级渗透测试助手"

而不是：

# "完全自动化黑客"

因为真正困难的问题依然包括：

* 环境理解
* 横向移动
* 权限维持
* Exploit Chain
* 业务逻辑漏洞

这些仍然需要大量人工参与。

---

## 3. AI SOC / AI 蓝队

这是目前企业增长最快的方向之一。

包括：

* AI 告警分析
* AI 日志研判
* AI Threat Hunting
* AI 自动关联分析
* AI 流量异常检测

AI 特别适合：

* 高噪声环境
* 重复性工作
* 海量日志场景

它无法完全替代分析师。

但已经开始显著降低：

SOC 的人力消耗。

---

# AI + GRC / 等保 / 合规

这是国内目前很容易被忽视，但实际价值非常高的方向。

例如：

* 等保 2.0
* ISO 27001
* NIST
* CIS Benchmark

本质上大量工作其实是：

* 配置检查
* 文档映射
* 控制项验证
* 证据收集
* 审计流程

这些非常适合：

# Agent 化 + Skill 化

未来很可能出现：

Compliance Agent

自动完成：

* 基线检查
* 证据收集
* 风险分析
* 整改建议
* 初版审计报告

这会是 AI Security 很重要的落地方向。

---

# AI Security 的核心变化

过去：

AI 安全的问题是：

模型会不会说错话？

现在：

AI 安全的问题正在变成：

当 AI 拥有：
- 权限
- 工具
- 长期记忆
- 自动化流程
- Shell
- Browser
- 多 Agent 协作

它是否会成为一个真正的"系统"？

而：

> 任何复杂系统，
> 都一定会产生安全问题。

AI Security 的未来，

已经不再只是"大模型安全"。

而是：

# "AI 系统安全"

---

# References / Related Research

* "Breaking the Protocol: Security Analysis of MCP"
  arXiv, 2026

* "Prompt Injection Attacks on Agentic Coding Assistants"
  arXiv, 2026

* "Memory Poisoning Attacks on Retrieval-Augmented LLM Agents"
  Future Generation Computer Systems, 2026

* "Securing LLM-based Agents against Cyberattacks"
  Journal of Information Assurance and Security, 2026

* Microsoft Security Research:
  "Prompts Become Shells: RCE Vulnerabilities in AI Agent Frameworks"

* OWASP Top 10 for LLM Applications

* Google Project Zero / AI-assisted Variant Analysis Discussions

* Anthropic / OpenAI Agent Safety Research Papers
