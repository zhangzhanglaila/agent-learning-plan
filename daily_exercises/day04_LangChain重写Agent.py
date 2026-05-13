"""
Day4 (5/16) — 用 LangChain 重写 EasyAgent
===========================================
任务：把 demo.py 和 demo2.py 中的裸 OpenAI 调用替换为 LangChain 标准写法。

学习目标：
  1. 学会 ChatPromptTemplate 构建提示词模板
  2. 掌握 StrOutputParser 的基本用法
  3. 理解 LangChain 的 Runnable 链式调用
"""

import os
import re
from dotenv import load_dotenv
from openai import OpenAI

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

load_dotenv()

# ==================== LangChain 初始化 ====================
# 用 ChatOpenAI 替代裸 OpenAI 客户端
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    temperature=0,  # 生产Agent建议低温，输出更稳定
)

# 保留原生客户端用于后续的底层调用（作为对比）
native_client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
)


# ==================== 任务1：LangChain 重写 demo.py（多轮对话）====================
def langchain_demo():
    """用 LangChain 实现多轮对话"""
    print("\n" + "=" * 60)
    print("任务1：LangChain 多轮对话")

    # LangChain 的 ChatPromptTemplate：支持模板变量 + 历史消息占位
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个友好的助手，回答简洁准确。"),
        MessagesPlaceholder(variable_name="history"),  # 历史消息插槽
        ("human", "{input}"),  # 当前用户输入
    ])

    # LCEL 链式调用：prompt | llm | parser
    chain = prompt | llm | StrOutputParser()

    # 模拟多轮对话
    history = [
        {"role": "user", "content": "1+1等于几？"},
        {"role": "assistant", "content": "等于2"},
    ]

    result = chain.invoke({
        "history": history,
        "input": "再加3等于几？"
    })
    print(f"LangChain回答：{result}")


# ==================== 任务2：LangChain 重写 demo2.py（工具调用Agent）====================
# 工具定义
def calculator(expression: str) -> str:
    try:
        expression = expression.replace("×", "*").replace("÷", "/")
        expression = re.sub(r"[^0-9+\-*/.]", "", expression)
        result = eval(expression)
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算失败：{str(e)}"


def langchain_agent_demo():
    """用 LangChain 实现工具调用Agent"""
    print("\n" + "=" * 60)
    print("任务2：LangChain 工具调用Agent")

    # System Prompt 模板
    system_template = """
你是一个严格执行规则的智能Agent。
【铁律】：只要是数学计算，只输出工具指令，格式：[calculator]表达式
例子：[calculator]12345*67890
禁止输出任何多余内容！
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", "{input}"),
    ])

    # 链：prompt → llm → 提取文本
    think_chain = prompt | llm | StrOutputParser()

    # 第一轮：模型决策
    user_input = "12345 × 67890 等于多少？"
    agent_thought = think_chain.invoke({"input": user_input})
    print(f"🤖 Agent决策：{agent_thought}")

    # 工具调度（和之前一样）
    match = re.search(r"\[calculator\](.*)", agent_thought.strip(), re.I)
    if match:
        expression = match.group(1).strip()
        tool_result = calculator(expression)
        print(f"🔧 工具结果：{tool_result}")

        # 第二轮：用 LangChain 生成最终回复
        final_prompt = ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("human", "{input}"),
            ("assistant", "{agent_thought}"),
            ("human", "工具返回结果：{tool_result}\n请用自然语言回复。"),
        ])
        final_chain = final_prompt | llm | StrOutputParser()
        final_answer = final_chain.invoke({
            "input": user_input,
            "agent_thought": agent_thought,
            "tool_result": tool_result,
        })
        print(f"✅ 最终回答：{final_answer}")


# ==================== 任务3：对比原生 vs LangChain ====================
def compare():
    """对比原生调用和 LangChain 调用的写法差异"""
    print("\n" + "=" * 60)
    print("任务3：原生 vs LangChain 对比")

    question = "什么是Agent？请一句话回答。"

    # 原生方式（EasyAgent风格）
    native_response = native_client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": question}],
    )
    native_answer = native_response.choices[0].message.content

    # LangChain 方式
    lc_prompt = ChatPromptTemplate.from_messages([
        ("human", "{input}"),
    ])
    lc_chain = lc_prompt | llm | StrOutputParser()
    lc_answer = lc_chain.invoke({"input": question})

    print(f"原生方式：{native_answer}")
    print(f"LC方式：  {lc_answer}")
    print("\n区别：")
    print("  原生：手动管理messages列表、手动调用API、手动提取content")
    print("  LC：  声明式定义Prompt模板 → 链式组合 → invoke即可")
    print("  LC优势：模板可复用、组件可替换(换模型/换parser不改链结构)")


if __name__ == "__main__":
    langchain_demo()
    langchain_agent_demo()
    compare()

"""
============================================================
📝 练习任务：
  1. 运行上述代码，确认三个任务都能正常输出
  2. 修改 system_template，添加第二个工具 [string] 的规则
  3. 在 langchain_agent_demo 中扩展 dispatch 逻辑，支持双工具
  4. 尝试使用 .stream() 替代 .invoke()，观察流式输出效果

💡 关键理解：
  - ChatPromptTemplate.from_messages() 可以混合 "system"/"human"/"assistant" 角色
  - MessagesPlaceholder 用于动态插入历史消息
  - | 运算符连接 Runnable，形成处理链
  - StrOutputParser 从 AIMessage 中提取纯文本 content
============================================================
"""
