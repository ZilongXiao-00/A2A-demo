from a2a_demo.agent_server import AgentDefinition, run_agent
from a2a_demo.llm_client import call_llm


DEFINITION = AgentDefinition(
    name="MathAgent",
    description="解决数学计算和推理任务。",
    skill_id="math-calc",
    skill_name="数学计算",
    skill_description="解决算术、代数和分步骤数学推理任务。",
    tags=["数学", "推理", "计算"],
    examples=["1000 以内有多少个质数？", "根号 5 等于多少？"],
    system_prompt=(
        "你是一个严谨的数学助手。请清晰解决用户的数学问题，展示关键推理步骤，"
        "检查计算过程，并让最终答案容易找到。"
    ),
    default_port=9999,
    temperature=0.2,
)


def main() -> None:
    run_agent(
        DEFINITION,
        lambda query, system_prompt, temperature: call_llm(
            query,
            system_prompt=system_prompt,
            temperature=temperature,
        ),
    )


if __name__ == "__main__":
    main()
