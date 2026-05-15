# 18天Agent应用面试冲刺计划（5/13 - 5/31）

> **定位：** Agent 应用开发工程师面试，不含 LLM/VLM/RLHF 算法岗内容
> **目标：** 18天内具备 Agent 实习面试能力，覆盖 Agent 开发技能 + LeetCode + 八股背诵
> **每日时间分配：** 上午3-4h Agent学习 | 下午3-4h LeetCode + 代码练习 | 晚上1-2h 八股背诵 + 复盘
> **八股背诵：** 全部来自 `AI智能体面试题库-精简版.md`（75题），Extra01 仅作理解参考不强制背诵

---

## 路径缩写说明

所有路径均为相对路径，从本文件夹（AgentLearningPlan/）出发。

| 路径 | 说明 |
|------|------|
| `hello-agents/` | 主教程（docs/文档 + code/代码 + Extra-Chapter/面试答案） |
| `ai-agents-from-zero/` | 辅教程（LangChain/LangGraph 文档 + 题库 + 电商项目） |
| `VideoCode/` | 视频配套代码（马克的技术工作坊 · 7个全栈项目） |
| `daily_exercises/` | 每日练习代码（15个文件） |
| `EasyAgent/` | 入门级 Agent 代码 |
| LeetCode 笔记 | 本机路径 `D:/University/大学资料/面试/java面试/LeetCodeHot100/notes/`（外部目录，需自行调整） |

---

## 三套材料对比分析

| 维度 | hello-agents（主） | VideoCode（实战补充） | ai-agents-from-zero（辅） |
|------|-------------------|----------------------|--------------------------|
| 定位 | "从零构建智能体" — 理解原理，自研框架 | 视频教程配套代码 — 全栈实战 | "LangChain/LangGraph实战" — 用框架搭应用 |
| 章节数 | 16章 + Extra + 共创项目 | 7个项目（Agent/RAG/MCP/A2A） | 26章 + 2个实战项目 |
| 核心理念 | 先理解原理 → 再手写框架（HelloAgents） | 一个视频一个项目 → 从零跑通全栈 | 先学框架API → 再搭应用 |
| 代码风格 | OpenAI原生API → 自研HelloAgents框架 | OpenRouter + FastMCP + a2a + FastAPI | LangChain @tool / LCEL / LangGraph |
| 独特优势 | 三种范式手写、自建框架(Ch7)、Agentic RL(Ch11)、评估(Ch12)、上下文工程(Ch9) | ReAct类封装、MCP全栈(MarkChat)、A2A多Agent、RAG notebook | LangChain/LangGraph API、企业部署、电商问数项目 |
| 面试答案 | ✅ 参考答案 `Extra01-参考答案.md`（2344行） | — | ✅ 题库 `AI智能体面试题库-精简版.md`（75题） |

---

## 代码可运行性说明

所有 `.py` 文件语法均正确（已通过 `py_compile` 校验），但可运行程度分为三档：

| 标记 | 含义 | 操作 |
|------|------|------|
| ✅ **直接可跑** | DeepSeek API 开箱即用 | 配好 `.env` 即可 |
| 🔧 **需配置** | 需改 env 变量或 API 地址 | 按下方说明改一个文件即可 |
| 📖 **阅读为主** | 缺包/缺GPU，不建议真跑 | 计划里就当阅读理解用 |

### .env 配置（一次性操作）

在项目根目录 `.env` 文件中，确保有以下变量（缺一不可）：

```bash
# ===== 原有变量（保留）=====
DEEPSEEK_API_KEY=sk-xxx
DEEPSEEK_BASE_URL=https://api.deepseek.com

# ===== 新增：供 hello-agents Ch4/Ch7 代码使用 =====
LLM_MODEL_ID=deepseek-chat
LLM_API_KEY=sk-xxx              # 和上面同一个 key
LLM_BASE_URL=https://api.deepseek.com
```

> 💡 `LLM_*` 三行加上后，hello-agents 的 `HelloAgentsLLM` 类就能直接走 DeepSeek，不需要改任何 Python 代码。

### 各来源详细状态

| 代码来源 | 文件数 | 状态 | 跑起来的操作 |
|----------|--------|------|-------------|
| `daily_exercises/` | 12 py | ✅ 直接可跑 | `.env` 配好 `DEEPSEEK_API_KEY` + `DEEPSEEK_BASE_URL` |
| `EasyAgent/` | 3 py | ✅ 直接可跑 | 同上 |
| `VideoCode/` | 9 py | 🔧 需适配 | 用 OpenRouter API。如要跑：改 `base_url` 为 DeepSeek、model 改为 `deepseek-chat`；或用 `uv` + OpenRouter key 原封不动跑。**建议当阅读理解**，核心价值在代码逻辑 |
| `hello-agents/code/chapter4/` | 5 py | 🔧 需配置 | `.env` 加上 `LLM_MODEL_ID`/`LLM_API_KEY`/`LLM_BASE_URL`（见上方） |
| `hello-agents/code/chapter7/` | 7 py | 📖 需装包 | `pip install helloagents` + `.env` 配 `LLM_*` 三个变量 |
| `hello-agents/code/chapter8/` | 3 py | 📖 需装包 | 同上 |
| `hello-agents/code/chapter10/` | 22 py | 📖 需装包 | `pip install helloagents fastmcp` |
| `hello-agents/code/chapter11/` | 1 py | 📖 缺GPU | SFT/GRPO 训练需 torch + CUDA GPU，个人电脑跑不了，阅读了解即可 |
| `hello-agents/code/chapter12/` | 1 py | 📖 需装包 | `pip install helloagents` |

> 💡 **学习策略**：真正需要动手跑的是 `daily_exercises/`（每天代码练习）。hello-agents 和 VideoCode 的代码主要是「阅读+对比」，看懂了就行——面试问的是你理不理解代码结构，不是问你跑没跑过 `helloagents` 包。

---

## 学习材料清单（含完整路径）

