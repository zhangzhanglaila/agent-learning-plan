"""
Day11 (5/23) — LangGraph 多步 Agent 实战
==========================================
任务：用 LangGraph 构建一个多步推理 Agent
     意图识别 → 检索 → 工具调用 → 生成 → 条件判断

学习目标：
  1. 掌握 State 设计、Node 粒度、条件边的实践
  2. 能画出完整的图结构
  3. 能回答面试中关于 LangGraph 的问题
"""

import os
from typing import Annotated, TypedDict, Literal
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

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
    """计算数学表达式"""
    import re
    try:
        expression = re.sub(r"[^0-9+\-*/().]", "", expression)
        return str(eval(expression))
    except Exception as e:
        return f"计算错误：{e}"


@tool
def search_knowledge(query: str) -> str:
    """搜索内部知识库"""
    kb = {
        "langgraph": "LangGraph是有向图状态机框架，核心：State/Node/Edge/Graph。适合有分支、循环、人工介入的复杂Agent。",
        "react": "ReAct模式 = Thought(思考) → Action(行动) → Observation(观察) 循环。让模型在推理和行动之间交替。",
    }
    for k, v in kb.items():
        if k in query.lower():
            return v
    return f"未找到'{query}'的相关知识"


# ==================== State 设计 ====================
class AgentState(TypedDict):
    """Agent 的共享状态"""
    messages: Annotated[list, add_messages]  # 完整对话 + tool_calls
    intent: str                              # 意图分类
    search_results: str                      # 检索结果
    confidence: float                        # 置信度 0-1
    final_answer: str                        # 最终回答


# ==================== 节点定义 ====================

def classify_intent(state: AgentState) -> dict:
    """节点1：意图识别 —— 判断用户想做什么"""
    last_msg = state["messages"][-1]

    classify_prompt = f"""分析以下用户消息的意图，只能回复以下之一：
- calculation：数学计算
- knowledge：查询专业知识
- chat：闲聊

用户消息：{last_msg.content}

只回复一个单词。"""

    response = llm.invoke([HumanMessage(content=classify_prompt)])
    intent = response.content.strip().lower()
    print(f"  🎯 意图识别：{intent}")
    return {"intent": intent}


def route_by_intent(state: AgentState) -> Literal["calculator", "knowledge_search", "chat_response"]:
    """条件边：根据意图路由到不同节点"""
    intent = state.get("intent", "chat")
    if intent == "calculation":
        return "calculator"
    elif intent == "knowledge":
        return "knowledge_search"
    else:
        return "chat_response"


def calculator_node(state: AgentState) -> dict:
    """节点2a：计算器节点 —— 绑定计算工具，让模型调用"""
    llm_with_calc = llm.bind_tools([calculator])
    response = llm_with_calc.invoke(
        [SystemMessage(content="你是计算助手。用 calculator 工具计算。")]
        + state["messages"]
    )
    print(f"  🔢 计算节点：{response.content if response.content else '(调用工具中...)'}")
    return {"messages": [response]}


def knowledge_search_node(state: AgentState) -> dict:
    """节点2b：知识搜索节点 —— 检索+生成"""
    last_msg = state["messages"][-1]
    kb_result = search_knowledge.invoke({"query": last_msg.content})
    print(f"  📚 检索结果：{kb_result[:80]}...")

    response = llm.invoke([
        SystemMessage(content=f"根据以下资料回答用户问题。\n资料：{kb_result}"),
        HumanMessage(content=last_msg.content),
    ])
    print(f"  📚 生成回答：{response.content[:80]}...")
    return {"search_results": kb_result, "messages": [response]}


def chat_response_node(state: AgentState) -> dict:
    """节点2c：闲聊节点 —— 直接回复"""
    response = llm.invoke(
        [SystemMessage(content="你是友好的助手。")]
        + state["messages"]
    )
    print(f"  💬 闲聊回复：{response.content[:80]}...")
    return {"messages": [response]}


