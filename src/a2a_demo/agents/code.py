from a2a_demo.agent_server import AgentDefinition, run_agent
from a2a_demo.llm_client import call_llm


DEFINITION = AgentDefinition(
    name="CodeAgent",
    description="编写、解释和审查小段代码。",
    skill_id="code-writing",
    skill_name="代码编写",
    skill_description="生成可运行代码，解释实现选择，并审查简单代码片段。",
    tags=["编程", "Python", "代码审查"],
    examples=["用 Python 写快速排序。", "帮我检查这个函数有没有 bug。"],
    system_prompt=(
        "你是一个务实的编程助手。请提供可运行、简洁的代码。"
        "当用户没有指定语言时优先使用 Python。必要时说明假设，并给出简短使用说明。"
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
