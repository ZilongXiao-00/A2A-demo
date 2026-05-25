import argparse
import asyncio
import warnings

from google.adk.agents import SequentialAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.runners import InMemoryRunner


warnings.filterwarnings("ignore", category=UserWarning, module="google.adk")
warnings.filterwarnings("ignore", category=UserWarning, module="__main__")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="__main__")


DEFAULT_AGENTS = [
    ("math_agent", 9999, "Remote A2A math agent"),
    ("code_agent", 9998, "Remote A2A coding agent"),
    ("translator_agent", 9997, "Remote A2A translation agent"),
    ("summarizer_agent", 9996, "Remote A2A summarization and planning agent"),
]


async def run(prompt: str, host: str) -> list[str]:
    remote_agents = []
    for name, port, description in DEFAULT_AGENTS:
        agent = RemoteA2aAgent(
            name=name,
            agent_card=f"http://{host}:{port}/.well-known/agent.json",
            description=description,
        )
        remote_agents.append(agent)
        print(f"[OK] {name} initialized on port {port}")

    root_agent = SequentialAgent(
        name="root_agent",
        description="Run several remote A2A agents in sequence.",
        sub_agents=remote_agents,
    )
    print(f"[OK] {root_agent.name} initialized")

    runner = InMemoryRunner(root_agent)
    events = await runner.run_debug(prompt, quiet=True)
    responses: list[str] = []
    for event in events:
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if getattr(part, "text", None):
                    responses.append(part.text)
    return responses


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the ADK remote A2A demo.")
    parser.add_argument("--host", default="localhost")
    parser.add_argument(
        "--prompt",
        default=(
            "First calculate sqrt(5), then write Python code for it, translate the final "
            "answer into Chinese, and summarize the result."
        ),
    )
    args = parser.parse_args()

    responses = asyncio.run(run(args.prompt, args.host))
    print("\nFinal ADK Response")
    print("-" * 18)
    print("\n\n".join(responses) if responses else "No final text response received.")


if __name__ == "__main__":
    main()
