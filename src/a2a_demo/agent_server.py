import argparse
from collections.abc import Callable
from dataclasses import dataclass

import uvicorn
from a2a.server.agent_execution import AgentExecutor
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from a2a.utils import new_agent_text_message


@dataclass(frozen=True)
class AgentDefinition:
    name: str
    description: str
    skill_id: str
    skill_name: str
    skill_description: str
    tags: list[str]
    examples: list[str]
    system_prompt: str
    default_port: int
    temperature: float = 0.7


class LLMBackedAgent:
    def __init__(
        self,
        definition: AgentDefinition,
        llm_caller: Callable[[str, str, float], str],
    ) -> None:
        self.definition = definition
        self.llm_caller = llm_caller

    def run(self, query: str) -> str:
        return self.llm_caller(
            query,
            self.definition.system_prompt,
            self.definition.temperature,
        )


class LLMBackedAgentExecutor(AgentExecutor):
    def __init__(self, agent: LLMBackedAgent) -> None:
        self.agent = agent

    async def execute(self, context, event_queue) -> None:
        prompt = context.get_user_input()
        response = self.agent.run(prompt)
        await event_queue.enqueue_event(new_agent_text_message(response))

    async def cancel(self, context, event_queue) -> None:
        return None


def build_app(
    definition: AgentDefinition,
    host: str,
    port: int,
    llm_caller: Callable[[str, str, float], str],
):
    skill = AgentSkill(
        id=definition.skill_id,
        name=definition.skill_name,
        description=definition.skill_description,
        tags=definition.tags,
        examples=definition.examples,
    )
    agent_card = AgentCard(
        name=definition.name,
        description=definition.description,
        url=f"http://{host}:{port}/",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=False),
        skills=[skill],
    )
    request_handler = DefaultRequestHandler(
        agent_executor=LLMBackedAgentExecutor(
            LLMBackedAgent(definition=definition, llm_caller=llm_caller)
        ),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )
    return server.build()


def run_agent(definition: AgentDefinition, llm_caller: Callable[[str, str, float], str]) -> None:
    parser = argparse.ArgumentParser(description=f"Run {definition.name}.")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=definition.default_port)
    args = parser.parse_args()
    uvicorn.run(
        build_app(definition, args.host, args.port, llm_caller),
        host=args.host,
        port=args.port,
    )
