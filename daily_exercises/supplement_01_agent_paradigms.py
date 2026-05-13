"""
Supplement 1 — Agent经典范式：Plan-and-Solve + Reflection
==========================================================
来源：hello-agents Ch4（hello-agents/code/chapter4/）
适配：使用你的 DeepSeek API 配置，无需额外安装框架

学习目标：
  1. 掌握 Plan-and-Solve 范式：先规划再执行（和 ReAct 的区别？）
  2. 掌握 Reflection 范式：执行→反思→优化 的自我纠错循环
  3. 能对比三种范式的适用场景（面试重点！）

三种范式对比：
  ReAct（已有 day02/day07）: Thought→Action→Observation 交替，适合路径不确定的任务
  Plan-and-Solve（本文件）:  先完整规划→再逐步执行，适合可分解的任务
  Reflection（本文件）:      执行→自我评审→优化，适合需要质量保证的任务
"""

import os
import re
import ast
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# ==================== LLM 客户端（同 EasyAgent 模式）====================

class LLMClient:
    """轻量 LLM 客户端 — 和你的 EasyAgent/demo2.py 完全一样的模式"""
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL"),
        )
        self.model = "deepseek-chat"

    def think(self, messages: list, temperature: float = 0) -> str:
        """调用 LLM，收集流式结果"""
        print(f"🧠 调用 {self.model}...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )
            collected = []
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    collected.append(content)
            print()
            return "".join(collected)
        except Exception as e:
            print(f"❌ LLM 调用失败: {e}")
            return None


# ==================== 工具定义（模拟计算器）====================

def calculator(expression: str) -> str:
    """安全的数学计算器"""
    try:
        expression = re.sub(r"[^0-9+\-*/().\s]", "", expression)
        if not expression.strip():
            return "错误：无效表达式"
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"计算错误：{e}"


# ================================================================
#  范式1：Plan-and-Solve（先规划，再执行）
# ================================================================
# 面试要点：
#  - 和 ReAct 的区别：Plan-Solve 是"想好再做"，ReAct 是"边想边做"
#  - 适用场景：任务可以提前分解为清晰步骤（如：多步数学题、数据处理）
#  - 局限：计划可能不准确，无法根据中间结果动态调整

PLANNER_PROMPT = """你是一个AI规划专家。请将用户的问题分解成多个简单步骤。
输出一个 Python 列表，每个元素是一个子任务。

问题: {question}

请严格按以下格式输出（```python 和 ``` 是必需的）:
```python
["步骤1", "步骤2", "步骤3"]
```
"""

EXECUTOR_PROMPT = """你是一个AI执行专家。请按照计划逐步解决问题。

# 原始问题: {question}
# 完整计划: {plan}
# 已完成步骤: {history}
# 当前步骤: {current_step}

请只输出当前步骤的答案，不要输出多余内容。
"""


class PlanAndSolveAgent:
    """Plan-and-Solve Agent：先规划完整计划，再逐步执行"""
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def plan(self, question: str) -> list:
        prompt = PLANNER_PROMPT.format(question=question)
        response = self.llm.think([{"role": "user", "content": prompt}]) or ""
        try:
            plan_str = response.split("```python")[1].split("```")[0].strip()
            plan = ast.literal_eval(plan_str)
            return plan if isinstance(plan, list) else []
        except Exception as e:
            print(f"❌ 解析计划失败: {e}")
            return []

    def execute(self, question: str, plan: list) -> str:
        history = ""
        final_answer = ""
        for i, step in enumerate(plan, 1):
            print(f"\n→ 步骤 {i}/{len(plan)}: {step}")
            prompt = EXECUTOR_PROMPT.format(
                question=question, plan=plan,
                history=history if history else "（尚无完成步骤）",
                current_step=step,
            )
            response = self.llm.think([{"role": "user", "content": prompt}]) or ""
            history += f"步骤{i}: {step}\n结果: {response}\n\n"
            final_answer = response
        return final_answer

    def run(self, question: str) -> str:
        print(f"\n{'='*50}\n📋 Plan-and-Solve Agent\n问题: {question}")
        plan = self.plan(question)
        if not plan:
            return "无法生成有效计划"
        print(f"📝 计划: {plan}")
        answer = self.execute(question, plan)
        print(f"\n✅ 最终答案: {answer}")
        return answer


# ================================================================
#  范式2：Reflection（执行 → 反思 → 优化）
# ================================================================
# 面试要点：
#  - 本质是"自我纠错循环"：生成 → 评审 → 优化 → 再评审
#  - 适用场景：代码生成、文案写作、需要质量保证的输出
#  - 关键设计：评审员的 Prompt 要针对具体维度（如仅关注性能、安全、风格）

INITIAL_PROMPT = """你是一位资深Python程序员。请根据要求编写代码。
要求: {task}
请直接输出代码，不要包含额外解释。
"""

REFLECT_PROMPT = """你是一位严格的代码评审专家。请审查以下代码的算法效率。

# 原始任务: {task}
# 待审查代码:
```python
{code}
```

请分析时间复杂度，并提出优化建议。
如果代码在算法层面已最优，请回答"无需改进"。
"""

REFINE_PROMPT = """你是一位资深Python程序员。请根据评审意见优化代码。

# 原始任务: {task}
# 上一版代码: {last_code}
# 评审意见: {feedback}

请直接输出优化后的代码。
"""


class ReflectionAgent:
    """Reflection Agent：生成 → 自我评审 → 优化，循环直到满意"""
    def __init__(self, llm: LLMClient, max_iterations: int = 2):
        self.llm = llm
        self.max_iterations = max_iterations

    def run(self, task: str) -> str:
        print(f"\n{'='*50}\n🪞 Reflection Agent\n任务: {task}")

        # Step 1: 初始生成
        print("\n--- 第1轮：初始生成 ---")
        code = self.llm.think([
            {"role": "user", "content": INITIAL_PROMPT.format(task=task)}
        ]) or ""
        print(f"📝 初始代码:\n{code[:200]}...")

        # Step 2: 反思-优化循环
        for i in range(self.max_iterations):
            print(f"\n--- 第{i+2}轮：反思与优化 ---")

            # 反思
            feedback = self.llm.think([
                {"role": "user", "content": REFLECT_PROMPT.format(task=task, code=code)}
            ]) or ""
            print(f"🔍 评审意见: {feedback[:150]}...")

            if "无需改进" in feedback:
                print("✅ 代码已达到最优，停止迭代")
                break

            # 优化
            code = self.llm.think([
                {"role": "user", "content": REFINE_PROMPT.format(
                    task=task, last_code=code, feedback=feedback
                )}
            ]) or ""
            print(f"🔄 优化后代码:\n{code[:200]}...")

        print(f"\n✅ 最终代码:\n{code}")
        return code


# ==================== 测试 ====================
if __name__ == "__main__":
    llm = LLMClient()

    # ---- 测试1: Plan-and-Solve ----
    print("\n" + "=" * 60)
    print("📋 测试1：Plan-and-Solve 范式")
    print("=" * 60)
    agent_ps = PlanAndSolveAgent(llm)
    agent_ps.run(
        "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。"
        "周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"
    )

    # ---- 测试2: Reflection ----
    print("\n" + "=" * 60)
    print("🪞 测试2：Reflection 范式")
    print("=" * 60)
    agent_rf = ReflectionAgent(llm, max_iterations=2)
    agent_rf.run("编写一个Python函数，找出1到n之间所有的素数(prime numbers)。")

    # ---- 测试3: 对比三种范式 ----
    print("\n" + "=" * 60)
    print("📊 三种范式对比总结")
    print("=" * 60)
    print("""
    ┌──────────────┬──────────────────────┬──────────────────────┐
    │ 范式         │ 核心逻辑             │ 适合场景             │
    ├──────────────┼──────────────────────┼──────────────────────┤
    │ ReAct        │ Thought→Action→Obs   │ 路径不确定，需动态   │
    │ (day02/07)   │ 边想边做，交替进行   │ 决策和调用工具       │
    ├──────────────┼──────────────────────┼──────────────────────┤
    │ Plan-Solve   │ 先完整规划→再逐步    │ 任务可预先分解，     │
    │ (本文件)     │ 执行，不回头改计划   │ 如多步数学/数据处理  │
    ├──────────────┼──────────────────────┼──────────────────────┤
    │ Reflection   │ 生成→自我评审→优化   │ 需要质量保证，       │
    │ (本文件)     │ 反复迭代直到满意     │ 如代码生成/文案创作  │
    └──────────────┴──────────────────────┴──────────────────────┘

    💡 面试话术（对比三种范式）：
    "ReAct 是 Agent 最基础的范式，模型边思考边行动，适合路径不确定的任务。
     Plan-and-Solve 先做完整规划再逐步执行，效率高但缺乏灵活性。
     Reflection 增加了自我纠错循环，通过评审→优化提升输出质量。
     在实际项目中，LangGraph 可以把三种范式组合成复杂的 Agent 工作流。"

    💡 hello-agents 最值得看的练习代码：
    1. code/chapter4/ReAct.py — 对比你的 EasyAgent/demo2.py（结构完全一致！）
    2. code/chapter4/Plan_and_solve.py — 规划和执行的分离设计
    3. code/chapter4/Reflection.py — 自我纠错循环（带 Memory 模块）
    4. code/chapter4/llm_client.py — LLM 客户端的封装模式（对比你的写法）
    5. code/chapter7/ — 自建框架完整实现（需 pip install helloagents）
    6. code/chapter8/10_RAG_Pipeline_Complete.py — 完整 RAG pipeline（856行）
    """)

"""
============================================================
📝 练习任务：
  1. 运行代码，观察 Plan-and-Solve 的计划生成和执行过程
  2. 运行 Reflection，观察代码如何通过评审被优化
  3. 修改 ReflectionAgent 的 REFLECT_PROMPT，
     让它关注"代码风格"而不是"算法效率"
  4. 思考：如果一个问题需要查天气 + 计算，三种范式分别怎么处理？
  5. 对比 hello-agents/code/chapter4/ReAct.py 和你的 EasyAgent/demo2.py

💡 面试重点 — 三种范式对比：
  - ReAct：路径不确定时要动态决策，调用工具获取信息
  - Plan-Solve：任务可分解为明确步骤时更高效
  - Reflection：需要保证输出质量时用自我纠错
  - 实际项目：LangGraph 图结构中通常组合使用多种范式
============================================================
"""