def evaluate_confidence(state: AgentState) -> dict:
    """节点3：置信度评估 —— 判断回答是否足够好"""
    last_msg = state["messages"][-1]
    if not last_msg.content:
        return {"confidence": 1.0}

    eval_prompt = f"""评估以下AI回答的置信度（0-1之间的小数）。
0分=完全胡说，1分=非常确定正确。

AI回答：{last_msg.content}

只回复一个数字（如：0.95）。"""

    response = llm.invoke([HumanMessage(content=eval_prompt)])
    try:
        confidence = float(response.content.strip())
    except ValueError:
        confidence = 0.5
    print(f"  📊 置信度：{confidence}")
    return {"confidence": confidence}


def should_retry(state: AgentState) -> Literal["chat_response", END]:
    """条件边：置信度低则重新回答"""
    if state.get("confidence", 1.0) < 0.7:
        print("  ⚠️  置信度过低，重试...")
        return "chat_response"
    return END


# ==================== 构建图 ====================
def build_graph():
    """构建多步 Agent 图"""
    graph_builder = StateGraph(AgentState)

    # 添加节点
    graph_builder.add_node("classify_intent", classify_intent)
    graph_builder.add_node("calculator", calculator_node)
    graph_builder.add_node("knowledge_search", knowledge_search_node)
    graph_builder.add_node("chat_response", chat_response_node)
    graph_builder.add_node("evaluate", evaluate_confidence)

    # 工具节点（处理 tool_calls）
    graph_builder.add_node("calc_tools", ToolNode([calculator]))

    # 入口
    graph_builder.add_edge(START, "classify_intent")

    # 意图路由 → 三个分支
    graph_builder.add_conditional_edges("classify_intent", route_by_intent, {
        "calculator": "calculator",
        "knowledge_search": "knowledge_search",
        "chat_response": "chat_response",
    })

    # 计算器分支：模型可能调用工具
    from langgraph.prebuilt import tools_condition
    graph_builder.add_conditional_edges("calculator", tools_condition, {
        "tools": "calc_tools",
        END: "evaluate",
    })
    graph_builder.add_edge("calc_tools", "calculator")  # 工具执行后回到计算器

    # 知识搜索/闲聊 → 评估
    graph_builder.add_edge("knowledge_search", "evaluate")
    graph_builder.add_edge("chat_response", "evaluate")

    # 评估 → 重试或结束
    graph_builder.add_conditional_edges("evaluate", should_retry, {
        "chat_response": "chat_response",
        END: END,
    })

    return graph_builder.compile()


# ==================== 测试 ====================
if __name__ == "__main__":
    graph = build_graph()

    print("图结构：")
    print("  START → classify_intent")
    print("    ├─ calculation → calculator ⇄ calc_tools → evaluate")
    print("    ├─ knowledge → knowledge_search → evaluate")
    print("    └─ chat → chat_response → evaluate")
    print("  evaluate → [置信度<0.7?] → chat_response (重试)")
    print("           → [置信度≥0.7?] → END")

    test_queries = [
        "帮我算 156×23+47",
        "什么是 LangGraph？",
        "今天心情不错",
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"👤 用户：{query}")

        result = graph.invoke({
            "messages": [HumanMessage(content=query)],
        })

        final_msg = result["messages"][-1]
        print(f"✅ 最终回答：{final_msg.content[:100]}...")
        print(f"  意图：{result.get('intent', 'N/A')}")
        print(f"  置信度：{result.get('confidence', 'N/A')}")

"""
============================================================
📝 练习任务：
  1. 运行代码，观察不同输入的图执行路径
  2. 添加第四个意图分支 "translation"（翻译意图 → 翻译节点）
  3. 修改置信度阈值从0.7改为0.5，观察重试逻辑变化
  4. 画出这个图的完整结构（用纸和笔或ASCII）

💡 面试常见问题准备：
  Q: "你用过 LangGraph 吗？画一下你的图结构"
  A: 画出上面的图，解释每个节点的职责和边的条件

  Q: "什么时候用 LangGraph 而不是简单的 Workflow？"
  A: 当流程有分支、循环、需要状态持久化/恢复、人工介入时

  Q: "State 怎么设计的？"
  A: TypedDict + Annotated[list, add_messages] reducer模式
============================================================
"""
