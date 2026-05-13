"""
Day8 (5/20) — 从零搭建 RAG 问答系统
=====================================
任务：完整实现一个 RAG（检索增强生成）Pipeline

学习目标：
  1. 掌握 RAG 的完整流程：加载→切块→向量化→存储→检索→生成
  2. 理解每个环节的工程意义
  3. 能回答面试中的 RAG 全链路问题
"""

import os
from typing import List
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma

load_dotenv()

# 国内用户如无法访问 HuggingFace，取消下面这行的注释：
# os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# ==================== 初始化 ====================
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    temperature=0,
)

# 优先用本地模型（免费、离线），失败则尝试 OpenAI 兼容 API
try:
    from langchain_huggingface import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="shibing624/text2vec-base-chinese",
        model_kwargs={"device": "cpu"},
    )
    print("✅ 使用本地 Embedding 模型：text2vec-base-chinese")
except (ImportError, Exception):
    try:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL"),
        )
        print("✅ 使用 OpenAI Embedding API")
    except Exception:
        raise RuntimeError(
            "无法初始化 Embedding！请执行：\n"
            "  pip install langchain-huggingface sentence-transformers\n"
            "或提供有效的 OpenAI API Key"
        )

# ==================== Step 1: 准备文档 ====================
# 模拟一个企业内部知识库
raw_documents = [
    """AI Agent（智能体）是由大语言模型（LLM）、工具集、运行循环和当前状态组成的自主系统。
    与传统AI应用不同，Agent能根据目标持续做出决策，动态选择工具，并根据反馈调整策略。
    Agent的核心循环是 ReAct 模式：Thought（思考）→ Action（行动）→ Observation（观察）。
    适用场景：路径不确定、需要根据中间结果动态调用工具的任务。""",

    """RAG（Retrieval-Augmented Generation，检索增强生成）是一种将外部知识检索与
    大模型生成相结合的技术。核心流程分为两个阶段：
    索引阶段：文档加载 → 清洗 → 切块 → 向量化 → 写入向量库
    检索阶段：问题输入 → Query改写 → 检索召回 → 重排序 → 上下文组装 → 模型生成
    RAG的优势：知识可溯源、时效性强、无需重新训练模型。""",

    """LangChain 是一个用于构建 LLM 应用的开发框架，核心包含六大模块：
    1. Models（模型接入）：统一封装各种LLM的调用接口
    2. Memory（记忆）：管理对话历史和上下文状态
    3. Retrieval（检索）：文档加载、向量存储、检索
    4. Chains（链）：将多个组件串联成处理流水线
    5. Agents（智能体）：模型动态决策调用哪些工具
    6. Callbacks（回调）：日志、监控、流式输出""",

    """LangGraph 是 LangChain 生态中的图状态机框架，
    用于构建包含循环、分支、人工介入的复杂Agent工作流。
    四个核心概念：
    - State（状态）：所有节点共享的上下文数据
    - Node（节点）：处理逻辑单元（调模型、查库、执行工具）
    - Edge（边）：流转规则（固定跳转或条件路由）
    - Graph（图）：节点+边的集合，编译后即可执行
    高级特性：流式处理、状态持久化（Checkpointer）、时间回溯（Time-Travel）、子图""",

    """Function Calling 是大模型的结构化调用机制。
    工作原理：宿主应用向模型发送工具列表（名称+描述+参数schema），
    模型根据用户输入决定是否调用工具及传什么参数，返回 tool_calls 结构，
    宿主程序执行函数后将结果封装为 ToolMessage 返回模型，
    模型基于工具结果生成最终回复。
    关键点：模型只负责决策（调用什么、传什么参数），不负责执行。""",
]

print(f"📄 加载了 {len(raw_documents)} 篇文档")


# ==================== Step 2: 文档切块 ====================
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,       # 每块最多200字符
    chunk_overlap=50,     # 相邻块重叠50字符，保持语义连续性
    separators=["\n\n", "\n", "。", "，", " ", ""],  # 优先在自然边界切分
)