| 优先级 | 材料 | 完整路径 |
|--------|------|----------|
| ⭐⭐⭐ | hello-agents 教程 | `hello-agents/docs/` |
| ⭐⭐⭐ | hello-agents Ch4 代码（独立可运行） | `hello-agents/code/chapter4/ReAct.py`、`Plan_and_solve.py`、`Reflection.py`、`llm_client.py`、`tools.py` |
| ⭐⭐⭐ | Plan-Solve + Reflection 适配版 | `daily_exercises/supplement_01_agent_paradigms.py` |
| ⭐⭐⭐ | hello-agents 面试答案 | `hello-agents/Extra-Chapter/Extra01-参考答案.md` |
| ⭐⭐⭐ | hello-agents 面试题目 | `hello-agents/Extra-Chapter/Extra01-面试问题总结.md` |
| ⭐⭐⭐ | VideoCode ReAct Agent + Prompt模板 | `VideoCode/Agent的概念、原理与构建模式/agent.py`、`prompt_template.py` |
| ⭐⭐⭐ | VideoCode MarkChat（MCP全栈） | `VideoCode/MCP 与 Function Calling 到底什么关系/MarkChat/` |
| ⭐⭐ | VideoCode A2A协议（单Agent+多Agent） | `VideoCode/A2A协议深度解析(1)/`、`A2A协议深度解析(2)/` |
| ⭐⭐ | VideoCode RAG notebook | `VideoCode/使用Python构建RAG系统/rag/main.ipynb` |
| ⭐⭐ | VideoCode MCP进阶（真实天气API） | `VideoCode/MCP终极指南-进阶篇/weather/weather.py` |
| ⭐⭐ | VideoCode 番外篇（系统提示词） | `VideoCode/MCP终极指南-番外篇/` |
| ⭐⭐ | hello-agents Ch7-12 框架代码 | `hello-agents/code/chapter{7-12}/`（需 `pip install helloagents`） |
| ⭐⭐ | ai-agents-from-zero 教程 | `ai-agents-from-zero/` 各章 md 文件 |
| ⭐⭐ | 面试题库（75题） | `ai-agents-from-zero/AI智能体面试题库-精简版.md` |
| ⭐ | daily_exercises（15个）| `daily_exercises/` |
| — | EasyAgent 入门代码 | `EasyAgent/demo.py`、`EasyAgent/demo2.py`、`EasyAgent/practice.py` |
| — | LeetCode 完整题库 | `D:/University/大学资料/面试/java面试/LeetCodeHot100/notes/LeetCodeHot100完成情况.md` |
| — | LeetCode 四刷进度 | `D:/University/大学资料/面试/java面试/LeetCodeHot100/notes/LeetCodeFourthPass.md` |

---

## 当前进度盘点

### LeetCode四刷已完成（43题）
1,2,3,4,5,10,11,15,17,20,21,22,23,31,32,33,34,39,42,46,48,49,53,55,56,62,64,70,72,75,76,78,79,84,85,94,96,98,101,102,104,105,114

### LeetCode四刷待完成（57题）
19, 121, 124, 128, 136, 139, 141, 142, 146, 148, 152, 155, 160, 169, 198, 200, 206, 207, 208, 215, 221, 226, 234, 236, 238, 239, 240, 253, 279, 283, 287, 297, 300, 301, 309, 312, 322, 337, 338, 347, 394, 399, 406, 416, 437, 438, 448, 461, 494, 538, 543, 560, 581, 617, 621, 647, 739

---

## 每日详细计划

---

### 📅 第1天 | 5月13日（周三）| Agent认知 + 三种经典范式

**🎯 Agent学习（上午3-4h）**

> 核心目标：建立Agent全局认知，手写 ReAct / Plan-Solve / Reflection 三种范式

**📖 阅读：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | hello-agents Ch1 初识智能体（30min） | `hello-agents/docs/第一章 初识智能体.md` |
| 2 | hello-agents Ch2 智能体发展史（20min） | `hello-agents/docs/第二章 智能体发展史.md` |
| 3 | hello-agents Ch3 大语言模型基础（30min） | `hello-agents/docs/第三章 大语言模型基础.md` |
| 4 | hello-agents Ch4 智能体经典范式构建（30min） | `hello-agents/docs/第四章 智能体经典范式构建.md` |
| 5 | （可选）ai-agents-from-zero 大模型认知 | `ai-agents-from-zero/1-1-大模型认知与工程概览.md` |

**💻 代码：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | **主练：Plan-Solve + Reflection 范式（已适配DeepSeek）** | `daily_exercises/supplement_01_agent_paradigms.py` |
| 2 | **★最佳：VideoCode ReAct（类封装+XML标签+参数解析器）** | `VideoCode/Agent的概念、原理与构建模式/agent.py` |
| 3 | 对比：VideoCode Prompt模板（了解工业级 ReAct template） | `VideoCode/Agent的概念、原理与构建模式/prompt_template.py` |
| 4 | 对比：hello-agents 原版 ReAct | `hello-agents/code/chapter4/ReAct.py` |
| 5 | 参考：hello-agents LLM客户端封装 | `hello-agents/code/chapter4/llm_client.py` |
| 6 | 参考：hello-agents 工具执行器 | `hello-agents/code/chapter4/tools.py` |
| 7 | 补充阅读：EasyAgent代码精读（你的原始代码，对照看） | `daily_exercises/day01_大模型认知与EasyAgent精读.md` |

> 🔧 **Ch4 代码要跑？** 在 `.env` 加上 `LLM_MODEL_ID=deepseek-chat`、`LLM_API_KEY=你的key`、`LLM_BASE_URL=https://api.deepseek.com` 即可（详见文首「代码可运行性说明」）。supplement_01 已适配 DeepSeek，直接可跑。

**📝 LeetCode（下午3-4h）| 4题**
| # | 题号 | 题目 | 难度 | 考点 |
|---|------|------|------|------|
| 1 | 19 | 删除链表的倒数第N个结点 | 中等 | 快慢指针 |
| 2 | 121 | 买卖股票的最佳时机 | 简单 | 贪心/DP |
| 3 | 124 | 二叉树中的最大路径和 | 困难 | 树形DP |
| 4 | 128 | 最长连续序列 | 中等 | 哈希 |

**📖 八股背诵（晚上1-2h）| 第1章 基础认知与技术选型（5题全部）**

| # | 内容 | 路径 |
|---|------|------|
| 1 | Q1-1 RAG和微调的核心区别？能不能一起用？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q1-1 |
| 2 | Q1-2 什么是AI Agent？和传统AI应用区别 | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q1-2 |
| 3 | Q1-3 什么时候用Prompt/RAG/微调/Workflow/Agent？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q1-3 |
| 4 | Q1-4 Token和上下文窗口是什么？工程意义？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q1-4 |
| 5 | Q1-5 大模型应用上线前最关心哪些工程指标？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q1-5 |

---

### 📅 第2天 | 5月14日（周四）| 低代码平台 + 多工具调度

**🎯 Agent学习（上午3-4h）**

> 核心目标：了解低代码平台，练习多工具Agent调度

**📖 阅读：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | hello-agents Ch5 低代码平台（60min） | `hello-agents/docs/第五章 基于低代码平台的智能体搭建.md` |
| 2 | ai-agents-from-zero Python调用Dify | `ai-agents-from-zero/4-Python调用Dify平台工作流.md` |
| 3 | ai-agents-from-zero Python调用Coze | `ai-agents-from-zero/5-Python调用Coze平台工作流.md` |
| 4 | hello-agents Ch6 框架开发实践（浏览） | `hello-agents/docs/第六章 框架开发实践.md` |
| 5 | 低代码平台动手文档 | `daily_exercises/day03_Coze_Dify平台动手.md` |

**💻 代码：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | **主练：多工具Agent调度** | `daily_exercises/day02_多工具Agent练习.py` |
| 2 | 回顾：三种范式对比总结 | `daily_exercises/supplement_01_agent_paradigms.py`（末尾的对比表） |

**📝 LeetCode（下午3-4h）| 4题**
| # | 题号 | 题目 | 难度 | 考点 |
|---|------|------|------|------|
| 1 | 136 | 只出现一次的数字 | 简单 | 位运算 |
| 2 | 139 | 单词拆分 | 中等 | DP |
| 3 | 141 | 环形链表 | 简单 | 快慢指针 |
| 4 | 142 | 环形链表II | 中等 | 快慢指针+数学 |

