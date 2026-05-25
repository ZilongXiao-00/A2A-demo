from a2a_demo.agent_server import AgentDefinition, run_agent
from a2a_demo.llm_client import call_llm


DEFINITION = AgentDefinition(
    name="TranslatorAgent",
    description="Translates text while preserving meaning, tone, and formatting.",
    skill_id="translate-text",
    skill_name="Text Translation",
    skill_description="Translate text between Chinese and English, or infer the target language from the request.",
    tags=["translation", "language"],
    examples=["Translate this paragraph into English.", "把这句话翻译成自然的中文。"],
    system_prompt=(
        "You are a professional translator. Preserve the source meaning, tone, numbers, and formatting. "
        "If the target language is not specified, infer it from the user's request. Return only the translation "
        "unless the user asks for notes."
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

