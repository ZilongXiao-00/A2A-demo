import argparse
import asyncio

import httpx
from a2a.client import Client, ClientConfig, ClientFactory, create_text_message_object
from a2a.types import Artifact, Message, Task
from a2a.utils.message import get_message_text


async def send_prompt(prompt: str, host: str, port: int) -> str:
    async with httpx.AsyncClient(timeout=100) as httpx_client:
        client: Client = await ClientFactory.connect(
            f"http://{host}:{port}/",
            client_config=ClientConfig(httpx_client=httpx_client),
        )
        agent_card = await client.get_card()
        print(f"Connected to {agent_card.name}: {agent_card.description}")
        print(f"Sending prompt: {prompt}")

        message = create_text_message_object(content=prompt)
        text_content = ""
        async for response in client.send_message(message):
            if isinstance(response, Message):
                print(f"Message ID: {response.message_id}")
                text_content = get_message_text(response)
            elif isinstance(response, tuple):
                task: Task = response[0]
                print(f"Task ID: {task.id}")
                if task.artifacts:
                    artifact: Artifact = task.artifacts[0]
                    print(f"Artifact ID: {artifact.artifact_id}")
                    text_content = get_message_text(artifact)
        return text_content


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a prompt to an A2A agent.")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=9999)
    parser.add_argument(
        "--prompt",
        default="How many prime numbers are less than 1000?",
        help="Prompt sent to the remote A2A agent.",
    )
    args = parser.parse_args()

    response = asyncio.run(send_prompt(args.prompt, args.host, args.port))
    print("\nFinal Agent Response")
    print("-" * 24)
    print(response or "No text response received.")


if __name__ == "__main__":
    main()