**📖 八股背诵（晚上1-2h）| 第5章 Tools/FC/Agent（上）**

| # | 内容 | 路径 |
|---|------|------|
| 1 | Q5-1 ReAct模式是什么？（含CoT区别追问） | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q5-1 |
| 2 | Q5-2 Tool/FC/Agent三者关系？（含追问） | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q5-2 |
| 3 | Q5-3 Agent核心组件构成？（含挑战追问） | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q5-3 |
| 4 | Q5-6 "查天气、查新闻"AI助手怎么设计？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q5-6 |
| 5 | Q5-7 什么是"工具幻觉"？怎么缓解？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q5-7 |
| 6 | Q5-8 Function Calling和"输出JSON再解析"的区别？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q5-8 |

---

### 📅 第3天 | 5月15日（周五）| LangChain入门

**🎯 Agent学习（上午3-4h）**

> 核心目标：用LangChain重写EasyAgent的手动逻辑

**📖 阅读：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | LangChain概述与架构（30min） | `ai-agents-from-zero/9-LangChain概述与架构.md` |
| 2 | LangChain快速上手（30min） | `ai-agents-from-zero/10-LangChain快速上手与HelloWorld.md` |
| 3 | Model I/O与模型接入（40min） | `ai-agents-from-zero/11-Model-I-O与模型接入.md` |
| 4 | 提示词与消息模板（20min） | `ai-agents-from-zero/13-提示词与消息模板.md` |

**💻 代码：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | **主练：LangChain重写Agent** | `daily_exercises/day04_LangChain重写Agent.py` |

**📝 LeetCode（下午3-4h）| 4题**
| # | 题号 | 题目 | 难度 | 考点 |
|---|------|------|------|------|
| 1 | 146 | LRU缓存 | 中等 | 哈希+双向链表 |
| 2 | 148 | 排序链表 | 中等 | 归并排序 |
| 3 | 152 | 乘积最大子数组 | 中等 | DP |
| 4 | 155 | 最小栈 | 中等 | 辅助栈 |

**📖 八股背诵（晚上1-2h）| 第3章 RAG入门 + 第4章检索基础（上）**

| # | 内容 | 路径 |
|---|------|------|
| 1 | Q3-1 完整RAG流水线描述（含chunk/rerank追问） | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q3-1 |
| 2 | Q3-2 文本切块怎么设计？常见坑？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q3-2 |
| 3 | Q4-1 向量数据库和传统数据库的区别？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q4-1 |
| 4 | Q4-2 Embedding是什么？核心价值？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q4-2 |
| 5 | Q6-3 LangChain在今天的价值？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q6-3 |

---

### 📅 第4天 | 5月16日（周六）| 输出解析器 + LCEL链式调用

**🎯 Agent学习（上午3-4h）**

> 核心目标：掌握结构化输出和LCEL链式调用

**📖 阅读：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | 输出解析器（40min） | `ai-agents-from-zero/14-输出解析器.md` |
| 2 | LCEL与链式调用（30min） | `ai-agents-from-zero/15-LCEL与链式调用.md` |

**💻 代码：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | **主练：4种结构化输出 + @tool装饰器** | `daily_exercises/day05_输出解析器与结构化输出.py` |
| 2 | **主练：顺序链/分支链/并行链/记忆** | `daily_exercises/day06_LCEL链式调用与记忆.py` |

**📝 LeetCode（下午3-4h）| 4题**
| # | 题号 | 题目 | 难度 | 考点 |
|---|------|------|------|------|
| 1 | 160 | 相交链表 | 简单 | 双指针 |
| 2 | 169 | 多数元素 | 简单 | 摩尔投票 |
| 3 | 198 | 打家劫舍 | 中等 | DP |
| 4 | 200 | 岛屿数量 | 中等 | DFS/BFS |

**📖 八股背诵（晚上1-2h）| 第2章 Prompt工程 + 结构化输出（6题全部）**

| # | 内容 | 路径 |
|---|------|------|
| 1 | Q2-1 System Message和User Message怎么分工？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q2-1 |
| 2 | Q2-2 结构化输出做法与优缺点 | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q2-2 |
| 3 | Q2-3 Prompt Injection是什么？RAG/Agent为什么要小心？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q2-3 |
| 4 | Q2-4 如何系统优化提示词并把准确率做上去？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q2-4 |
| 5 | Q2-5 Prompt工程的边界是什么？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q2-5 |
| 6 | Q2-6 如何做Prompt版本管理与回归？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q2-6 |

---

### 📅 第5天 | 5月17日（周日）| 从手写Agent到create_agent

**🎯 Agent学习（上午3-4h）**

> 核心目标：理解 Agent 实现的三种抽象层级

**📖 阅读：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | Tools工具调用（50min） | `ai-agents-from-zero/17-Tools工具调用.md` |
| 2 | Agent智能体（50min） | `ai-agents-from-zero/21-Agent智能体.md` |

**💻 代码：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | **主练：create_agent 多工具Agent** | `daily_exercises/day07_多工具Agent.py` |
| 2 | 对比：手写正则调度 | `daily_exercises/day02_多工具Agent练习.py` |
| 3 | 对比：VideoCode ReActAgent（XML标签+类封装，最佳结构） | `VideoCode/Agent的概念、原理与构建模式/agent.py` |
| 4 | 对比：hello-agents ReAct范式 | `daily_exercises/supplement_01_agent_paradigms.py` |

**四种实现对比（面试重点）：**
```
day02 手写正则       → 正则提取 + 手动调度（最底层，看见所有细节）
VideoCode ReActAgent → XML标签 + 类封装（结构最清晰，工业级）
hello-agents Ch4    → HelloAgentsLLM + ToolExecutor（封装LLM和工具）
LangChain day07     → create_agent 一行代码（底层LangGraph驱动）
```

**📝 LeetCode（下午3-4h）| 4题**
| # | 题号 | 题目 | 难度 | 考点 |
|---|------|------|------|------|
| 1 | 206 | 反转链表 | 简单 | 链表基础 |
| 2 | 207 | 课程表 | 中等 | 拓扑排序/BFS |
| 3 | 208 | 实现Trie(前缀树) | 中等 | 设计 |
| 4 | 215 | 数组中的第K个最大元素 | 中等 | 快选/堆 |

**📖 八股背诵（晚上1-2h）| 第5章 Tools/FC/Agent（下）+ 第6章 LangGraph入门**

| # | 内容 | 路径 |
|---|------|------|
| 1 | Q5-4 Function Calling基本原理（含追问：和文本解析的区别？） | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q5-4 |
| 2 | Q5-5 设计Tool的工程原则 | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q5-5 |
| 3 | Q5-9 工具很多时怎么控制上下文长度和调用稳定性？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q5-9 |
| 4 | Q6-4 如何用LangChain开发Agent？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q6-4 |

---

### 📅 第6天 | 5月18日（周一）| RAG全链路实战

