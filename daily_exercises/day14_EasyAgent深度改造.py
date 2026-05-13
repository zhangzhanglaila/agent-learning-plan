"""
Day14 (5/26) — EasyAgent 深度改造（综合实战）
================================================
任务：基于 demo2.py 进行全面升级，整合前13天学到的所有能力
     用 LangChain + LangGraph 构建一个生产级的多工具Agent

改造目标：
  1. ChatPromptTemplate 替代手动 System Prompt
  2. 添加多个工具（计算器 + 翻译 + 天气 + 知识搜索）
  3. 用 LangGraph 实现工具选择路由
  4. 添加对话记忆（RunnableWithMessageHistory）
  5. 添加错误处理和降级逻辑
"""

import os
import re
from typing import Annotated, TypedDict, Literal
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
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


# ==================== 工具层 ====================

@tool
def calculator(expression: str) -> str:
    """数学计算器。输入：数学表达式字符串，如 '100+200' 或 '(3+5)*2'"""
    try:
        expression = expression.replace("×", "*").replace("÷", "/")
        expression = re.sub(r"[^0-9+\-*/().]", "", expression)
        if not expression:
            return "错误：无效的表达式"
        return str(eval(expression))
    except Exception as e:
        return f"计算错误：{e}"


@tool
def translator(text: str, target_lang: str = "英文") -> str:
    """翻译工具。输入：text=要翻译的文本, target_lang=目标语言（默认英文）"""
    # 使用LLM做翻译（比mock更真实）
    response = llm.invoke([
        SystemMessage(content=f"将以下内容翻译成{target_lang}，只输出译文。"),
        HumanMessage(content=text),
    ])
    return response.content


@tool
def get_weather(city: str) -> str:
    """查询城市实时天气（模拟）。输入：城市名称"""
    weather_db = {
        "北京": "晴 22°C 湿度40%", "上海": "多云 25°C 湿度65%",
        "深圳": "阵雨 28°C 湿度80%", "杭州": "阴 20°C 湿度55%",
    }
    return weather_db.get(city, f"{city}：晴 20°C（模拟）")


@tool
def search_knowledge(query: str) -> str:
    """搜索专业知识库。输入：查询关键词"""
    kb = {
        "agent": "AI Agent = 大模型 + 工具集 + 运行循环 + 当前状态。核心循环：ReAct（Thought→Action→Observation）。",
        "rag": "RAG流程：索引阶段（文档→切块→向量化→存储）→检索阶段（Query→召回→重排→生成）。",
        "langgraph": "LangGraph四要素：State（状态）→Node（节点）→Edge（边）→Graph（图）。支持循环/分支/HITL。",
        "mcp": "MCP（模型上下文协议）= 统一标准连接外部工具/资源/提示。三角色：Host/Client/Server。",
    }
    for k, v in kb.items():
        if k in query.lower():
            return v
    return f"未找到关于'{query}'的知识"


# ==================== State ====================
class EnhancedAgentState(TypedDict):
    messages: Annotated[list, add_messages]
    intent: str
    retry_count: int


# ==================== 节点 ====================

# 系统提示词（用 ChatPromptTemplate 风格，直接写在这里）
SYSTEM_PROMPT = """你是一个智能助手，诚实、简洁、有帮助。

能力范围：
- 数学计算：使用 calculator 工具
- 翻译：使用 translator 工具
- 天气查询：使用 get_weather 工具
- 专业知识：使用 search_knowledge 工具

规则：
- 不编造数据（天气/知识必须靠工具获取）
- 如果工具调用失败，告知用户并建议替代方案
- 计算工具只接受纯数学表达式"""


def intent_classifier(state: EnhancedAgentState) -> dict:
    """节点1：意图识别"""
    last_msg = state["messages"][-1]
    content = last_msg.content if hasattr(last_msg, 'content') else ""

    classify_prompt = f"""分析用户意图，只回复一个词：
calculation | translation | weather | knowledge | chat

用户消息：{content}"""

    response = llm.invoke([HumanMessage(content=classify_prompt)])
    intent = response.content.strip().lower()
    print(f"  🎯 意图：{intent}")
    return {"intent": intent, "retry_count": state.get("retry_count", 0)}


