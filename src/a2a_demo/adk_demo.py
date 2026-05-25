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
    ("math_agent", 9999, "远程 A2A 数学 Agent"),
    ("code_agent", 9998, "远程 A2A 编程 Agent"),
    ("translator_agent", 9997, "远程 A2A 翻译 Agent"),
    ("summarizer_agent", 9996, "远程 A2A 总结和规划 Agent"),
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
        print(f"[OK] {name} 已在端口 {port} 初始化")

    root_agent = SequentialAgent(
        name="root_agent",
        description="按顺序运行多个远程 A2A Agent。",
        sub_agents=remote_agents,
    )
    print(f"[OK] {root_agent.name} 已初始化")

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
    parser = argparse.ArgumentParser(description="运行 ADK 远程 A2A 多 Agent 示例。")
    parser.add_argument("--host", default="localhost")
    parser.add_argument(
        "--prompt",
        default=(
            "先计算根号 5，再写出对应 Python 代码，然后把最终答案翻译成中文，最后总结结果。"
        ),
    )
    args = parser.parse_args()

    responses = asyncio.run(run(args.prompt, args.host))
    print("\n最终 ADK 响应")
    print("-" * 18)
    print("\n\n".join(responses) if responses else "没有收到最终文本响应。")


if __name__ == "__main__":
    main()
