from a2a_demo.agent_server import AgentDefinition, run_agent
from a2a_demo.llm_client import call_llm


DEFINITION = AgentDefinition(
    name="SummarizerPlannerAgent",
    description="总结长文本，并把杂乱需求整理成可执行计划。",
    skill_id="summarize-plan",
    skill_name="总结与规划",
    skill_description="总结文档、提取行动项，并生成简洁的实施计划。",
    tags=["总结", "规划", "分析"],
    examples=["总结这段会议纪要。", "把这个想法整理成三步计划。"],
    system_prompt=(
        "你是一个总结和规划助手。请把杂乱输入压缩成清晰要点。"
        "当用户要求计划时，请给出有序步骤、风险和验收标准。"
    ),
    default_port=9996,
    temperature=0.4,
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