**🎯 Agent学习（上午3-4h）**

> 核心目标：从零搭建完整RAG pipeline

**📖 阅读：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | 向量数据库与Embedding实战（30min） | `ai-agents-from-zero/18-向量数据库与Embedding实战.md` |
| 2 | RAG检索增强生成（40min） | `ai-agents-from-zero/19-RAG检索增强生成.md` |
| 3 | hello-agents Ch8 记忆与检索 §8.1-8.3（40min） | `hello-agents/docs/第八章 记忆与检索.md` |

**💻 代码：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | **★先行（15min）：VideoCode RAG notebook — 7个cell直观看懂切分→嵌入→存储→检索→重排→生成** | `VideoCode/使用Python构建RAG系统/rag/main.ipynb` |
| 2 | **主练：RAG全链路（LangChain抽象版）** | `daily_exercises/day08_RAG全链路实战.py` |
| 3 | 参考：hello-agents 完整RAG pipeline（856行） | `hello-agents/code/chapter8/10_RAG_Pipeline_Complete.py` |

> ⚠️ 运行 day08 需设 `HF_ENDPOINT=https://hf-mirror.com`（国内无法直连HuggingFace）
> 💡 学习路径：先看 VideoCode notebook 理解裸 pipeline → 再看 day08 理解 LangChain 如何封装

**📝 LeetCode（下午3-4h）| 4题**
| # | 题号 | 题目 | 难度 | 考点 |
|---|------|------|------|------|
| 1 | 221 | 最大正方形 | 中等 | DP |
| 2 | 226 | 翻转二叉树 | 简单 | 树基础 |
| 3 | 234 | 回文链表 | 简单 | 快慢指针+反转 |
| 4 | 236 | 二叉树的最近公共祖先 | 中等 | 树 |

**📖 八股背诵（晚上1-2h）| 第3章 RAG全链路（中）重点！**

| # | 内容 | 路径 |
|---|------|------|
| 1 | Q3-3 RAG效果不好怎么排查？（含top_k追问） | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q3-3 |
| 2 | Q3-4 混合检索、重排序、查询改写分别解决什么问题？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q3-4 |
| 3 | Q3-5 RAG如何接入Agent执行链路？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q3-5 |
| 4 | Q3-7 什么是Lost in the Middle？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q3-7 |
| 5 | Q4-3 如何选择Embedding模型？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q4-3 |

---

### 📅 第7天 | 5月19日（周二）| 自建Agent框架 ⭐最重要！

**🎯 Agent学习（上午3-4h）**

> 核心目标：把你的EasyAgent代码升维成"自己的Agent框架" — 面试杀手锏

**📖 阅读：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | hello-agents Ch7 构建你的Agent框架（90min精读） | `hello-agents/docs/第七章 构建你的Agent框架.md` |

**💻 代码（二选一）：**

**方案A（推荐，不装包）：** 对比分析 + 自己设计框架

| # | 内容 | 路径 |
|---|------|------|
| 1 | hello-agents Ch4 LLM客户端封装 | `hello-agents/code/chapter4/llm_client.py` |
| 2 | hello-agents Ch4 工具执行器 | `hello-agents/code/chapter4/tools.py` |
| 3 | hello-agents Ch4 ReAct Agent | `hello-agents/code/chapter4/ReAct.py` |
| 4 | hello-agents Ch4 Plan-Solve Agent | `hello-agents/code/chapter4/Plan_and_solve.py` |
| 5 | hello-agents Ch4 Reflection Agent | `hello-agents/code/chapter4/Reflection.py` |
| 6 | 你的原始实现（对比用） | `EasyAgent/demo2.py` |

**方案B（完整体验）：** 安装 helloagents 包，运行框架测试

```bash
pip install helloagents  # 来自 https://github.com/jjyaoao/helloagents
# 装完后确保 .env 已配 LLM_MODEL_ID / LLM_API_KEY / LLM_BASE_URL
```

| # | 内容 | 路径 |
|---|------|------|
| 1 | LLM客户端扩展 | `hello-agents/code/chapter7/my_llm.py` |
| 2 | 计算器工具 | `hello-agents/code/chapter7/my_calculator_tool.py` |
| 3 | ReAct Agent实现 | `hello-agents/code/chapter7/my_react_agent.py` |
| 4 | Simple Agent实现 | `hello-agents/code/chapter7/my_simple_agent.py` |
| 5 | ReAct测试 | `hello-agents/code/chapter7/test_react_agent.py` |
| 6 | Simple Agent测试 | `hello-agents/code/chapter7/test_simple_agent.py` |

> 📖 **方案 A（推荐）**：不装包，纯阅读 Ch4 的 5 个文件 + Ch7 的源码，理解框架设计思路就够了——面试讲的是设计，不是你跑没跑过 `helloagents`。

**📝 LeetCode（下午3-4h）| 4题**
| # | 题号 | 题目 | 难度 | 考点 |
|---|------|------|------|------|
| 1 | 238 | 除自身以外数组的乘积 | 中等 | 前缀积 |
| 2 | 239 | 滑动窗口最大值 | 困难 | 单调队列 |
| 3 | 240 | 搜索二维矩阵II | 中等 | 二分/剪枝 |
| 4 | 253 | 会议室II | 中等 | 扫描线/堆 |

**📖 八股背诵（晚上1-2h）| 第3章 RAG进阶 + 第7章 记忆**

| # | 内容 | 路径 |
|---|------|------|
| 1 | Q3-8 有了超长上下文模型，还需要RAG吗？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q3-8 |
| 2 | Q3-9 复杂文档RAG/多模态RAG怎么做？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q3-9 |
| 3 | Q3-10 什么是Agentic RAG？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q3-10 |
| 4 | Q7-1 上下文窗口/短期记忆/长期记忆的关系？（含追问） | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q7-1 |
| 5 | Q7-2 如何为Agent设计短期和长期记忆？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q7-2 |

---

### 📅 第8天 | 5月20日（周三）| MCP协议 + 通信协议 ⭐最重要！

**🎯 Agent学习（上午3-4h）**

> 核心目标：理解MCP（面试必问），对比A2A/ANP

**📖 阅读：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | hello-agents Ch10 智能体通信协议（90min）| `hello-agents/docs/第十章 智能体通信协议.md` |
| 2 | ai-agents-from-zero MCP模型上下文协议 | `ai-agents-from-zero/20-MCP模型上下文协议.md` |

**💻 代码：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | **★主练：MarkChat 全栈MCP应用（Server+Client+Backend+前端+FC对比+日志）** | `VideoCode/MCP 与 Function Calling 到底什么关系/MarkChat/` |
| 2 | 精读 MarkChat backend.py — **FC调用 → MCP调用的对比切换** | `VideoCode/MCP 与 Function Calling 到底什么关系/MarkChat/backend.py` |
| 3 | 精读 MarkChat mcp_server.py + mcp_client.py — 标准MCP通信 | `VideoCode/MCP 与 Function Calling 到底什么关系/MarkChat/mcp_server.py`、`mcp_client.py` |
| 4 | 参考：day09 DeepSeek适配版MCP | `daily_exercises/day09_MCP协议实战.py` |
| 5 | 参考：VideoCode MCP进阶（真实天气API+日志） | `VideoCode/MCP终极指南-进阶篇/weather/weather.py` |
| 6 | 参考：VideoCode 番外篇（Cline/ReAct系统提示词） | `VideoCode/MCP终极指南-番外篇/` |
| 7 | 参考：hello-agents MCP/A2A示例（需helloagents） | `hello-agents/code/chapter10/` |

