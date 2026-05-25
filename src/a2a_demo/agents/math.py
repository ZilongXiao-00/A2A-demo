from a2a_demo.agent_server import AgentDefinition, run_agent
from a2a_demo.llm_client import call_llm


DEFINITION = AgentDefinition(
    name="MathAgent",
    description="Solves math calculation and reasoning tasks.",
    skill_id="math-calc",
    skill_name="Math Calculation",
    skill_description="Solve arithmetic, algebra, and step-by-step math reasoning tasks.",
    tags=["math", "reasoning", "calculation"],
    examples=["How many prime numbers are less than 1000?", "What is sqrt(5)?"],
    system_prompt=(
        "You are a careful math assistant. Solve the user's math problem clearly. "
        "Show the key reasoning steps, verify arithmetic, and keep the final answer easy to find."
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

