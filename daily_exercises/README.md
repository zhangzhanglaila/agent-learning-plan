# Daily Exercises — 索引

每天一个文件，包含当日任务 + 完整答案代码（全部已通过运行验证 ✅）

## 学习材料定位

| 材料 | 角色 | 用途 |
|------|------|------|
| **hello-agents**（16章）| ⭐⭐⭐ 主教程 | 理解Agent原理 + 自建框架 + 面试答案 |
| **ai-agents-from-zero**（26章）| ⭐⭐ 辅教程 | LangChain/LangGraph API参考 + 75题题库 |
| **daily_exercises**（本目录）| ⭐ 练习代码 | 每天动手的完整可运行代码 |

## 每日练习索引

| Day | 日期 | 文件 | 主题 | 对应主教程 |
|-----|------|------|------|------------|
| 1 | 5/13 | `day01_大模型认知与EasyAgent精读.md` | Agent认知 + ReAct范式 | hello-agents Ch1-4 |
| 2 | 5/14 | `day02_多工具Agent练习.py` | 多工具调度 + 经典范式 | hello-agents Ch4-6 |
| 3 | 5/15 | `day03_Coze_Dify平台动手.md` | 低代码平台 | hello-agents Ch5 |
| 4 | 5/16 | `day04_LangChain重写Agent.py` | LangChain入门 | ai-agents-from-zero Ch9-11 |
| 5 | 5/17 | `day05_输出解析器与结构化输出.py` | 输出解析器 + @tool | ai-agents-from-zero Ch13-14 |
| 6 | 5/18 | `day06_LCEL链式调用与记忆.py` | LCEL + Memory | ai-agents-from-zero Ch15-16 |
| 7 | 5/19 | `day07_多工具Agent.py` | 自建Agent框架 ⭐ | **hello-agents Ch7** |
| 8 | 5/20 | `day08_RAG全链路实战.py` | RAG + 记忆系统 | hello-agents Ch8 |
| 9 | 5/21 | `day09_MCP协议实战.py` | MCP + 通信协议 | hello-agents Ch10 |
| 10 | 5/22 | `day10_Agent与LangGraph入门.py` | LangGraph基础 | ai-agents-from-zero Ch22-23 |
| 11 | 5/23 | `day11_LangGraph多步Agent.py` | LangGraph实战 + 上下文工程 | hello-agents Ch9 |
| 12 | 5/24 | `day12_LangGraph高级特性.py` | LangGraph高级 + Agent评估 | hello-agents Ch12 |
| 13 | 5/25 | `day13_电商问数项目剖析.md` | 综合项目剖析 | 两个教程项目 |
| 14 | 5/26 | `day14_EasyAgent深度改造.py` | 综合实战 | 全部整合 |
| — | — | `supplement_01_agent_paradigms.py` | Plan-Solve + Reflection 范式 | hello-agents Ch4 |

## 使用方式

1. **上午**：按计划阅读 hello-agents / ai-agents-from-zero 对应章节
2. **上午**：打开本目录对应日期的文件，运行代码 → 理解代码 → 改参数观察变化
3. **晚上**：对照 hello-agents `Extra01-参考答案.md` 背诵对应八股
4. **周末**：回顾标记的薄弱点，确保核心概念能脱稿复述

## 项目故事线（面试用）

```
EasyAgent (OpenAI原生API, 手写Agent循环)
  → hello-agents Ch7 (自建HelloAgents框架, 三种范式)
    → daily_exercises (LangChain/LangGraph工业级框架)
```

所有代码已通过运行验证（2026-05-13）。运行时注意：
- Windows 下加 `PYTHONIOENCODING=utf-8`（解决 emoji 编码问题）
- Day08 国内用户需设 `HF_ENDPOINT=https://hf-mirror.com`