> 💡 MarkChat 是唯一一个**全栈可交互**的 MCP 实战项目，`backend.py` 里明确对比了 Function Calling 和 MCP 的两种工具执行路径，面试时讲 MCP vs FC 直接背这段！

**📝 LeetCode（下午3-4h）| 4题**
| # | 题号 | 题目 | 难度 | 考点 |
|---|------|------|------|------|
| 1 | 279 | 完全平方数 | 中等 | BFS/DP |
| 2 | 283 | 移动零 | 简单 | 双指针 |
| 3 | 287 | 寻找重复数 | 中等 | 快慢指针/二分 |
| 4 | 297 | 二叉树的序列化与反序列化 | 困难 | 树/设计 |

**📖 八股背诵（晚上1-2h）| 第7章 MCP专题（上）**

| # | 内容 | 路径 |
|---|------|------|
| 1 | Q7-3 什么是MCP？和Tool/RAG/Agent的区别？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q7-3 |
| 2 | Q7-4 MCP和Function Calling的关系？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q7-4 |
| 3 | Q7-5 MCP如何做到跨平台兼容？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q7-5 |
| 4 | Q7-6 MCP技术协议的主体内容？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q7-6 |
| 5 | Q7-7 MCP服务器开发流程？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q7-7 |
| 6 | Q7-8 Agent如何接入MCP工具？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q7-8 |

---

### 📅 第9天 | 5月21日（周四）| LangGraph入门

**🎯 Agent学习（上午3-4h）**

> 核心目标：掌握LangGraph四要素，会画图、会写条件边

**📖 阅读：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | LangGraph概述与快速入门（30min） | `ai-agents-from-zero/22-LangGraph概述与快速入门.md` |
| 2 | LangGraph API：图与状态（30min） | `ai-agents-from-zero/23-LangGraphAPI：图与状态.md` |
| 3 | LangGraph API：节点、边与进阶（40min） | `ai-agents-from-zero/24-LangGraphAPI：节点、边与进阶.md` |

**💻 代码：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | **主练：Agent + LangGraph入门** | `daily_exercises/day10_Agent与LangGraph入门.py` |

**📝 LeetCode（下午3-4h）| 5题（DP集中突破）**
| # | 题号 | 题目 | 难度 | 考点 |
|---|------|------|------|------|
| 1 | 300 | 最长递增子序列 | 中等 | DP+二分 |
| 2 | 301 | 删除无效的括号 | 困难 | BFS/回溯 |
| 3 | 309 | 买卖股票的最佳时机含冷冻期 | 中等 | DP状态机 |
| 4 | 312 | 戳气球 | 困难 | 区间DP |
| 5 | 322 | 零钱兑换 | 中等 | DP/背包 |

**📖 八股背诵（晚上1-2h）| 第6章 LangGraph框架（剩余）**

| # | 内容 | 路径 |
|---|------|------|
| 1 | Q6-1 LangGraph相比普通Workflow的最大价值？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q6-1 |
| 2 | Q6-2 State/Node/Edge分别代表什么？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q6-2 |
| 3 | Q6-5 LCEL的价值？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q6-5 |
| 4 | Q6-6 LangGraph进阶特性里最有工程价值的是哪些？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q6-6 |
| 5 | Q6-7 Checkpoint/HITL/Time-Travel怎么讲得更工程化？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q6-7 |

---

### 📅 第10天 | 5月22日（周五）| LangGraph多步Agent + 上下文工程

**🎯 Agent学习（上午3-4h）**

> 核心目标：构建复杂Agent图 + 理解上下文工程

**📖 阅读：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | hello-agents Ch9 上下文工程（50min） | `hello-agents/docs/第九章 上下文工程.md` |
| 2 | LangGraph高级特性（30min） | `ai-agents-from-zero/25-LangGraph高级特性.md` |

**💻 代码：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | **主练：LangGraph多步Agent** | `daily_exercises/day11_LangGraph多步Agent.py` |
| 2 | **主练：LangGraph高级特性** | `daily_exercises/day12_LangGraph高级特性.py` |

**📝 LeetCode（下午3-4h）| 4题**
| # | 题号 | 题目 | 难度 | 考点 |
|---|------|------|------|------|
| 1 | 337 | 打家劫舍III | 中等 | 树形DP |
| 2 | 338 | 比特位计数 | 简单 | DP/位运算 |
| 3 | 347 | 前K个高频元素 | 中等 | 堆/桶排序 |
| 4 | 394 | 字符串解码 | 中等 | 栈 |

**📖 八股背诵（晚上1-2h）| 第7章 MCP（下）+ 第4章检索进阶**

| # | 内容 | 路径 |
|---|------|------|
| 1 | Q7-9 MCP的流式HTTP传输核心优势？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q7-9 |
| 2 | Q7-10 MCP调用如何保证并发？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q7-10 |
| 3 | Q7-11 A2A和MCP的区别？什么时候需要多智能体？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q7-11 |
| 4 | Q7-12 有哪些热门的MCP工具？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q7-12 |
| 5 | Q4-4 近似检索和精确检索怎么权衡？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q4-4 |

---

### 📅 第11天 | 5月23日（周六）| 记忆系统 + Agent评估 + RL

**🎯 Agent学习（上午3-4h）**

> 核心目标：深入记忆系统 + 学会评估Agent + 了解Agent训练

**📖 阅读：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | hello-agents Ch8 记忆与检索（回看精读，60min） | `hello-agents/docs/第八章 记忆与检索.md` |
| 2 | hello-agents Ch12 智能体性能评估（50min） | `hello-agents/docs/第十二章 智能体性能评估.md` |
| 3 | hello-agents Ch11 Agentic RL（30min，了解） | `hello-agents/docs/第十一章 Agentic-RL.md` |

**💻 代码（浏览，需helloagents包或GPU）：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | 记忆巩固 Demo | `hello-agents/code/chapter8/06_Memory_Consolidation_Demo.py` |
| 2 | Agent + Tool 集成 | `hello-agents/code/chapter8/08_Agent_Tool_Integration.py` |
| 3 | Agent评估示例 | `hello-agents/code/chapter12/01_basic_agent_example.py` |
| 4 | GRPO训练Pipeline | `hello-agents/code/chapter11/06_complete_pipeline.py` |

**📝 LeetCode（下午3-4h）| 4题**
| # | 题号 | 题目 | 难度 | 考点 |
|---|------|------|------|------|
| 1 | 399 | 除法求值 | 中等 | 图/并查集 |
| 2 | 406 | 根据身高重建队列 | 中等 | 贪心 |
| 3 | 416 | 分割等和子集 | 中等 | DP/01背包 |
| 4 | 437 | 路径总和III | 中等 | 树+前缀和 |

