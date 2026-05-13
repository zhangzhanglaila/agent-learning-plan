"""
Day7 (5/19) — 多工具 Agent（create_tool_calling_agent）
========================================================
任务：用 LangChain 的 create_tool_calling_agent + AgentExecutor
     构建一个生产级的多工具Agent。

学习目标：
  1. 理解 Function Calling 的完整链路
  2. 掌握 AgentExecutor 的循环机制
  3. 学会设计工具和 System Prompt
"""

import os
import re
import json
from typing import Optional
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    temperature=0,
)


# ==================== 工具定义 ====================

@tool
def calculator(expression: str) -> str:
    """数学计算器，支持加减乘除和括号。
    输入示例：'100+200*3' 或 '(100+200)*3'
    注意：只接受纯数学表达式，不接受文字描述"""
    try:
        expression = expression.replace("×", "*").replace("÷", "/")
        expression = expression.replace("＋", "+").replace("－", "-")
        expression = re.sub(r"[^0-9+\-*/().]", "", expression)
        if not expression:
            return "错误：请输入有效的数学表达式"
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"计算错误：{str(e)}"


@tool
def get_weather(city: str) -> str:
    """查询指定城市的实时天气（模拟）。
    输入：城市名称，如'北京'、'上海'"""
    weather_db = {
        "北京": "晴，22°C，湿度40%，风力2级",
        "上海": "多云，25°C，湿度65%，风力3级",
        "深圳": "阵雨，28°C，湿度80%，风力4级",
        "杭州": "阴，20°C，湿度55%，风力2级",
    }
    return weather_db.get(city, f"{city}：晴，20°C（模拟数据）")


@tool
def search_knowledge(query: str) -> str:
    """搜索内部知识库（模拟），用于回答专业问题。
    输入：搜索关键词或问题"""
    knowledge = {
        "agent": "AI Agent = 大模型 + 工具集 + 运行循环 + 当前状态。它能自主规划、调用工具、根据反馈调整策略。",
        "rag": "RAG（检索增强生成）= 从外部知识库检索相关文档，将文档片段注入Prompt，让模型基于证据回答。",
        "langchain": "LangChain 是 LLM 应用开发框架，提供 Prompt/Model/Parser/Retriever/Tools/Agents 六大模块。",
        "langgraph": "LangGraph 是基于有向图的状态机框架，用 State/Node/Edge 建模复杂的 Agent 工作流。",
    }
    for key, value in knowledge.items():
        if key in query.lower():
            return value
    return f"未找到关于'{query}'的知识条目。已知主题：{', '.join(knowledge.keys())}"


# ==================== 构建 Agent ====================

def build_agent():
    """构建带多工具的 Agent（LangChain 1.x 推荐方式）"""
    tools = [calculator, get_weather, search_knowledge]

    system_prompt = """你是一个智能助手，可以调用工具来完成用户的任务。

你可以使用的工具：
- calculator：进行数学计算
- get_weather：查询城市天气
- search_knowledge：搜索专业知识

回答规则：
- 先思考用户意图，选择合适的工具
- 如果需要真实数据（天气/知识），必须调用工具
- 计算结果要准确
- 回答简洁友好"""

    # create_agent：一行创建，底层由 LangGraph 驱动
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )
    return agent


# ==================== 测试 ====================

if __name__ == "__main__":
    agent = build_agent()

    test_queries = [
        "北京今天天气怎么样？",
        "帮我算一下 (135 + 265) × 3 ÷ 2",
        "什么是 RAG？请用知识库帮我查一下",
        "上海天气怎么样？然后帮我算一下气温如果升高5度是多少度",
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"👤 用户：{query}")
        # create_agent 使用 {"messages": [...]} 格式
        result = agent.invoke({
            "messages": [HumanMessage(content=query)],
        })
        # 提取最后一条AI消息
        final_msg = result["messages"][-1]
        print(f"✅ 回答：{final_msg.content}")

"""
============================================================
📝 练习任务：
  1. 运行代码，观察 Agent 自动选择工具的过程
  2. 添加一个新工具（如：time_tool 返回当前时间）
  3. 测试当用户问"天气+计算"组合问题时，Agent是否能正确多步调用
  4. 尝试用 agent.stream() 替代 agent.invoke()，观察流式输出

💡 关键理解：
  - create_agent（LangChain 1.x）一行创建Agent，底层由 LangGraph 驱动
  - 输入格式：{"messages": [HumanMessage(content=...)]}
  - 输出格式：{"messages": [...]}, 最后一条是最终回答
  - 中间消息包含 tool_calls 和 ToolMessage（工具执行结果）

🔗 Function Calling 链路回顾（面试重点）：
  宿主发 tool schema → 模型返回 tool_calls → 宿主执行函数
  → 结果封成 ToolMessage 交回模型 → 模型生成最终答复
============================================================
"""
