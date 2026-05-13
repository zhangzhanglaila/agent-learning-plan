from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam
import os
import re  # 新增：精准提取工具参数
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化客户端
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
)


# ===================== 【优化1：更健壮的计算器】 =====================
def calculator(expression: str) -> str:
    """
    优化版计算器：自动识别中文数学符号（×÷＋－），支持所有运算
    """
    try:
        # 关键：把中文符号替换成Python能识别的英文符号
        expression = expression.replace("×", "*").replace("÷", "/").replace("＋", "+").replace("－", "-")
        # 只保留数字和运算符号，过滤所有文字
        expression = re.sub(r"[^0-9+\-*/]", "", expression)

        result = eval(expression)
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算失败：{str(e)}"


# ===================== 【优化2：强制AI只输出工具指令，不加废话】 =====================
system_prompt: ChatCompletionSystemMessageParam = {
    "role": "system",
    "content": """
    你是一个严格执行规则的智能Agent。
    【铁律】：只要是数学计算，**只输出工具指令，不许加任何文字、换行、解释**！
    工具调用格式：[calculator]数学表达式
    例子：[calculator]12345*67890
    禁止输出任何多余内容！
    """
}

# 对话上下文
messages: list = [
    system_prompt,
    {"role": "user", "content": "12345 × 67890 等于多少？"}
]

# ===================== 【优化3：精准提取工具指令】 =====================
# 1. AI思考
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)
agent_thought = response.choices[0].message.content
print("🤖 Agent工具调用：", agent_thought)

# 2. 正则表达式：精准提取 [calculator] 后面的计算式
match = re.search(r"\[calculator\](.*)", agent_thought.strip(), re.I)
if match:
    expression = match.group(1).strip()  # 只提取计算式
    tool_result = calculator(expression)
    print("🔧 工具执行结果：", tool_result)

    # 3. 把结果还给AI，生成最终回答
    messages.append({"role": "assistant", "content": agent_thought})
    messages.append({"role": "user", "content": tool_result})

    final_response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )
    print("\n✅ Agent最终回答：", final_response.choices[0].message.content)
else:
    print("\n✅ Agent回答：", agent_thought)