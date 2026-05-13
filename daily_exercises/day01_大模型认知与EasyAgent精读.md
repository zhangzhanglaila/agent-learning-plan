# Day1 (5/13) — 大模型认知 + EasyAgent代码精读

## 📖 阅读任务

1. **1-1 大模型认知与工程概览** — 重点：Token概念、训练三阶段、开源vs闭源
2. **1-2 提示词工程基础** — 重点：核心六要素、System/User/Assistant角色
3. **1-3 RAG、微调、续训与智能体选型** — 重点：五者选型判断

---

## ✍️ 代码精读任务：逐行理解 EasyAgent 三个文件

### demo.py — 多轮对话基础

```python
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
    {"role": "user", "content": "1+1等于几？"},
    {"role": "assistant", "content": "等于3"},
    {"role": "user", "content": "再加3等于几？"}
]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)

print("DeepSeek回答：", response.choices[0].message.content)
```

**逐行理解要点：**
- 第1-4行：导入依赖 — `OpenAI`客户端、类型提示、`os`读环境变量、`load_dotenv`加载`.env`
- 第6行：`load_dotenv()` 从项目根目录`.env`文件加载 `DEEPSEEK_API_KEY` 和 `DEEPSEEK_BASE_URL`
- 第8-11行：创建OpenAI兼容客户端，指向DeepSeek的API地址
- 第14-21行：消息列表包含3条历史 — 构建多轮对话上下文
- 第23-26行：调用模型，传入消息历史，获取回复
- **核心模式：** `messages` 列表 = 对话历史，模型看到完整上下文再生成

---

### demo2.py — Agent工具调用循环

```python
from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam
import os
import re
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
)


# ===================== 工具1：计算器 =====================
def calculator(expression: str) -> str:
    """优化版计算器：自动识别中文数学符号"""
    try:
        # 把中文符号替换成Python能识别的英文符号
        expression = expression.replace("×", "*").replace("÷", "/").replace("＋", "+").replace("－", "-")
        # 只保留数字和运算符号，过滤所有文字
        expression = re.sub(r"[^0-9+\-*/]", "", expression)
        result = eval(expression)
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算失败：{str(e)}"


# ===================== System Prompt：约束Agent行为 =====================
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

# ===================== Agent循环 =====================
# Step 1: 模型决策
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)
agent_thought = response.choices[0].message.content
print("🤖 Agent工具调用：", agent_thought)

# Step 2: 正则提取工具指令
match = re.search(r"\[calculator\](.*)", agent_thought.strip(), re.I)
if match:
    expression = match.group(1).strip()
    tool_result = calculator(expression)
    print("🔧 工具执行结果：", tool_result)

    # Step 3: 结果回传，模型生成最终回复
    messages.append({"role": "assistant", "content": agent_thought})
    messages.append({"role": "user", "content": tool_result})

    final_response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )
    print("\n✅ Agent最终回答：", final_response.choices[0].message.content)
else:
    print("\n✅ Agent回答：", agent_thought)
```

**逐行理解要点——Agent核心循环：**
1. **System Prompt 定规则** — 告诉模型"只输出工具指令"（第30-37行）
2. **模型决策** — 模型读取消息，决定输出 `[calculator]12345*67890`（第43-48行）
3. **宿主程序提取指令** — 用正则 `\[calculator\](.*)` 精确解析（第52行）
4. **宿主程序执行工具** — `calculator("12345*67890")` → 返回计算结果（第54行）
5. **结果回传给模型** — 把工具结果追加到消息历史（第58-59行）
6. **模型生成最终回答** — 基于工具结果生成自然语言回复（第61-65行）

**关键理解：模型不执行代码，只输出"调用意图"！** 实际执行在宿主程序。

---

### practice.py — 独立实现（你的版本）

```python
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
    return f"计算结果：{result}"


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
```

---

## ✅ Day1 自检清单

- [ ] 能用自己的话解释 Token 是什么？上下文窗口的工程意义？
- [ ] 能画图说出 RAG vs 微调 vs Agent 分别解决什么问题？
- [ ] 能默写 `demo2.py` 的 Agent 循环6步骤？
- [ ] 能解释为什么模型不直接调API，而是输出"调用意图"？
- [ ] 能说出 System Message 和 User Message 的分工？
