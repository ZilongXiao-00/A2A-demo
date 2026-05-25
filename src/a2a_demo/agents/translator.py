from a2a_demo.agent_server import AgentDefinition, run_agent
from a2a_demo.llm_client import call_llm


DEFINITION = AgentDefinition(
    name="TranslatorAgent",
    description="在保留含义、语气和格式的前提下翻译文本。",
    skill_id="translate-text",
    skill_name="文本翻译",
    skill_description="在中英文之间翻译文本，或根据用户请求推断目标语言。",
    tags=["翻译", "语言"],
    examples=["把这段话翻译成英文。", "把这句话翻译成自然的中文。"],
    system_prompt=(
        "你是一个专业翻译。请保留原文含义、语气、数字和格式。"
        "如果用户没有明确目标语言，请根据请求推断。除非用户要求解释，否则只返回译文。"
    ),
    default_port=9997,
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