def chat_response(state: EnhancedAgentState) -> dict:
    """节点2：纯对话（不需要工具）"""
    response = llm.invoke(
        [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    )
    return {"messages": [response]}


def tool_agent(state: EnhancedAgentState) -> dict:
    """节点3：工具Agent（绑定工具让模型选择调用）"""
    tools = [calculator, translator, get_weather, search_knowledge]
    llm_with_tools = llm.bind_tools(tools)

    response = llm_with_tools.invoke(
        [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    )
    print(f"  🔧 {'调用工具中' if hasattr(response, 'tool_calls') and response.tool_calls else f'直接回复：{response.content[:60]}...'}")
    return {"messages": [response]}


def error_recovery(state: EnhancedAgentState) -> dict:
    """节点4：错误恢复 —— 当工具调用过多时降级"""
    retry_count = state.get("retry_count", 0)
    print(f"  ⚠️  重试次数：{retry_count}，请求降级处理")

    response = llm.invoke(
        [SystemMessage(content="工具调用遇到问题，请直接基于你的知识回答用户，并说明你无法获取实时数据。")]
        + state["messages"]
    )
    return {"messages": [response], "retry_count": retry_count + 1}


# ==================== 路由逻辑 ====================

def route_by_intent(state: EnhancedAgentState) -> Literal["tool_agent", "chat_response"]:
    """意图 → 选择节点"""
    intent = state.get("intent", "chat")
    if intent in ("calculation", "translation", "weather", "knowledge"):
        return "tool_agent"
    return "chat_response"


def should_retry(state: EnhancedAgentState) -> Literal["error_recovery", END]:
    """检查是否需要重试/降级"""
    messages = state.get("messages", [])
    if not messages:
        return END

    last_msg = messages[-1]
    # 如果模型仍在请求工具调用（且超过2轮）→ 降级
    if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
        if state.get("retry_count", 0) >= 2:
            return "error_recovery"
    return END


# ==================== 构建图 ====================

def build_enhanced_agent():
    """构建增强版 Agent 图"""
    graph_builder = StateGraph(EnhancedAgentState)

    # 添加节点
    graph_builder.add_node("classifier", intent_classifier)
    graph_builder.add_node("tool_agent", tool_agent)
    graph_builder.add_node("chat_response", chat_response)
    graph_builder.add_node("error_recovery", error_recovery)
    # 工具执行节点
    graph_builder.add_node("tools", ToolNode([calculator, translator, get_weather, search_knowledge]))

    # 边
    graph_builder.add_edge(START, "classifier")
    graph_builder.add_conditional_edges("classifier", route_by_intent, {
        "tool_agent": "tool_agent",
        "chat_response": "chat_response",
    })

    # 工具Agent的条件边
    from langgraph.prebuilt import tools_condition
    graph_builder.add_conditional_edges("tool_agent", tools_condition, {
        "tools": "tools",
        END: END,
    })
    graph_builder.add_edge("tools", "tool_agent")  # 工具执行后回到Agent

    # 错误恢复 → 结束
    graph_builder.add_edge("error_recovery", END)
    graph_builder.add_edge("chat_response", END)

    return graph_builder.compile()


# ==================== 测试 ====================

if __name__ == "__main__":
    agent = build_enhanced_agent()

    test_cases = [
        "帮我算 (135 + 265) × 3",
        "把 'Hello, how are you?' 翻译成中文",
        "北京今天什么天气？",
        "什么是 RAG？",
        "你好，今天心情不错",
    ]

    for query in test_cases:
        print(f"\n{'='*60}")
        print(f"👤 {query}")

        result = agent.invoke({
            "messages": [HumanMessage(content=query)],
        })

        final_msg = result["messages"][-1]
        answer = final_msg.content if hasattr(final_msg, 'content') else str(final_msg)
        print(f"✅ {answer[:120]}")

    print("\n" + "=" * 60)
    print("✅ 增强版Agent完成！回顾你从 Day1 到 Day14 的进步：")
    print("  Day1-2: 手动正则提取 → Day5: @tool装饰器 → Day10: create_agent")
    print("  Day6: LCEL链 → Day7: AgentExecutor → Day11: LangGraph图")
    print("  Day8: RAG → Day9: MCP → Day12: Checkpoint/Streaming")
    print("  今天: 全部整合 → 一个生产级的多工具Agent")

"""
============================================================
📝 最终练习：
  1. 确保这个增强版Agent能正确处理5种不同意图
  2. 加入 Checkpointer，让同一个用户的多轮对话能记住上文
  3. 添加一个"工具调用计数"状态字段，超过5次调用后自动降级
  4. 准备面试话术："我做了一个多工具Agent，用LangGraph编排了
     意图识别→工具路由→工具执行→错误恢复的完整流程"
============================================================
"""
