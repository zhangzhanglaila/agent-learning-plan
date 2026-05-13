"""
Day9 (5/21) — MCP 模型上下文协议实战
=====================================
任务：
  1. 搭建一个 MCP Server（天气服务）
  2. 用 LangChain MCP 客户端连接并调用

学习目标：
  1. 理解 MCP 的三角色架构：Host - Client - Server
  2. 掌握 FastMCP 的基本写法
  3. 能区分 MCP 和 Function Calling 的关系

注意：本文件需要安装 mcp 和 langchain-mcp-adapters
  pip install mcp langchain-mcp-adapters
"""

import os
import asyncio
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# Part 1: MCP Server（天气服务）
# 保存为独立的 mcp_weather_server.py 并单独运行
# ============================================================

MCP_SERVER_CODE = '''
"""
MCP 天气服务 Server
运行方式：python mcp_weather_server.py
"""
import asyncio
from mcp.server.fastmcp import FastMCP

# 创建 MCP Server 实例
mcp = FastMCP("天气服务")

# 注册 Tool：暴露给AI模型调用的能力
@mcp.tool()
async def get_weather(city: str) -> str:
    """查询指定城市的实时天气（模拟数据）

    Args:
        city: 城市名称，如 北京、上海、深圳
    """
    weather_db = {
        "北京": "晴，22°C，湿度40%",
        "上海": "多云，25°C，湿度65%",
        "深圳": "阵雨，28°C，湿度80%",
        "杭州": "阴，20°C，湿度55%",
    }
    return weather_db.get(city, f"{city}：晴，20°C（模拟天气数据）")


@mcp.tool()
async def get_forecast(city: str, days: int = 3) -> str:
    """查询未来N天天气预报（模拟）

    Args:
        city: 城市名称
        days: 预报天数，默认3天
    """
    forecast = {
        "北京": ["晴 22°C", "多云 20°C", "小雨 18°C"],
        "上海": ["多云 25°C", "阴 23°C", "小雨 21°C"],
    }
    city_forecast = forecast.get(city, [f"晴 {20+i}°C" for i in range(days)])
    return f"{city}未来{days}天：" + " | ".join(city_forecast[:days])


@mcp.resource("weather://cities")
async def list_cities() -> str:
    """列出支持的城市列表（Resource 类型）"""
    return "支持的城市：北京、上海、深圳、杭州"


# STDIO 方式运行（标准输入输出）
if __name__ == "__main__":
    print("🌤️  MCP天气服务已启动（STDIO模式）")
    mcp.run(transport="stdio")
'''

# 写入 Server 文件
with open("./mcp_weather_server.py", "w", encoding="utf-8") as f:
    f.write(MCP_SERVER_CODE)
print("已生成 mcp_weather_server.py，可单独运行：python mcp_weather_server.py")


# ============================================================
# Part 2: MCP Client（通过 LangChain 调用 MCP Server）
# ============================================================

CLIENT_DEMO = '''
"""MCP 客户端：通过 LangChain 连接 MCP Server"""
import os
import asyncio
from dotenv import load_dotenv

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

async def main():
    # 1. 创建 MCP 客户端，连接本地 STDIO 天气服务
    mcp_client = MultiServerMCPClient(
        {
            "weather": {
                "command": "python",
                "args": ["mcp_weather_server.py"],
                "transport": "stdio",
            }
        }
    )

    # 2. 获取 MCP Server 暴露的工具，转为 LangChain Tool
    tools = await mcp_client.get_tools()
    print(f"🔌 从 MCP Server 获取到 {len(tools)} 个工具：")
    for t in tools:
        print(f"  - {t.name}: {t.description}")

    # 3. 创建 LLM
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL"),
        temperature=0,
    )

    # 4. 构建 Agent
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个天气预报助手，使用天气工具回答用户问题。"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # 5. 测试
    queries = [
        "北京今天天气怎么样？",
        "上海未来3天什么天气？",
        "有哪些城市可以查天气？",
    ]
    for q in queries:
        print(f"\\n{'='*50}")
        print(f"👤 {q}")
        result = await executor.ainvoke({
            "input": q,
            "chat_history": [],
        })
        print(f"✅ {result['output']}")


if __name__ == "__main__":
    asyncio.run(main())
'''

