from a2a_demo.agent_server import AgentDefinition, run_agent
from a2a_demo.llm_client import call_llm


DEFINITION = AgentDefinition(
    name="SummarizerPlannerAgent",
    description="Summarizes long text and turns messy requests into practical plans.",
    skill_id="summarize-plan",
    skill_name="Summarize and Plan",
    skill_description="Summarize documents, extract action items, and create concise implementation plans.",
    tags=["summary", "planning", "analysis"],
    examples=["Summarize this meeting note.", "Turn this idea into a three-step plan."],
    system_prompt=(
        "You are a summarization and planning assistant. Compress noisy input into clear takeaways. "
        "When the user asks for a plan, provide ordered steps, risks, and acceptance criteria."
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

