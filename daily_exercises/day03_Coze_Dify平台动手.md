# Day3 (5/15) — Coze & Dify 低代码平台动手

## 📖 阅读任务

1. **第3章** 基于Coze&Dify平台的智能体开发 — 重点：两者的功能模块对比
2. **第4章** Python调用Dify平台工作流 — 重点：API Key + SSE流式
3. **第5章** Python调用Coze平台工作流 — 重点：参数对齐 + 流式PING/MESSAGE/DONE

---

## ✍️ 动手任务

### 任务1：在 Dify 上搭建"客服分类Agent"

**步骤：**
1. 注册/登录 Dify 平台
2. 创建新应用 → 选择 "Chatflow" 类型
3. 搭建工作流：
   ```
   [开始] → [LLM: 意图分类] → [条件分支]
     ├─ 投诉类 → [LLM: 道歉+记录] → [结束]
     ├─ 咨询类 → [知识库检索] → [LLM: 回答] → [结束]
     └─ 其他   → [LLM: 转人工] → [结束]
   ```
4. 测试：输入"我要投诉产品质量问题"，观察走哪个分支

### 任务2：用 Python 调用 Dify 工作流

```python
"""
Python 调用 Dify 工作流 Demo
============================
前置条件：在 Dify 平台发布工作流，获取 API Key
"""
import requests
import json

# Dify 配置
DIFY_API_KEY = "app-xxxxxxxxxxxxx"  # 替换为你的 API Key
DIFY_BASE_URL = "http://localhost/v1"  # 本地部署地址

def call_dify_workflow(query: str, user: str = "user-001") -> str:
    """调用 Dify 工作流（阻塞模式）"""
    url = f"{DIFY_BASE_URL}/chat-messages"
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": {},  # 工作流输入变量
        "query": query,
        "user": user,
        "response_mode": "blocking",  # 阻塞模式
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    return data.get("answer", "")


def call_dify_streaming(query: str, user: str = "user-001"):
    """调用 Dify 工作流（流式模式）"""
    url = f"{DIFY_BASE_URL}/chat-messages"
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": {},
        "query": query,
        "user": user,
        "response_mode": "streaming",  # 流式模式
    }

    response = requests.post(url, headers=headers, json=payload, stream=True)

    full_answer = []
    for line in response.iter_lines(decode_unicode=True):
        if not line or not line.startswith("data: "):
            continue
        json_str = line[6:]  # 去掉 "data: " 前缀
        try:
            event = json.loads(json_str)

            # Dify 的 SSE 事件类型
            event_type = event.get("event", "")

            if event_type == "message":
                # 模型输出的文本块
                chunk = event.get("answer", "")
                print(chunk, end="", flush=True)
                full_answer.append(chunk)

            elif event_type == "workflow_finished":
                # 工作流执行完毕
                print(f"\n[工作流完成，状态：{event.get('data', {}).get('status')}]")

            elif event_type == "error":
                print(f"\n[错误：{event.get('message')}]")
                break

        except json.JSONDecodeError:
            continue

    return "".join(full_answer)


if __name__ == "__main__":
    # 测试阻塞模式
    print("=== 阻塞模式 ===")
    result = call_dify_workflow("我要投诉产品质量问题")
    print(f"回答：{result}")

    print("\n=== 流式模式 ===")
    call_dify_streaming("你们的退货政策是什么？")
```

### 任务3：在 Coze 上搭建同样功能的 Bot

**步骤：**
1. 进入 Coze 平台 → 创建 Bot
2. 配置：
   - 人设与回复逻辑（System Prompt）
   - 添加插件（如：搜索插件）
   - 添加知识库（上传FAQ文档）
   - 设置工作流（可选）
3. 发布到 API → 获取 access_token

```python
"""
Python 调用 Coze Bot API
"""
import requests
import json

COZE_API_KEY = "pat_xxxxxxxxxxxxx"  # 替换为你的 Personal Access Token
COZE_BOT_ID = "bot_xxxxxxxxxxxxx"   # 替换为你的 Bot ID

def call_coze_bot(query: str, user_id: str = "user-001") -> str:
    """调用 Coze Bot（非流式）"""
    url = "https://api.coze.cn/v3/chat"
    headers = {
        "Authorization": f"Bearer {COZE_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "bot_id": COZE_BOT_ID,
        "user_id": user_id,
        "stream": False,
        "additional_messages": [
            {
                "role": "user",
                "content": query,
                "content_type": "text",
            }
        ],
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    # 从响应中提取回复
    messages = data.get("messages", [])
    for msg in messages:
        if msg.get("role") == "assistant" and msg.get("type") == "answer":
            return msg.get("content", "")
    return "未获取到回复"


def call_coze_streaming(query: str, user_id: str = "user-001"):
    """调用 Coze Bot（流式）"""
    url = "https://api.coze.cn/v3/chat"
    headers = {
        "Authorization": f"Bearer {COZE_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "bot_id": COZE_BOT_ID,
        "user_id": user_id,
        "stream": True,
        "additional_messages": [
            {"role": "user", "content": query, "content_type": "text"}
        ],
    }

    response = requests.post(url, headers=headers, json=payload, stream=True)

    for line in response.iter_lines(decode_unicode=True):
        if not line or not line.startswith("data: "):
            continue
        json_str = line[6:]
        try:
            event = json.loads(json_str)

            # Coze 流式事件类型
            if event.get("event") == "PING":
                continue  # 心跳
            elif event.get("event") == "MESSAGE":
                chunk = event.get("data", {}).get("content", "")
                print(chunk, end="", flush=True)
            elif event.get("event") == "DONE":
                print("\n[对话完成]")
                break
            elif event.get("event") == "ERROR":
                print(f"\n[错误：{event.get('data', {}).get('message')}]")
                break
        except json.JSONDecodeError:
            continue


if __name__ == "__main__":
    print("=== Coze 非流式 ===")
    result = call_coze_bot("你好，请介绍一下你自己")
    print(f"回答：{result}")

    print("\n=== Coze 流式 ===")
    call_coze_streaming("帮我分析一下最近的热点新闻")
```

---

## ✅ Day3 自检清单

- [ ] Dify 上搭建了至少一个 Chatflow
- [ ] Coze 上搭建了至少一个 Bot
- [ ] 能说出 Dify 流式响应的关键事件：`message` → `workflow_finished`
- [ ] 能说出 Coze 流式响应的关键事件：`PING` → `MESSAGE` → `DONE`
- [ ] 能对比 Coze/Dify 和 LangChain/LangGraph 的定位差异