chunks: List[Document] = text_splitter.create_documents(
    [doc for doc in raw_documents],
    # 为每个chunk添加元数据（方便后续过滤和溯源）
    metadatas=[{"source": f"doc_{i}"} for i in range(len(raw_documents))],
)

print(f"✂️  切分后共 {len(chunks)} 个 chunk")
for i, chunk in enumerate(chunks):
    print(f"  chunk_{i}: {chunk.page_content[:60]}... [来源：{chunk.metadata['source']}]")


# ==================== Step 3: 向量化 + 存储 ====================
# Chroma 是轻量级向量数据库，适合本地开发和Demo
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="my_knowledge_base",
    persist_directory="./chroma_db",  # 持久化到本地
)

print(f"💾 向量库已建立，共 {vectorstore._collection.count()} 条向量")


# ==================== Step 4: 构建检索器 ====================
retriever = vectorstore.as_retriever(
    search_type="similarity",  # 相似度检索
    search_kwargs={"k": 3},    # 返回Top-3最相关chunk
)


# ==================== Step 5: RAG 问答链 ====================
# 提示词模板：关键是告诉模型"基于检索到的上下文回答，不要编造"
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个基于知识库回答问题的助手。

【规则】
1. 只根据下面提供的【参考资料】回答问题
2. 如果资料中没有相关信息，请明确说"根据现有资料，我无法回答这个问题"
3. 回答时尽量引用资料中的原文
4. 回答简洁、准确

【参考资料】
{context}"""),
    ("human", "{question}"),
])


def format_docs(docs: List[Document]) -> str:
    """将检索到的文档拼接成上下文字符串"""
    formatted = []
    for i, doc in enumerate(docs):
        formatted.append(f"[资料{i+1}，来源：{doc.metadata.get('source', 'unknown')}]\n{doc.page_content}")
    return "\n\n".join(formatted)


# LCEL 方式构建 RAG 链
rag_chain = (
    {
        "context": retriever | format_docs,   # 检索 → 格式化
        "question": RunnablePassthrough(),     # 原样传递问题
    }
    | rag_prompt
    | llm
    | StrOutputParser()
)


# ==================== Step 6: 测试 ====================
if __name__ == "__main__":
    test_questions = [
        "什么是 AI Agent？",
        "RAG 的流程包含哪些阶段？",
        "LangChain 有哪些核心模块？",
        "Function Calling 是如何工作的？",
        "今天天气怎么样？",  # 测试"知识库没有的信息"的处理
    ]

    for q in test_questions:
        print(f"\n{'='*60}")
        print(f"👤 问题：{q}")

        # 查看检索到了哪些 chunk
        docs = retriever.invoke(q)
        print(f"🔍 检索到 {len(docs)} 个相关片段：")
        for i, doc in enumerate(docs):
            print(f"  [{i}] {doc.page_content[:80]}...")

        # 生成回答
        answer = rag_chain.invoke(q)
        print(f"✅ 回答：{answer}")

"""
============================================================
📝 练习任务：
  1. 运行代码，观察每个问题的检索结果和最终回答
  2. 修改 chunk_size 为 100 和 500，对比检索质量
  3. 把 retriever 的 k 改为 1 和 5，观察回答质量变化（k=1可能丢信息，k=5可能引入噪声）
  4. 添加自己的文档（如：你简历中的项目描述），测试检索效果
  5. 实现"混合检索"：同时用相似度检索 + 关键词检索

💡 关键理解（面试重点）：
  RAG 效果不好的排查顺序：
  1. 检索前：Query 本身是否表述清楚？
  2. 检索中：切块是否过碎？Embedding 是否合适？Top-K 是否合理？
  3. 检索后：上下文是否过长？噪声是否淹没了关键信息？
============================================================
"""
