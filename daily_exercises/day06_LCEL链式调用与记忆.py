"""
Day6 (5/18) — LCEL 链式调用 + 对话记忆
========================================
任务：
  1. 用 LCEL 搭建多条链：顺序链、分支链、并行链
  2. 用 RunnableWithMessageHistory 实现带记忆的多轮对话Agent

学习目标：
  1. 掌握 Runnable 四种组合方式
  2. 理解 Memory 在 Agent 中的角色（短期记忆 vs 长期记忆）
"""

import os
from typing import Dict
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableParallel,
    RunnableBranch,
    RunnableLambda,
)
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    temperature=0,
)


# ==================== 任务1：LCEL 链的四种组合方式 ====================

def demo_sequential_chain():
    """顺序链：A → B → C，数据单向流动"""
    print("\n" + "=" * 60)
    print("1. 顺序链 (Sequential)")

    # 翻译链
    translate_prompt = ChatPromptTemplate.from_template(
        "把以下内容翻译成英文：{text}"
    )
    # 摘要链
    summarize_prompt = ChatPromptTemplate.from_template(
        "用一句话概括以下英文内容：{text}"
    )

    # 组合：翻译 → 摘要
    chain = (
        translate_prompt | llm | StrOutputParser()
        | (lambda en_text: {"text": en_text})  # 把输出包装成dict
        | summarize_prompt | llm | StrOutputParser()
    )

    result = chain.invoke({"text": "人工智能正在改变我们与世界互动的方式"})
    print(f"原文 → 翻译 → 摘要：\n{result}")


def demo_branch_chain():
    """分支链：根据条件走不同处理路径"""
    print("\n" + "=" * 60)
    print("2. 分支链 (Branch)")

    # 正面回复
    positive_prompt = ChatPromptTemplate.from_template(
        "用户的评论很积极：{input}，请热情感谢用户。"
    )
    # 负面回复
    negative_prompt = ChatPromptTemplate.from_template(
        "用户的评论很消极：{input}，请礼貌道歉并提供帮助。"
    )

    branch = RunnableBranch(
        # 条件函数, 对应链
        (lambda x: "好" in x["input"] or "棒" in x["input"],
         positive_prompt | llm | StrOutputParser()),
        # 默认链
        negative_prompt | llm | StrOutputParser(),
    )

    print("正面输入：", branch.invoke({"input": "这个产品太棒了！"}))
    print("负面输入：", branch.invoke({"input": "质量很差，很失望"}))


def demo_parallel_chain():
    """并行链：同一输入同时走多条处理路径"""
    print("\n" + "=" * 60)
    print("3. 并行链 (Parallel)")

    # 同时做翻译和摘要
    translate_prompt = ChatPromptTemplate.from_template(
        "把以下内容翻译成英文（只输出译文）：{text}"
    )
    summarize_prompt = ChatPromptTemplate.from_template(
        "用不超过10个字概括：{text}"
    )

    parallel = RunnableParallel(
        translation=translate_prompt | llm | StrOutputParser(),
        summary=summarize_prompt | llm | StrOutputParser(),
    )

    result = parallel.invoke({
        "text": "人工智能技术近年来发展迅速，深度学习模型在自然语言处理、计算机视觉等领域取得了突破性进展。"
    })
    print(f"英文翻译：{result['translation']}")
    print(f"中文摘要：{result['summary']}")


# ==================== 任务2：带记忆的多轮对话Agent ====================

# 内存中的会话存储（生产环境换成Redis）
store: Dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """根据session_id获取对话历史"""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


def demo_memory_agent():
    """带记忆的对话Agent：记住之前的对话"""
    print("\n" + "=" * 60)
    print("4. 带记忆的多轮对话")

    system_prompt = """你是一个友好的助手，回答简洁。当前时间是2026年5月。"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),  # ← 历史消息插在这里
        ("human", "{input}"),
    ])

    chain = prompt | llm | StrOutputParser()

    # 包装记忆能力
    agent_with_memory = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",       # 哪个参数是用户输入
        history_messages_key="history",   # 哪个参数是历史消息
    )

    # 模拟多轮对话
    session_id = "user-001"

    print("第1轮：", agent_with_memory.invoke(
        {"input": "我叫小明，我在学Python"},
        config={"configurable": {"session_id": session_id}}
    ))

    print("第2轮：", agent_with_memory.invoke(
        {"input": "我之前说我在学什么？"},
        config={"configurable": {"session_id": session_id}}
    ))

    print("第3轮：", agent_with_memory.invoke(
        {"input": "我叫什么名字？"},
        config={"configurable": {"session_id": session_id}}
    ))

    # 查看内部存储的消息历史
    print(f"\n内部存储的消息数：{len(store[session_id].messages)}")
    for msg in store[session_id].messages:
        print(f"  [{msg.type}] {msg.content[:50]}...")


if __name__ == "__main__":
    demo_sequential_chain()
    demo_branch_chain()
    demo_parallel_chain()
    demo_memory_agent()

"""
============================================================
📝 练习任务：
  1. 运行所有示例，观察四种链的输出
  2. 改造 demo_parallel_chain，增加第三条并行链路（如：情感分析）
  3. 修改 demo_memory_agent，用新的 session_id 重新对话，观察记忆是否隔离
  4. 尝试实现"摘要记忆"：当历史消息超过10条时，自动用LLM生成摘要压缩

💡 关键理解：
  - LCEL 核心是 | 运算符：上游输出 → 下游输入
  - RunnableBranch 就是 if/elif/else 的声明式写法
  - RunnableWithMessageHistory 自动管理消息的增删查
  - session_id 实现多用户隔离，生产用 Redis 替代 InMemory
============================================================
"""
