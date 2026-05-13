# 18天Agent学习冲刺计划

> 18天内具备 AI Agent 实习面试能力 | Agent开发 + LeetCode Hot100 + 面试八股
> 计划周期：2026年5月13日 - 5月31日（18天学习 + 1天缓冲）

## 仓库内容

本仓库是**自包含的**——所有学习材料、练习代码、教程文档都在一个文件夹里。

```
AgentLearningPlan/
├── README.md                              ← 本文件
├── 18天Agent学习冲刺计划.md                ← 每日详细计划（含精确文件路径）
├── .gitignore
│
├── daily_exercises/       16 files        ← 每天练习代码（12 py + 3 md + 1 README）
├── EasyAgent/              3 files        ← 入门级 Agent 代码
│
├── hello-agents/          139 files       ← ⭐⭐⭐ 主教程（精选）
│   ├── docs/         16章教程文档
│   ├── code/         Ch4/Ch7/Ch8/Ch10/Ch11/Ch12 代码
│   ├── Extra-Chapter/ 面试答案 + 补充知识（8个）
│   └── Co-creation-projects/
│
├── ai-agents-from-zero/   93 files        ← ⭐⭐ 辅教程（精选）
│   ├── 18章 LangChain/LangGraph 教程
│   ├── AI智能体面试题库-精简版.md  (75题)
│   ├── AI智能体与大模型应用开发面试题库.md
│   ├── 全书术语表.md
│   └── 实战项目-电商问数/  (17章)
│
└── VideoCode/             34 files        ← ⭐⭐⭐ 实战补充（精选）
    ├── Agent的概念、原理与构建模式/  (ReActAgent + Prompt模板)
    ├── MCP 与 Function Calling/MarkChat/  (MCP 全栈应用)
    ├── A2A协议深度解析(1)(2)/             (A2A单Agent + 多Agent)
    ├── 使用Python构建RAG系统/             (RAG notebook)
    ├── MCP终极指南-进阶篇/                (真实天气API + 日志)
    └── MCP终极指南-番外篇/                (Cline/ReAct 系统提示词)

总计：~230 个精选文件（只包含计划中实际引用的文件）
```

## 三套材料分工

| 材料 | 角色 | 用途 |
|------|------|------|
| **hello-agents**（16章）| ⭐⭐⭐ 主教程 | 理解 Agent 原理 → 自建框架 → 面试答案（2344行） |
| **VideoCode**（7项目）| ⭐⭐⭐ 实战补充 | Agent / RAG / MCP / A2A 全栈可运行项目 |
| **ai-agents-from-zero**（26章）| ⭐⭐ 辅教程 | LangChain / LangGraph API 参考 + 75题题库 + 电商项目 |
| **daily_exercises** | ⭐ 每日练习 | 每天动手的完整可运行代码 |

## 快速开始

### 环境要求

- Python 3.10+
- DeepSeek API Key（在 `.env` 中配置 `DEEPSEEK_API_KEY` 和 `DEEPSEEK_BASE_URL`）

### 安装依赖

```bash
pip install openai python-dotenv langchain langchain-openai langchain-core langgraph
pip install chromadb sentence-transformers mcp langchain-mcp-adapters
```

### 运行练习代码

```bash
# Windows 必须加 PYTHONIOENCODING（解决 emoji GBK 编码问题）
PYTHONIOENCODING=utf-8 python daily_exercises/day02_多工具Agent练习.py

# Day08 RAG 需设 HuggingFace 镜像（国内无法直连）
HF_ENDPOINT=https://hf-mirror.com PYTHONIOENCODING=utf-8 python daily_exercises/day08_RAG全链路实战.py
```

## 使用方式

1. **上午 3-4h**：打开 `18天Agent学习冲刺计划.md`，按当天表格的「阅读」「代码」逐个对照
2. **下午 3-4h**：LeetCode Hot100 刷题（四刷第 58-100 题）
3. **晚上 1-2h**：背诵对应八股，脱稿复述

## 面试项目故事线

```
Level 1: EasyAgent
  "用OpenAI原生API手写完整Agent循环"
  代码：EasyAgent/demo2.py、daily_exercises/day02_多工具Agent练习.py

Level 2: VideoCode ReActAgent + HelloAgents 自建框架
  "将代码抽象为可复用框架，支持 ReAct/Plan-Solve/Reflection 三种范式"
  代码：VideoCode/Agent的概念、原理与构建模式/agent.py、
        daily_exercises/supplement_01_agent_paradigms.py

Level 3: MCP全栈 + A2A多Agent + LangGraph 工业级应用
  "MCP暴露工具、A2A多Agent协作、LangGraph构建复杂工作流"
  代码：VideoCode/MCP与FunctionCalling/MarkChat/、
        VideoCode/A2A协议深度解析/、
        daily_exercises/day10-14
```

## 特点

- **自包含**：一个 git clone 获取全部学习材料
- **精选文件**：只包含计划中实际引用的 ~230 个文件，不含无关内容
- **无 git 污染**：不含任何外部仓库的 `.git` 目录
- **精确路径**：计划中每个文件路径都真实对应

> **最后更新：** 2026年5月13日
