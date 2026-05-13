"""
Day12 (5/24) — LangGraph 高级特性：Checkpoint + Streaming + 子图
==================================================================
任务：
  1. 实现带 Checkpointer 的 Agent（断点续跑+对话持久化）
  2. 实现流式输出（四种 stream_mode）
  3. 理解 Time-Travel 和 HITL 的工程价值

学习目标：
  1. 掌握 Checkpoint 的三个价值：可恢复、可复盘、可中断
  2. 掌握四种 stream_mode 的用途
  3. 能回答面试中关于 LangGraph 高级特性的问题
"""

import os
from typing import Annotated, TypedDict
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

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
    """两数相乘"""
    return str(a * b)


@tool
def add(a: float, b: float) -> str:
    """两数相加"""
    return str(a + b)


@tool
def subtract(a: float, b: float) -> str:
    """两数相减"""
    return str(a - b)


# ==================== State ====================
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# ==================== 任务1：Checkpoint 持久化 ====================

def demo_checkpointer():
    """演示 Checkpoint 的断点续跑能力"""
    print("=" * 60)
    print("任务1：Checkpoint 持久化演示")

    tools = [multiply, add, subtract]

    # 构建图（和之前一样）
    llm_with_tools = llm.bind_tools(tools)

    def chatbot(state: AgentState):
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    graph_builder = StateGraph(AgentState)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_node("tools", ToolNode(tools))
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_conditional_edges("chatbot", tools_condition)
    graph_builder.add_edge("tools", "chatbot")

    # ⭐ 关键：创建 MemorySaver 作为 Checkpointer
    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)

    # 同一个 thread_id 的多次 invoke 共享状态
    config = {"configurable": {"thread_id": "user-abc-001"}}

    # 第一轮对话
    print("\n第1轮：计算 10+5")
    result = graph.invoke(
        {"messages": [HumanMessage(content="计算 10+5")]},
        config=config,
    )
    print(f"  回答：{result['messages'][-1].content}")

    # 第二轮对话：使用相同的 thread_id，"还记得"上一轮
    print("\n第2轮：把刚才的结果乘以3")
    result = graph.invoke(
        {"messages": [HumanMessage(content="把刚才的结果乘以3")]},
        config=config,
    )
    print(f"  回答：{result['messages'][-1].content}")

    # 查看 Checkpoint 中保存的状态
    checkpoint = memory.get(config)
    if checkpoint:
        msg_count = len(checkpoint["channel_values"]["messages"])
        print(f"\n  📦 Checkpoint 中保存了 {msg_count} 条消息")

    print("""
  Checkpoint 的三个工程价值：
  1. 可恢复  — 长任务/断点续跑/失败重放
  2. 可复盘  — Time-Travel：回退到任意历史节点重新执行
  3. 可控制  — HITL：在关键动作前暂停，等待人工确认
""")


# ==================== 任务2：流式输出（Streaming）====================

def demo_streaming():
    """演示 LangGraph 的四种 stream_mode"""
    print("\n" + "=" * 60)
    print("任务2：流式输出演示")

    tools = [add, multiply]
    llm_with_tools = llm.bind_tools(tools)

    def chatbot(state: AgentState):
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    graph_builder = StateGraph(AgentState)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_node("tools", ToolNode(tools))
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_conditional_edges("chatbot", tools_condition)
    graph_builder.add_edge("tools", "chatbot")
    graph = graph_builder.compile()

    print("""
  四种 stream_mode：
  ┌──────────────┬──────────────────────────────────────────┐
  │ values       │ 每个节点执行完后的完整 State（最常用）    │
  │ updates      │ 每个节点返回的增量更新                    │
  │ messages     │ 流式Token + 元数据（实现打字机效果）      │
  │ custom       │ 节点内手动 yield 的自定义数据             │
  └──────────────┴──────────────────────────────────────────┘
""")

    # 演示 values 模式
    print("stream_mode='values'（观察State变化）：")
    for i, chunk in enumerate(graph.stream(
        {"messages": [HumanMessage(content="计算 6×7")]},
        stream_mode="values",
    )):
        msg_count = len(chunk.get("messages", []))
        last_msg = chunk["messages"][-1] if chunk["messages"] else "空"
        print(f"  Step {i}: {msg_count}条消息, 最新=[{last_msg.__class__.__name__}]")

    # 演示 updates 模式
    print("\nstream_mode='updates'（观察增量变化）：")
    for i, chunk in enumerate(graph.stream(
        {"messages": [HumanMessage(content="计算 6×7")]},
        stream_mode="updates",
    )):
        print(f"  Step {i}: {list(chunk.keys())}")


# ==================== 任务3：HITL 模拟（人工介入）====================

def demo_hitl_concept():
    """演示 HITL 的概念（不运行真实打断，仅讲清楚设计）"""
    print("\n" + "=" * 60)
    print("任务3：HITL 人工介入模式")

    print("""
  HITL（Human-In-The-Loop）设计模式：

  # 在关键节点前加 interrupt
  graph_builder.compile(
      checkpointer=memory,
      interrupt_before=["execute_payment"],  # ← 执行前暂停
  )

  # 人工审核通过后继续
  graph.invoke(None, config)  # None = 无新输入，从Checkpoint继续

  典型使用场景：
  - 支付操作前 → 人工确认金额
  - 删改数据前 → 人工审核影响范围
  - 对外发送前 → 人工审核内容

  面试表达：
  "Checkpoint 负责可恢复，HITL 负责可控制。
   支付/删改/发送前把图暂停，
   人工审核通过后从Checkpoint继续执行。"
""")


if __name__ == "__main__":
    demo_checkpointer()
    demo_streaming()
    demo_hitl_concept()

"""
============================================================
📝 练习任务：
  1. 运行 demo_checkpointer，确认第二轮对话"记得"第一轮的结果
  2. 用新的 thread_id 重新对话，观察记忆是否隔离
  3. 把 demo_streaming 中的 stream_mode 逐个改成 "updates"/"messages"
     观察输出差异
  4. 尝试手动实现一个 HITL 流程（在某个节点前暂停 + 手动继续）

💡 面试常见问题：
  Q: "Checkpoint 怎么用？"
  A: compile(checkpointer=MemorySaver())，同一 thread_id 共享状态

  Q: "stream_mode 怎么选？"
  A: values 看全貌，updates 看增量，messages 做打字机效果
============================================================
"""
