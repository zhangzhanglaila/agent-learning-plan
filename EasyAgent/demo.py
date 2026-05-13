from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam
import os
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
)

# 用官方类型定义消息
messages: list[ChatCompletionUserMessageParam] = [
    # 第1条：用户问
    {"role": "user", "content": "1+1等于几？"},
    # 第2条：AI回答
    {"role": "assistant", "content": "等于3"},
    # 第3条：用户继续问（基于上文）
    {"role": "user", "content": "再加3等于几？"}
]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)

print("DeepSeek回答：", response.choices[0].message.content)