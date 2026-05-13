"""
Day10 (5/22) — Agent + LangGraph 快速入门
==========================================
任务：
  1. 用 create_agent 构建现代化 Agent
  2. 用 LangGraph 写第一个 HelloWorld 图
  3. 对比 AgentExecutor vs create_agent vs LangGraph

学习目标：
  1. 理解 create_agent 的简化和便利
  2. 掌握 LangGraph 的 State-Node-Edge-Graph 四要素
"""

import os
from typing import Annotated, TypedDict
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

# LangGraph 核心
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    temperature=0,
)


# ==================== 工具 ====================
@tool
def multiply(a: float, b: float) -> str:
    """将两个数相乘"""
    return str(a * b)


@tool
def add(a: float, b: float) -> str:
    """将两个数相加"""
    return str(a + b)


# ==================== 任务1：create_agent（LangChain 1.x 推荐方式）====================
def demo_create_agent():
    """create_agent：一行创建Agent，底层由 LangGraph 驱动"""
    print("=" * 60)
    print("任务1：create_agent（现代化写法）")

    agent = create_agent(
        model=llm,
        tools=[multiply, add],
        system_prompt="你是一个数学助手，用工具计算。回答简洁。",
    )

    result = agent.invoke({
        "messages": [HumanMessage(content="先算3×4，再加上2，结果是多少？")]
    })

    # 打印完整消息流（可以看到 tool_calls 和 tool 结果）
    print("Agent消息流：")
    for msg in result["messages"]:
        print(f"  [{msg.__class__.__name__}] {msg.content[:100] if hasattr(msg, 'content') and msg.content else '(无内容)'}")
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tc in msg.tool_calls:
                print(f"    → 调用工具：{tc['name']}({tc['args']})")


# ==================== 任务2：LangGraph HelloWorld ====================

# 定义 State（共享状态）
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # add_messages 是 reducer：新消息追加到列表


def demo_langgraph_hello():
    """LangGraph 最小构建：模型节点 + 工具节点 + 条件边"""
    print("\n" + "=" * 60)
    print("任务2：LangGraph HelloWorld")

    tools = [multiply, add]

    # 绑定工具到模型（让模型知道有哪些工具可用）
    llm_with_tools = llm.bind_tools(tools)

    # 节点1：调用模型
    def chatbot(state: AgentState):
        """模型节点：接收消息，返回AI回复（可能包含 tool_calls）"""
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    # 节点2：执行工具（LangGraph 内置）
    tool_node = ToolNode(tools=tools)

    # 构建图
    graph_builder = StateGraph(AgentState)

    graph_builder.add_node("chatbot", chatbot)    # 添加模型节点
    graph_builder.add_node("tools", tool_node)     # 添加工具节点

    graph_builder.add_edge(START, "chatbot")       # 入口 → 模型
    # 条件边：如果模型返回 tool_calls → 去 tools，否则 → END
    graph_builder.add_conditional_edges("chatbot", tools_condition)
    graph_builder.add_edge("tools", "chatbot")     # 工具执行完 → 回到模型

    graph = graph_builder.compile()

    # 可视化图结构（文本版）
    print("图结构：")
    print("  START → chatbot")
    print("  chatbot → [有tool_calls?] → tools → chatbot")
    print("           [无tool_calls?] → END")

    # 运行
    result = graph.invoke({
        "messages": [HumanMessage(content="计算 (3+5) × 2")]
    })

    print(f"\n对话轮数：{len(result['messages'])} 条消息")
    print(f"最终回答：{result['messages'][-1].content}")


# ==================== 任务3：三种方式对比 ====================
def compare_approaches():
    """对比 AgentExecutor vs create_agent vs LangGraph"""
    print("\n" + "=" * 60)
    print("任务3：三种 Agent 构建方式对比")

    print("""
┌────────────────┬──────────────────┬──────────────────────────────────┐
│ 方式           │ 代码量           │ 适用场景                         │
├────────────────┼──────────────────┼──────────────────────────────────┤
│ AgentExecutor  │ 多（手动组装）   │ 老项目，需要精细控制Agent循环    │
│ (classic)      │ prompt+agent+    │                                  │
│                │ executor         │                                  │
├────────────────┼──────────────────┼──────────────────────────────────┤
│ create_agent   │ 少（一行创建）   │ 新项目，快速开发                 │
│ (1.x 推荐)     │ 底层是LangGraph  │ 底层自动用LangGraph驱动           │
├────────────────┼──────────────────┼──────────────────────────────────┤
│ LangGraph      │ 中（显式建图）   │ 复杂流程，需要分支/循环/人工介入  │
│ (图状态机)     │ State+Node+Edge  │ 完全掌控流程的每一步              │
└────────────────┴──────────────────┴──────────────────────────────────┘
""")


if __name__ == "__main__":
    demo_create_agent()
    demo_langgraph_hello()
    compare_approaches()

"""
============================================================
📝 练习任务：
  1. 运行代码，观察 create_agent 内部的消息流（tool_calls → tool 结果 → 最终回复）
  2. 修改 LangGraph 例子，添加第三个节点（如：结果润色节点）
  3. 在 LangGraph 图中故意制造一个工具调用失败的情况，观察会发生什么

💡 关键理解：
  create_agent vs AgentExecutor：
    - create_agent 更简洁，底层基于 LangGraph
    - AgentExecutor 是经典路线，需要手动组装
    - 新项目优先 create_agent

  LangGraph 四要素：
    State  → 共享状态（TypedDict + reducer）
    Node   → 处理逻辑（函数/可调用对象）
    Edge   → 流转规则（固定边/条件边）
    Graph  → 编译后执行

  tools_condition：
    LangGraph 内置的条件判断函数
    检查最后一条消息是否包含 tool_calls
    有 → 路由到 "tools"，没有 → 路由到 END
============================================================
"""