with open("./mcp_weather_client.py", "w", encoding="utf-8") as f:
    f.write(CLIENT_DEMO)
print("已生成 mcp_weather_client.py")


# ============================================================
# Part 3: MCP 概念验证（不依赖 mcp 包的轻量演示）
# ============================================================

def mcp_concept_demo():
    """
    不用真实 MCP 包，用代码演示 MCP 的核心概念：
    MCP = 统一的协议标准，让工具/资源/提示可以跨平台暴露和接入
    """
    print("\n" + "=" * 60)
    print("MCP 核心概念演示（纯Python模拟）")

    # 模拟一个 MCP Server 的能力注册表
    class MockMCPServer:
        def __init__(self, name: str):
            self.name = name
            self.tools = {}   # model-controlled：AI决定何时调用
            self.resources = {}  # application-driven：宿主程序决定何时读取
            self.prompts = {}    # user-controlled：用户手动选择

        def register_tool(self, name: str, description: str, schema: dict, handler):
            self.tools[name] = {
                "description": description,
                "inputSchema": schema,
                "handler": handler,
            }

        def register_resource(self, uri: str, description: str, handler):
            self.resources[uri] = {
                "description": description,
                "handler": handler,
            }

        def list_capabilities(self):
            return {
                "tools": list(self.tools.keys()),
                "resources": list(self.resources.keys()),
                "prompts": list(self.prompts.keys()),
            }

    # 创建天气 MCP Server
    weather_server = MockMCPServer("weather-service")

    # 注册 Tool（AI 决定何时调用）
    weather_server.register_tool(
        name="get_weather",
        description="查询指定城市的实时天气",
        schema={"city": {"type": "string", "description": "城市名称"}},
        handler=lambda city: f"{city}：晴 22°C",
    )

    # 注册 Resource（应用按需读取）
    weather_server.register_resource(
        uri="weather://config/cities",
        description="支持的城市列表",
        handler=lambda: ["北京", "上海", "深圳", "杭州"],
    )

    print(f"Server: {weather_server.name}")
    print(f"能力清单: {weather_server.list_capabilities()}")

    # MCP vs Function Calling 的区别
    print("""
┌─────────────────────────────────────────────────────┐
│ MCP 和 Function Calling 的关系（面试重点）           │
├─────────────────────────────────────────────────────┤
│ Function Calling：模型如何表达"我要调哪个工具"       │
│                   → 属于模型推理层的结构化调用机制    │
│                                                      │
│ MCP：工具/资源/提示如何被标准化暴露和接入             │
│       → 属于生态层的统一协议                         │
│                                                      │
│ 关系：上下层，不是替代关系                           │
│ Agent 可以在 MCP 暴露的能力之上                      │
│       继续用 Function Calling 做调用决策             │
└─────────────────────────────────────────────────────┘
""")


if __name__ == "__main__":
    mcp_concept_demo()
    print("\n✅ 已生成文件：")
    print("  - mcp_weather_server.py（MCP Server）")
    print("  - mcp_weather_client.py（MCP Client）")
    print("\n运行方式：")
    print("  # 终端1：启动MCP Server")
    print("  python mcp_weather_server.py")
    print("  # 终端2：运行客户端测试")
    print("  python mcp_weather_client.py")

"""
============================================================
📝 练习任务：
  1. 阅读并理解 mcp_weather_server.py 和 mcp_weather_client.py
  2. 给 MCP Server 添加第三个 Tool（如：get_humidity 查询湿度）
  3. 用 mcp_weather_client.py 测试新工具
  4. 思考：如果不用 MCP，你的工具是怎么暴露给 Agent 的？（对比 EasyAgent 的正则方式）

💡 关键理解：
  MCP 三角色：
    Host：  发起请求的一方（如 Claude Desktop、你的应用）
    Client：与 Server 建立连接，转换协议消息
    Server：暴露能力的一方（工具/资源/提示模板）

  三种能力类型：
    Tools：     AI 决定何时调用（model-controlled）
    Resources： 宿主程序决定何时读取（application-driven）
    Prompts：   用户手动选择（user-controlled）

  传输方式：
    STDIO：          标准输入输出，适合本地工具
    Streamable HTTP：HTTP流式传输，适合远程服务
============================================================
"""