**📖 八股背诵（晚上1-2h）| 第9章 评测 + 可观测性 + 成本**

| # | 内容 | 路径 |
|---|------|------|
| 1 | Q9-1 如何评估RAG或Agent？（含RAGAS/badcase追问） | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q9-1 |
| 2 | Q9-8 意图识别/任务路由怎么做？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q9-8 |
| 3 | Q9-9 大模型应用的可观测性怎么做？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q9-9 |
| 4 | Q9-10 控制成本优先从哪些层面下手？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q9-10 |
| 5 | Q9-11 模型路由怎么做？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q9-11 |

---

### 📅 第12天 | 5月24日（周日）| 多智能体 + 综合项目

**🎯 Agent学习（上午3-4h）**

> 核心目标：理解多Agent协作 + 看真实项目架构

**📖 阅读：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | LangGraph多智能体与A2A（40min） | `ai-agents-from-zero/26-LangGraph多智能体与A2A.md` |
| 2 | hello-agents Ch13 智能旅行助手（30min） | `hello-agents/docs/第十三章 智能旅行助手.md` |
| 3 | hello-agents Ch14 深度研究智能体（30min） | `hello-agents/docs/第十四章 自动化深度研究智能体.md` |
| 4 | 社区共创项目（浏览，20min） | `hello-agents/Co-creation-projects/README.md` |

**💻 代码：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | **主练：综合整合** | `daily_exercises/day14_EasyAgent深度改造.py` |
| 2 | **★A2A实战：单Agent天气服务** | `VideoCode/A2A协议深度解析(1)/weather/agent_executor.py` |
| 3 | **★A2A实战：多Agent协作（天气+机票）** | `VideoCode/A2A协议深度解析(2)/` |
| 4 | A2A示例请求/返回数据 | `VideoCode/A2A协议深度解析(1)/weather/示例/`、`VideoCode/A2A协议深度解析(2)/示例/` |

**📝 LeetCode（下午3-4h）| 4题**
| # | 题号 | 题目 | 难度 | 考点 |
|---|------|------|------|------|
| 1 | 438 | 找到字符串中所有字母异位词 | 中等 | 滑动窗口 |
| 2 | 448 | 找到所有数组中消失的数字 | 简单 | 原地哈希 |
| 3 | 461 | 汉明距离 | 简单 | 位运算 |
| 4 | 494 | 目标和 | 中等 | DP/背包 |

**📖 八股背诵（晚上1-2h）| 第8章 平台选型 + 第4章知识图谱**

| # | 内容 | 路径 |
|---|------|------|
| 1 | Q8-1 Coze/Dify和LangChain/LangGraph的关系？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q8-1 |
| 2 | Q8-2 各类Agent开发框架怎么选？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q8-2 |
| 3 | Q8-3 什么时候工作流比Agent更合适？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q8-3 |
| 4 | Q8-4 Python调用Dify/Coze工作流关注哪些工程细节？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q8-4 |
| 5 | Q8-5 RAGFlow等开源RAG平台怎么选型？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q8-5 |
| 6 | Q4-5 知识图谱/图数据库什么时候比纯向量检索更有价值？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q4-5 |
| 7 | Q4-6 GraphRAG适合什么场景？和传统向量RAG怎么选？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q4-6 |

---

### 📅 第13天 | 5月25日（周一）| 电商问数项目 + 项目表达

**🎯 Agent学习（上午3-4h）**

> 核心目标：理解完整的生产级Agent项目

**📖 阅读：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | 实战项目-电商问数 核心章节（90min） | `ai-agents-from-zero/实战项目-电商问数/` |
| 2 | hello-agents Ch15 赛博小镇（20min） | `hello-agents/docs/第十五章 构建赛博小镇.md` |

**💻 代码/文档：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | 电商问数项目剖析 | `daily_exercises/day13_电商问数项目剖析.md` |

**📝 LeetCode（下午3-4h）| 4题**
| # | 题号 | 题目 | 难度 | 考点 |
|---|------|------|------|------|
| 1 | 538 | 把二叉搜索树转换为累加树 | 中等 | 反向中序 |
| 2 | 543 | 二叉树的直径 | 简单 | 树形DP |
| 3 | 560 | 和为K的子数组 | 中等 | 前缀和+哈希 |
| 4 | 581 | 最短无序连续子数组 | 中等 | 双指针 |

**📖 八股背诵（晚上1-2h）| 第11章项目表达 + 第3章企业RAG + 内网部署**

| # | 内容 | 路径 |
|---|------|------|
| 1 | Q11-1 介绍做过的RAG/Agent项目怎么讲？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q11-1 |
| 2 | Q11-2 "为什么不用更热门的框架/模型"怎么答？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q11-2 |
| 3 | Q11-3 线上效果波动大怎么展示排障能力？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q11-3 |
| 4 | Q3-6 企业RAG为什么必须重视权限、版本和引用？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q3-6 |
| 5 | Q9-12 内网环境怎么设计Agent/RAG系统？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q9-12 |

---

### 📅 第14天 | 5月26日（周二）| LeetCode收尾 + 知识串联

**🎯 Agent学习（上午2-3h）**

> 核心目标：查漏补缺，知识体系串联

**📖 阅读：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | hello-agents Ch16 毕业设计（20min） | `hello-agents/docs/第十六章 毕业设计.md` |
| 2 | Extra02 上下文工程补充知识 | `hello-agents/Extra-Chapter/Extra02-上下文工程补充知识.md` |
| 3 | Extra05 Agent Skills vs MCP | `hello-agents/Extra-Chapter/Extra05-AgentSkills解读.md` |
| 4 | Extra06 GUI Agent科普 | `hello-agents/Extra-Chapter/Extra06-GUIAgent科普与实战.md` |
| 5 | Extra09 Agent开发踩坑经验 | `hello-agents/Extra-Chapter/Extra09-Agent应用开发实践踩坑与经验分享.md` |
| 6 | Extra10 Agent自进化 | `hello-agents/Extra-Chapter/Extra10-Agent自进化.md` |

**💻 代码：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | 快速过所有练习代码 | `daily_exercises/` 全部14+1个文件 |

**📝 LeetCode（下午3-4h）| 4题 — 四刷收尾**
| # | 题号 | 题目 | 难度 | 考点 |
|---|------|------|------|------|
| 1 | 617 | 合并二叉树 | 简单 | 树 |
| 2 | 621 | 任务调度器 | 中等 | 贪心 |
| 3 | 647 | 回文子串 | 中等 | 中心扩展/DP |
| 4 | 739 | 每日温度 | 中等 | 单调栈 |

**📖 八股背诵（晚上1-2h）| 安全 + 幻觉 + 部署（第9章全部）**

| # | 内容 | 路径 |
|---|------|------|
| 1 | Q9-2 什么是"幻觉"，怎么缓解 | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q9-2 |
| 2 | Q9-3 多用户Agent安全沙箱 | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q9-3 |
| 3 | Q9-4 Agent部署和运维指标 | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q9-4 |
| 4 | Q9-5 RAG系统实际部署面临哪些挑战？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q9-5 |
| 5 | Q9-6 如何确保Agent行为安全可控？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q9-6 |
| 6 | Q9-7 Agent链路耗时很长怎么定位瓶颈？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q9-7 |

