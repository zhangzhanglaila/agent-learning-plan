import os
import re

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam


load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL")
)
def calculator(expression: str) -> str:
    expression = expression.replace("×", "*").replace("÷", "/").replace("＋", "+").replace("－", "-")
    expression = re.sub(r"[^0-9+\-*/]", "", expression)
    result = eval(expression)
    return f"计算结果：{result}"  # 返回字符串


system_prompt: ChatCompletionSystemMessageParam = {
    "role": "system",
    "content": """
    你是一个严格执行规则的agent
    规则：但凡有计算，只输出工具指令
    工具调用格式：[calculator]数学表达式
    例如：[calculator]12345*67890
    禁止输出其他内容
    """
}

messages: list = [
    system_prompt,
    {"role": "user", "content": "520*2等于多少"}
]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)
agent_thought = response.choices[0].message.content
match = re.search(r"\[calculator\](.*)", agent_thought, re.I)
if match:
    expression = match.group(1).strip()
    tool_result = calculator(expression)
    messages.append({"role": "assistant", "content": agent_thought})
    messages.append({"role": "user", "content": tool_result})
    final_response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )
    print("\n✅ Agent最终回答：", final_response.choices[0].message.content)


else:
    print("\n✅ Agent回答：", agent_thought)