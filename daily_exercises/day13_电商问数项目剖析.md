# Day13 (5/25) — 电商问数项目深度剖析

## 📖 阅读任务

精读 `实战项目-电商问数/` 下的全部章节，理解一个完整的 NL2SQL Agent 项目。

---

## 🏗️ 项目架构全景图

```
用户自然语言问题
      │
      ▼
┌─────────────────────────────────────────────┐
│         FastAPI 接口层 (SSE流式)              │
│   /query → QueryService → 图执行             │
└─────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────┐
│          LangGraph 问数工作流                  │
│                                               │
│  [关键词抽取] → [多路召回] → [上下文合并]     │
│       │              │              │          │
│       ▼              ▼              ▼          │
│   稀疏检索     稠密向量检索    字段值检索       │
│  (Elasticsearch) (Qdrant)   (ES精确匹配)      │
│       │              │              │          │
│       └──────────────┴──────────────┘          │
│                      │                         │
│                      ▼                         │
│              [信息过滤与补全]                   │
│                      │                         │
│                      ▼                         │
│          [SQL生成 → 校验 → 纠错 → 执行]        │
│                      │                         │
│                      ▼                         │
│                 [结果返回]                      │
└─────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────┐
│            元数据知识库                        │
│  MySQL(表/字段/指标) + Qdrant(向量)           │
│  + Elasticsearch(全文检索)                    │
└─────────────────────────────────────────────┘
```

---

## 🔑 核心技术点拆解

### 1. 数仓基础（第1章）

```
事实表(Fact)：  记录业务事件 — 如：订单表、支付表
维度表(Dim)：   描述业务实体 — 如：商品表、用户表、日期表
指标(Metric)：  可度量的业务值 — 如：销售额、订单数、客单价
维度(Dimension)：分析的角度 — 如：按日期、按地区、按品类
```

**面试表达：** "问数项目本质上是把用户的自然语言问题，
通过检索元数据（表名/字段名/指标名），
翻译成可执行的SQL，然后返回查询结果。"

### 2. 元数据知识库（第7-9章）

```
元数据类型          存储位置              检索方式
─────────────────────────────────────────────────
表信息             MySQL + Qdrant        语义检索
字段信息           MySQL + Qdrant        语义检索 + 精确匹配
字段值             Elasticsearch         关键词 + 模糊搜索
指标定义           MySQL + Qdrant        语义检索
```

**为什么不能只靠向量检索？**
- 用户问"华为手机" → 数据库字段叫 `brand_name`
- 纯向量检索可能找不到这个对应关系
- 需要 语义检索 + 关键词匹配 + 字段值精确匹配 三路召回

### 3. 三路召回（第11章）

```python
# 核心代码骨架
def multi_route_recall(query: str) -> dict:
    """三路召回策略"""
    return {
        # 路1：稠密向量语义召回 → 找"意思相近"的字段
        "dense": qdrant.search(
            query_vector=embed(query),
            top_k=10,
        ),
        # 路2：稀疏关键词召回 → 找"关键词匹配"的字段
        "sparse": es.search(
            query={"match": {"field_name": query}},
            top_k=10,
        ),
        # 路3：字段值精确召回 → "华为"是否在brand_name的枚举值里
        "value": es.search_field_values(
            keywords=extract_keywords(query),
            top_k=10,
        ),
    }
```

面试表达："三路召回解决的是语义匹配盲区问题，
稠密向量负责语义相似，稀疏检索负责关键词命中，
字段值检索负责精确枚举匹配。"

### 4. SQL 闭环（第14章）⭐核心⭐

```
            ┌──────────────────────────────────┐
            │         SQL 生成与执行闭环         │
            │                                    │
            │  generate_sql ──→ validate_sql     │
            │       ↑                │            │
            │       │           [语法/权限/危险]  │
            │       │                │            │
            │       │          ┌─────┴─────┐      │
            │       │          │ 通过？     │      │
            │       │          └─────┬─────┘      │
            │       │          是    │    否      │
            │       │          │     ▼            │
            │       │          │  correct_sql     │
            │       │          │     │            │
            │       │          │     └────────┐   │
            │       │          ▼              │   │
            │       │       run_sql           │   │
            │       │          │              │   │
            │       │     [执行成功？]         │   │
            │       │     是   │   否         │   │
            │       │     │    └──────────────┘   │
            │       │     ▼                       │
            │       │  返回结果                    │
            │       └─────────────────────────────┘
            └──────────────────────────────────┘
```

**四个核心函数：**

```python
def generate_sql(user_question: str, context: str) -> str:
    """LLM 根据用户问题 + 检索到的元数据上下文 → 生成SQL"""
    prompt = f"""
    根据以下元数据信息，将用户问题转为SQL。
    
    元数据：
    {context}
    
    用户问题：{user_question}
    
    只输出SQL，不要任何解释。
    """
    return llm.invoke(prompt)


def validate_sql(sql: str) -> tuple[bool, str]:
    """
    校验SQL的合法性：
    1. 语法检查（用 sqlparse 或 EXPLAIN）
    2. 安全检查（禁止 DROP/DELETE/UPDATE/INSERT）
    3. 权限检查（只允许 SELECT 指定表）
    """
    # 安全检查
    dangerous_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]
    sql_upper = sql.upper()
    for kw in dangerous_keywords:
        if kw in sql_upper:
            return False, f"禁止的操作：{kw}"

    # 语法检查
    try:
        import sqlparse
        parsed = sqlparse.parse(sql)
        if not parsed:
            return False, "SQL语法错误"
    except Exception:
        pass  # 非关键检查

    return True, "OK"


def correct_sql(sql: str, error_msg: str) -> str:
    """SQL出错时，让LLM自我修正"""
    prompt = f"""
    以下SQL执行时出错，请修正。
    
    原始SQL：{sql}
    错误信息：{error_msg}
    
    只输出修正后的SQL。
    """
    return llm.invoke(prompt)


def run_sql(sql: str) -> dict:
    """在沙箱中执行SQL"""
    # 再次安全检查
    ok, err = validate_sql(sql)
    if not ok:
        return {"success": False, "error": err}

    # 执行
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        return {"success": True, "data": rows}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### 5. SSE 流式接口（第15-17章）

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json
import asyncio

app = FastAPI()

@app.post("/query")
async def query(request: QueryRequest):
    """流式问数接口"""
    async def event_stream():
        # 用 LangGraph 的 astream_events 实现流式
        async for event in graph.astream_events(
            {"question": request.question},
            version="v2",
        ):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                # 模型输出的 token 流
                chunk = event["data"]["chunk"]
                yield f"data: {json.dumps({'type': 'token', 'content': chunk.content})}\n\n"

            elif kind == "on_tool_start":
                # 工具调用开始
                yield f"data: {json.dumps({'type': 'tool_start', 'name': event['name']})}\n\n"

            elif kind == "on_tool_end":
                # 工具调用结束
                yield f"data: {json.dumps({'type': 'tool_end', 'name': event['name']})}\n\n"

        # 流结束
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
```

---

## ✅ Day13 自检清单

- [ ] 能画出项目的完整架构图（三路召回 + SQL闭环）
- [ ] 能用自己的话解释：为什么需要元数据知识库？为什么三路召回？
- [ ] 能默写 SQL 闭环的四个步骤（generate→validate→correct→execute）
- [ ] 能说出 SSE 流式格式的关键格式：`data: {json}\n\n`
- [ ] 准备面试表达："这个项目把数仓、检索、生成、执行和前端交付串成一条链路"
