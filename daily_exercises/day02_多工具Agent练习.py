"""
Day2 (5/14) — 多工具Agent练习
===============================
任务：基于 practice.py 改造，添加第二个工具（字符串反转/统计），
让Agent能根据用户意图自动选择调用哪个工具。

学习目标：
  1. 理解多工具Agent的工具注册与调度机制
  2. 学会用 System Prompt 约束模型输出可解析的工具指令
  3. 掌握正则提取 + 工具路由的基本模式
"""

import os
import re
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
)


# ==================== 工具1：计算器 ====================
def calculator(expression: str) -> str:
    """安全的数学计算器"""
    try:
        expression = expression.replace("×", "*").replace("÷", "/")
        expression = expression.replace("＋", "+").replace("－", "-")
        expression = re.sub(r"[^0-9+\-*/.]", "", expression)
        if not expression:
            return "计算失败：无效的表达式"
        result = eval(expression)
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算失败：{str(e)}"


# ==================== 工具2：字符串工具箱 ====================
def string_tool(action: str, text: str) -> str:
    """
    字符串处理工具箱
    action: reverse(反转) | count(统计字符数) | upper(转大写)
    """
    action = action.strip().lower()
    text = text.strip()

    if action == "reverse":
        return f"反转结果：{text[::-1]}"
    elif action == "count":
        return f"字符数（含空格）：{len(text)}"
    elif action == "upper":
        return f"大写结果：{text.upper()}"
    else:
        return f"未知操作：{action}，支持的操作：reverse / count / upper"


# ==================== System Prompt：多工具调度 ====================
system_prompt: ChatCompletionSystemMessageParam = {
    "role": "system",
    "content": """
你是一个严格执行规则的智能Agent，具备以下工具：

【工具1】计算器
  格式：[calculator]数学表达式
  示例：[calculator]100*25

【工具2】字符串工具箱
  格式：[string]操作名 文本内容
  支持操作：reverse(反转), count(统计字符), upper(转大写)
  示例：[string]reverse hello world
  示例：[string]count 今天天气真好

【铁律】
  1. 数学计算 → 只输出 [calculator] 指令
  2. 字符串操作 → 只输出 [string] 指令
  3. 禁止输出任何额外文字、换行、解释！
"""
}

# ==================== 工具调度器 ====================
def dispatch_tool(agent_response: str) -> str | None:
    """解析Agent输出，调度到对应工具，返回工具结果；不匹配返回None"""
    agent_response = agent_response.strip()

    # 匹配 [calculator]表达式
    calc_match = re.search(r"\[calculator\](.*)", agent_response, re.I)
    if calc_match:
        expression = calc_match.group(1).strip()
        return calculator(expression)

    # 匹配 [string]操作名 文本（文本可为空）
    str_match = re.search(r"\[string\]\s*(\S+)(?:\s+(.*))?", agent_response, re.I)
    if str_match:
        action = str_match.group(1)
        text = str_match.group(2)
        return string_tool(action, text)

    return None


# ==================== Agent 对话循环 ====================
def run_agent(user_input: str) -> str:
    """一次完整的Agent交互：用户输入 → 模型决策 → 工具执行 → 最终回复"""
    messages: list = [
        system_prompt,
        {"role": "user", "content": user_input},
    ]

    # Step 1: 模型决策
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
    )
    agent_thought = response.choices[0].message.content
    print(f"🤖 Agent决策：{agent_thought}")

    # Step 2: 工具调度
    tool_result = dispatch_tool(agent_thought)

    if tool_result is not None:
        print(f"🔧 工具结果：{tool_result}")

        # Step 3: 结果回传，让模型生成最终回答
        messages.append({"role": "assistant", "content": agent_thought})
        messages.append({"role": "user", "content": f"工具返回结果：{tool_result}\n请用自然语言回复用户。"})

        final_response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
        )
        final_answer = final_response.choices[0].message.content
        return final_answer
    else:
        return agent_thought


# ==================== 测试用例 ====================
if __name__ == "__main__":
    test_cases = [
        "12345 × 67890 等于多少？",
        "把 'hello world' 反转一下",
        "统计这句话有多少个字符：今天天气真好",
        "帮我把 python 转成大写",
    ]

    for query in test_cases:
        print(f"\n{'='*60}")
        print(f"👤 用户：{query}")
        result = run_agent(query)
        print(f"✅ 最终回答：{result}")

"""
============================================================
📝 练习任务：
  1. 运行上面的代码，观察Agent如何自动选择工具
  2. 添加第三个工具：翻译工具 [translate]源语言→目标语言 文本
     （可以先用mock实现，返回 f"翻译({src}→{dst})：{text}"）
  3. 在System Prompt中注册新工具
  4. 在 dispatch_tool() 中添加匹配逻辑
  5. 测试："把 'hello world' 翻译成中文"

💡 思考题：
  - 如果用户说"先算100+200，再把结果反转"，当前系统能处理吗？
  - 如果不能，缺少什么能力？（提示：多步推理 + 状态管理）
============================================================
"""