---

### 📅 第15天 | 5月27日（周三）| LeetCode全面复习 + 八股场景题

**📖 阅读（上午2h）：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | 回顾薄弱八股（重刷精简版标记的薄弱题） | `ai-agents-from-zero/AI智能体面试题库-精简版.md` |
| 2 | 全书术语复习 | `ai-agents-from-zero/全书术语表.md` |

**📝 LeetCode（下午4h）| 四刷100题全面分类回顾**

> 按分类过思路（每道30秒：核心解法+复杂度+易错点）

- [ ] **哈希表**（8题）
- [ ] **双指针**（10题）
- [ ] **滑动窗口**（4题）
- [ ] **链表**（13题）
- [ ] **二叉树**（16题）
- [ ] **DP**（23题）
- [ ] **栈/单调栈**（7题）
- [ ] **堆/设计**（7题）
- [ ] **图/其他**（8题）

**📖 八股背诵（晚上2h）| 场景设计题**

| # | 内容 | 路径 |
|---|------|------|
| 1 | Q10-1 企业知识库问答系统设计 | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q10-1 |
| 2 | Q10-2 NL2SQL Agent风险控制 | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q10-2 |
| 3 | Q10-3 客服智能体设计 | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q10-3 |
| 4 | Q10-4 Agent完成判断与终止条件 | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q10-4 |
| 5 | Q10-5 Code Agent设计 | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q10-5 |

---

### 📅 第16天 | 5月28日（周四）| 业务场景设计题深度 + 高频LeetCode

**📖 场景设计题深度学习（上午3-4h）：**

| # | 内容 | 路径 |
|---|------|------|
| 1 | Q10-6/7 Deep Research系统设计 | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q10-6~7 |
| 2 | Q10-8 Python代码解释器设计 | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q10-8 |
| 3 | Q10-9 类Manus通用智能体设计 | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q10-9 |
| 4 | Q10-10 浏览器自动化Agent设计 | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q10-10 |
| 5 | Q10-11 真实/模拟环境Agent | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q10-11 |

**📝 LeetCode（下午2h）| 5道最高频题白板默写：**
- 146. LRU缓存 / 200. 岛屿数量 / 236. 二叉树最近公共祖先 / 300. 最长递增子序列 / 347. 前K个高频元素

**📖 八股背诵（晚上1-2h）| 第10章 场景设计题复盘 + 第9章 安全**

| # | 内容 | 路径 |
|---|------|------|
| 1 | Q10-6&7 Deep Research系统（脱稿复述架构） | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q10-6~7 |
| 2 | Q10-8 Python代码解释器（回顾） | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q10-8 |
| 3 | Q10-9 类Manus通用智能体（回顾） | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q10-9 |
| 4 | Q10-10 浏览器自动化Agent（回顾） | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q10-10 |
| 5 | Q10-11 真实/模拟环境Agent（回顾） | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q10-11 |
| 6 | Q9-6 如何确保Agent行为安全可控？（Day 14 回顾） | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q9-6 |

---

### 📅 第17天 | 5月29日（周五）| 全面模拟面试

**🎯 全天模拟面试训练（8h）**

**上午：Agent技术面试模拟（4h）**

| 模块 | 内容 | 参考材料 |
|------|------|----------|
| 1 | 自我介绍+项目介绍（30min） | 三层项目故事（见文末） |
| 2 | 基础认知快问快答（45min） | 精简版题库 Q1/Q5（第1章+第5章，共14题） |
| 3 | RAG深度问答（45min） | 精简版题库 Q3/Q4（第3章+第4章，共16题） |
| 4 | Agent+Tools+LangGraph（60min） | 精简版题库 Q6 + Q5剩余（第6章+第5章） |
| 5 | MCP+A2A+自建框架（45min） | 精简版题库 Q7（第7章，12题）+ 三层项目故事 L2 |

**下午：算法面试模拟（3h）**
- 随机抽5道Hot100题，限时25分钟/题，白板编程

**晚上：查漏补缺（1h）**

---

### 📅 第18天 | 5月30日（周六）| 项目打磨 + 最后冲刺

**📖 项目简历话术打磨（上午3-4h）：**

| # | 内容 | 参考材料 |
|---|------|----------|
| 1 | 三层项目故事写成简历描述 | `EasyAgent/demo2.py` + `hello-agents/code/chapter4/` + `daily_exercises/` |
| 2 | 热点技术话题准备（60min） | AI Coding工具、Agent未来趋势、MCP/A2A生态 |
| 3 | 最后代码过一遍（30min） | `daily_exercises/` 关键文件 |

**📝 LeetCode（下午2h）：** 回顾全部100题 + 重做3-5道最弱题目

**📖 八股背诵（下午+晚上3h）：** 全部必刷+高频过最后一遍

| # | 参考材料 |
|---|----------|
| 1 | Q12-1 常用哪些AI开发工具？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q12-1 |
| 2 | Q12-2 Cursor、Claude Code、Copilot的差异？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q12-2 |
| 3 | Q12-3 AI应用工程师和算法研究岗的差异？ | `ai-agents-from-zero/AI智能体面试题库-精简版.md` Q12-3 |
| 4 | 全部75题快速过最后一遍（重点：必刷+高频标记的题目） | `ai-agents-from-zero/AI智能体面试题库-精简版.md` |

---

### 📅 第19天（机动）| 5月31日（周日）| 缓冲日

补进度 / 再一轮模拟面试 / 整理面试清单投简历

---

## LeetCode Hot100 四刷进度总览

完整题库：`D:/University/大学资料/面试/java面试/LeetCodeHot100/notes/LeetCodeHot100完成情况.md`
四刷进度：`D:/University/大学资料/面试/java面试/LeetCodeHot100/notes/LeetCodeFourthPass.md`

### 数据校验
- 完整题库：**100题** | 四刷已完成：**43题** | 四刷待完成：**57题**

### 每日分配
| 日期 | 题目 | 数量 |
|------|------|------|
| 5/13 | 19, 121, 124, 128 | 4 |
| 5/14 | 136, 139, 141, 142 | 4 |
| 5/15 | 146, 148, 152, 155 | 4 |
| 5/16 | 160, 169, 198, 200 | 4 |
| 5/17 | 206, 207, 208, 215 | 4 |
| 5/18 | 221, 226, 234, 236 | 4 |
| 5/19 | 238, 239, 240, 253 | 4 |
| 5/20 | 279, 283, 287, 297 | 4 |
| 5/21 | 300, 301, 309, 312, 322 | 5 |
| 5/22 | 337, 338, 347, 394 | 4 |
| 5/23 | 399, 406, 416, 437 | 4 |
| 5/24 | 438, 448, 461, 494 | 4 |
| 5/25 | 538, 543, 560, 581 | 4 |
| 5/26 | 617, 621, 647, 739 | 4 |
| **合计** | | **57** |

---

## 面试八股材料总览

