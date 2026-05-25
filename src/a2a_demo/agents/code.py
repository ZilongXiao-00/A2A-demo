from a2a_demo.agent_server import AgentDefinition, run_agent
from a2a_demo.llm_client import call_llm


DEFINITION = AgentDefinition(
    name="CodeAgent",
    description="Writes, explains, and reviews small pieces of code.",
    skill_id="code-writing",
    skill_name="Code Writing",
    skill_description="Generate runnable code, explain implementation choices, and review simple snippets.",
    tags=["coding", "python", "review"],
    examples=["Write quicksort in Python.", "Review this function for bugs."],
    system_prompt=(
        "You are a pragmatic programming assistant. Provide runnable, concise code. "
        "Prefer Python when no language is specified. Mention assumptions and include brief usage notes."
    ),
    default_port=9998,
    temperature=0.3,
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

