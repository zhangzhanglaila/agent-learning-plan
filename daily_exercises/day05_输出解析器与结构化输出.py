"""
Day5 (5/17) — 输出解析器 + LangChain Tool 装饰器
==================================================
任务：
  1. 用 PydanticOutputParser 实现结构化信息提取
  2. 用 LangChain @tool 装饰器替代手动正则提取
  3. 对比 JSON+Parser vs 原生 Structured Output 的稳定性

学习目标：
  1. 掌握三种结构化输出方式，理解各自的适用场景
  2. 学会用 @tool 装饰器定义 LangChain 工具
"""

import os
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import (
    StrOutputParser,
    JsonOutputParser,
    PydanticOutputParser,
)
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    temperature=0,
)


# ==================== 任务1：三种结构化输出方式对比 ====================

# --- 方式1：纯 Prompt 约束（最不稳定）---
def approach1_prompt_only():
    """靠 Prompt 让模型输出 JSON —— 可能输出多余文字"""
    prompt = ChatPromptTemplate.from_messages([
        ("human", """从以下文本中提取姓名、年龄、城市，以JSON格式输出。

文本：张三，28岁，住在北京。

请严格输出JSON，不要加任何解释：""")
    ])
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({})
    print(f"纯Prompt方式：\n{result}")
    print("  问题：可能输出 ```json ... ``` 或额外解释文字\n")


# --- 方式2：JsonOutputParser（模型输出后解析）---
def approach2_json_parser():
    """JsonOutputParser：先让模型输出，再尝试解析为JSON"""
    parser = JsonOutputParser()
    prompt = ChatPromptTemplate.from_messages([
        ("human", """从以下文本中提取姓名、年龄、城市。

文本：张三，28岁，住在北京。

{format_instructions}""")
    ])
    # 注入格式化指令
    prompt = prompt.partial(format_instructions=parser.get_format_instructions())
    chain = prompt | llm | parser  # parser 自动解析 JSON
    result = chain.invoke({})
    print(f"JsonOutputParser方式：\n{result}")
    print("  优势：自动解析为Python dict")
    print("  劣势：模型仍可能不遵循JSON格式\n")


# --- 方式3：PydanticOutputParser（最强约束）---
class Person(BaseModel):
    name: str = Field(description="人物姓名")
    age: int = Field(description="年龄")
    city: str = Field(description="所在城市")


def approach3_pydantic_parser():
    """PydanticOutputParser：定义Schema，模型填充字段"""
    parser = PydanticOutputParser(pydantic_object=Person)
    prompt = ChatPromptTemplate.from_messages([
        ("human", """从以下文本中提取人物信息。

文本：张三，28岁，住在北京。

{format_instructions}""")
    ])
    prompt = prompt.partial(format_instructions=parser.get_format_instructions())
    chain = prompt | llm | parser
    result: Person = chain.invoke({})
    print(f"PydanticOutputParser方式：\n{result}")
    print(f"  类型：{type(result)}")
    print(f"  字段校验：name={result.name}, age={result.age}, city={result.city}")
    print("  优势：类型安全 + Pydantic自动校验\n")


# --- 方式4：原生 Structured Output（最推荐）---
def approach4_structured_output():
    """with_structured_output：模型原生结构化输出（需要模型支持response_format）"""
    try:
        structured_llm = llm.with_structured_output(Person)
        result: Person = structured_llm.invoke(
            "张三，28岁，住在北京。请提取人物信息。"
        )
        print(f"原生Structured Output方式：\n{result}")
        print("  优势：模型层面约束，无需Parser")
    except Exception as e:
        print(f"原生Structured Output方式：")
        print(f"  当前模型不支持 response_format（如DeepSeek），回退到 PydanticOutputParser")
        print(f"  错误信息：{e}")
    print()


# ==================== 任务2：用 LangChain @tool 替代手动正则 ====================

@tool
def calculator(expression: str) -> str:
    """数学计算器，支持加减乘除。输入：数学表达式字符串"""
    try:
        expression = expression.replace("×", "*").replace("÷", "/")
        import re
        expression = re.sub(r"[^0-9+\-*/.]", "", expression)
        result = eval(expression)
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算失败：{str(e)}"


@tool
def weather(city: str) -> str:
    """查询城市天气（模拟）。输入：城市名称"""
    import random
    temps = {"北京": "22°C 晴", "上海": "25°C 多云", "深圳": "28°C 阵雨"}
    return temps.get(city, f"{city}：{random.randint(15, 30)}°C 晴")


@tool
def text_reverse(text: str) -> str:
    """反转字符串。输入：要反转的文本"""
    return text[::-1]


def demo_tool_decorator():
    """演示 @tool 装饰器的便利性"""
    print("=" * 60)
    print("LangChain @tool 装饰器演示")

    tools = [calculator, weather, text_reverse]

    for t in tools:
        print(f"\n工具名：{t.name}")
        print(f"  描述：{t.description}")
        print(f"  参数Schema：{t.args}")

    # 直接调用
    print(f"\n直接调用 calculator：{calculator.invoke({'expression': '100+200'})}")
    print(f"直接调用 weather：{weather.invoke({'city': '北京'})}")

    print("\n@tool vs 手动正则的对比：")
    print("  手动正则：写正则 → 提取参数 → 手动调函数 → 手动拼接结果")
    print("  @tool：    定义函数 + 加装饰器 → LangChain自动管理schema/描述/调用")


# ==================== 运行 ====================
if __name__ == "__main__":
    approach1_prompt_only()
    approach2_json_parser()
    approach3_pydantic_parser()
    approach4_structured_output()
    demo_tool_decorator()

"""
============================================================
📝 练习任务：
  1. 运行代码，对比四种结构化输出方式的输出差异
  2. 自定义一个新 Pydantic 模型（如：Book 包含 title/author/year）
  3. 用 PydanticOutputParser 测试提取书名和作者
  4. 添加新的 @tool（如：翻译工具），观察 args_schema 的自动生成

💡 关键理解：
  - 生产优先级：原生 Structured Output > Pydantic Schema > JSON+Parser > 纯Prompt
  - @tool 装饰器自动从函数签名+docstring生成 name/description/args_schema
  - PydanticOutputParser 会向 Prompt 注入 format_instructions，引导模型按格式输出
============================================================
"""