| 来源 | 路径 | 用途 |
|------|------|------|
| **精简版题库（主）** | `ai-agents-from-zero/AI智能体面试题库-精简版.md` | **75题，全部背诵。** 按12章分类，每题3-6行要点 |
| 全题库（参考） | `ai-agents-from-zero/AI智能体与大模型应用开发面试题库.md` | 完整版，精简版的详细展开 |
| Extra01 参考答案（翻阅） | `hello-agents/Extra-Chapter/Extra01-参考答案.md` | **不强制背诵。** 精简版某个题理解不透时，去 Extra01 §4(Agent) §5(RAG) 找对应段落看详细解释 |
| Extra01 §1-3（跳过） | 同上 | LLM/VLM/RLHF 算法岗内容，Agent 应用面试不考 |

---

## 项目故事线（面试杀手锏）

```
Level 1: EasyAgent
  "我用OpenAI原生API手写完整Agent循环"
  代码：EasyAgent/demo2.py、daily_exercises/day02_多工具Agent练习.py

Level 2: VideoCode ReActAgent + HelloAgents 自建框架
  "我把代码抽象成可复用框架，支持 ReAct/Plan-Solve/Reflection 三种范式"
  代码：VideoCode/Agent的概念、原理与构建模式/agent.py、
        daily_exercises/supplement_01_agent_paradigms.py、
        hello-agents/code/chapter4/

Level 3: MCP全栈 + A2A多Agent + LangGraph工业级应用
  "用MCP暴露工具、用A2A实现多Agent协作、用LangGraph构建复杂工作流"
  代码：VideoCode/MCP 与 Function Calling 到底什么关系/MarkChat/（MCP全栈）、
        VideoCode/A2A协议深度解析(1)(2)/（A2A多Agent）、
        daily_exercises/day10-12、day14（LangGraph + 综合整合）
```

---

## 每日检查清单

- [ ] 阅读材料全部打开过？（按上表中的路径逐个打开）
- [ ] 代码运行并理解了？（`PYTHONIOENCODING=utf-8 python <文件路径>`）
- [ ] 八股今天的内容能脱稿复述？
- [ ] LeetCode今日题目全部AC？
- [ ] 标记今日薄弱点？

---

## 所有练习代码清单（全部✅已验证）

### daily_exercises（12个可运行py + 3个md）

| 文件 | 内容 | 运行命令 |
|------|------|----------|
| `daily_exercises/day02_多工具Agent练习.py` | 正则提取+多工具路由 | `PYTHONIOENCODING=utf-8 python daily_exercises/day02_多工具Agent练习.py` |
| `daily_exercises/day04_LangChain重写Agent.py` | ChatPromptTemplate+LCEL | `PYTHONIOENCODING=utf-8 python daily_exercises/day04_LangChain重写Agent.py` |
| `daily_exercises/day05_输出解析器与结构化输出.py` | 4种结构化输出+@tool | `PYTHONIOENCODING=utf-8 python daily_exercises/day05_输出解析器与结构化输出.py` |
| `daily_exercises/day06_LCEL链式调用与记忆.py` | 分支/并行链+记忆 | `PYTHONIOENCODING=utf-8 python daily_exercises/day06_LCEL链式调用与记忆.py` |
| `daily_exercises/day07_多工具Agent.py` | create_agent | `PYTHONIOENCODING=utf-8 python daily_exercises/day07_多工具Agent.py` |
| `daily_exercises/day08_RAG全链路实战.py` | RAG完整pipeline | `HF_ENDPOINT=https://hf-mirror.com PYTHONIOENCODING=utf-8 python daily_exercises/day08_RAG全链路实战.py` |
| `daily_exercises/day09_MCP协议实战.py` | MCP Server/Client（DeepSeek适配） | `PYTHONIOENCODING=utf-8 python daily_exercises/day09_MCP协议实战.py` |
| `daily_exercises/day10_Agent与LangGraph入门.py` | StateGraph+ToolNode | `PYTHONIOENCODING=utf-8 python daily_exercises/day10_Agent与LangGraph入门.py` |
| `daily_exercises/day11_LangGraph多步Agent.py` | 意图路由+置信度评估 | `PYTHONIOENCODING=utf-8 python daily_exercises/day11_LangGraph多步Agent.py` |
| `daily_exercises/day12_LangGraph高级特性.py` | Checkpoint/Streaming/HITL | `PYTHONIOENCODING=utf-8 python daily_exercises/day12_LangGraph高级特性.py` |
| `daily_exercises/day14_EasyAgent深度改造.py` | 综合整合 | `PYTHONIOENCODING=utf-8 python daily_exercises/day14_EasyAgent深度改造.py` |
| `daily_exercises/supplement_01_agent_paradigms.py` | Plan-Solve+Reflection | `PYTHONIOENCODING=utf-8 python daily_exercises/supplement_01_agent_paradigms.py` |

### VideoCode 实战项目

| 项目 | 内容 | 运行方式 |
|------|------|----------|
| `VideoCode/Agent的概念、原理与构建模式/` | ReActAgent（XML标签+类封装） | `cd VideoCode/Agent的概念、原理与构建模式/ && uv run agent.py <目录路径>` |
| `VideoCode/MCP 与 Function Calling 到底什么关系/MarkChat/` | MCP全栈应用（Server+Client+Backend+前端） | `cd VideoCode/MCP 与 Function Calling 到底什么关系/MarkChat/ && uv run start.py` |
| `VideoCode/A2A协议深度解析(1)/weather/` | A2A单Agent天气服务 | `cd VideoCode/A2A协议深度解析(1)/weather/ && uv run .` |
| `VideoCode/A2A协议深度解析(2)/` | A2A多Agent（天气+机票） | `cd VideoCode/A2A协议深度解析(2)/weather/ && uv run .`（再启动flight） |
| `VideoCode/使用Python构建RAG系统/rag/main.ipynb` | RAG notebook（7个cell全流程） | VS Code / Jupyter 打开即用 |
| `VideoCode/MCP终极指南-进阶篇/weather/` | MCP Server（真实天气API+日志） | `cd VideoCode/MCP终极指南-进阶篇/weather/ && uv run weather.py` |

> ⚠️ VideoCode 项目使用 `uv` 管理依赖，需先 `pip install uv`
> ⚠️ daily_exercises 在 Windows 下必须加 `PYTHONIOENCODING=utf-8`，否则 emoji 汉字报 GBK 编码错误
> ⚠️ Day08 国内需加 `HF_ENDPOINT=https://hf-mirror.com`（HuggingFace 被墙）
> Day01/03/13 为 .md 纯文档，无需运行

---

> **最后更新：** 2026年5月13日
> **主教程：** hello-agents（16章 + Extra面试答案 + Ch4代码）
> **实战补充：** VideoCode（7个项目：Agent/RAG/MCP/A2A）— 马克的技术工作坊配套代码
> **辅教程：** ai-agents-from-zero（LangChain/LangGraph API参考 + 75题题库 + 电商问数）
> **练习代码：** daily_exercises/（15个文件，12个可运行py） + VideoCode/（6个可运行项目）
