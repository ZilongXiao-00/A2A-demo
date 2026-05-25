# A2A Demo

这是一个轻量级 Agent2Agent (A2A) 协议示例项目，用来演示如何把本地 LLM Agent 封装成标准 A2A Server，并通过 A2A Client 或 Google ADK 的 `RemoteA2aAgent` 调用这些远程 Agent。

项目使用 OpenAI-compatible Chat Completions API，因此不绑定具体模型厂商。只要你的模型服务兼容 OpenAI Chat Completions 接口，就可以通过 `config.json` 或环境变量接入。

## 项目结构

```text
.
├── config.example.json
├── requirements.txt
├── pyproject.toml
└── src/a2a_demo
    ├── agent_server.py      # 通用 A2A Server 封装
    ├── llm_client.py        # 通用 LLM 调用封装
    ├── client.py            # 直接调用单个 A2A Agent 的客户端
    ├── adk_demo.py          # 使用 ADK 调用多个 A2A Agent 的示例
    └── agents
        ├── math.py          # 数学 Agent，默认端口 9999
        ├── code.py          # 编程 Agent，默认端口 9998
        ├── translator.py    # 翻译 Agent，默认端口 9997
        └── summarizer.py    # 总结/规划 Agent，默认端口 9996
```

## 从 0 开始运行

### 1. 创建环境

```powershell
conda create -y -n A2A python=3.11
conda activate A2A
pip install -e .
```

如果不想使用 editable install，也可以安装依赖后临时设置 `PYTHONPATH`：

```powershell
pip install -r requirements.txt
$env:PYTHONPATH="src"
```

### 2. 配置模型

方式一：使用本地配置文件。

```powershell
copy config.example.json config.json
```

然后把 `config.json` 改成你的 OpenAI-compatible API 配置：

```json
{
  "base_url": "https://api.example.com",
  "api_key": "your-api-key",
  "model": "your-model-name"
}
```

方式二：使用环境变量。

```powershell
$env:LLM_BASE_URL="https://api.example.com"
$env:LLM_API_KEY="your-api-key"
$env:LLM_MODEL="your-model-name"
```

环境变量优先级高于 `config.json`。本地真实配置文件 `config.json` 已经被 `.gitignore` 忽略，不会提交到仓库。

## 启动四个 A2A Agent 服务

分别打开四个终端，每个终端都先进入项目目录并激活环境：

```powershell
cd D:\Projects\Personal\A2A-agent
conda activate A2A
```

终端一启动数学 Agent：

```powershell
python -m a2a_demo.agents.math
```

终端二启动编程 Agent：

```powershell
python -m a2a_demo.agents.code
```

终端三启动翻译 Agent：

```powershell
python -m a2a_demo.agents.translator
```

终端四启动总结/规划 Agent：

```powershell
python -m a2a_demo.agents.summarizer
```

四个服务启动后，对应关系如下：

| Agent 模块 | 默认端口 | Agent 名称 | 能力 |
| --- | ---: | --- | --- |
| `a2a_demo.agents.math` | 9999 | `MathAgent` | 数学计算和推理 |
| `a2a_demo.agents.code` | 9998 | `CodeAgent` | 代码编写、解释、审查 |
| `a2a_demo.agents.translator` | 9997 | `TranslatorAgent` | 中英文翻译 |
| `a2a_demo.agents.summarizer` | 9996 | `SummarizerPlannerAgent` | 总结、提取要点、生成计划 |

## 直接调用单个 Agent

启动任意一个 Agent 后，可以用项目自带的 A2A Client 调用它。例如调用数学 Agent：

```powershell
python -m a2a_demo.client --port 9999 --prompt "1000 以内有多少个质数？"
```

调用编程 Agent：

```powershell
python -m a2a_demo.client --port 9998 --prompt "写一个 Python factorial 函数。"
```

调用翻译 Agent：

```powershell
python -m a2a_demo.client --port 9997 --prompt "Translate to English: A2A 让 Agent 之间可以通过标准协议通信。"
```

调用总结/规划 Agent：

```powershell
python -m a2a_demo.client --port 9996 --prompt "把这个任务拆成三步：启动服务、读取 Agent Card、发送 A2A 消息。"
```

直接调用单个 Agent 的过程是：

1. `client.py` 根据 `--host` 和 `--port` 连接远程 A2A Server。
2. `ClientFactory.connect()` 会读取该服务暴露的 Agent Card。
3. `create_text_message_object()` 把你的 `--prompt` 封装成 A2A 消息。
4. `client.send_message()` 把消息发给对应 Agent 服务。
5. Agent 服务中的 `AgentExecutor.execute()` 取出用户输入，调用本地 Agent 逻辑。
6. 本地 Agent 通过 `llm_client.call_llm()` 调用配置好的 LLM。
7. 服务把 LLM 输出封装成 A2A message/artifact 返回给客户端。

## 使用 ADK 调用四个服务

确保四个 Agent 服务都已经启动，然后在第五个终端运行：

```powershell
cd D:\Projects\Personal\A2A-agent
conda activate A2A
python -m a2a_demo.adk_demo
```

你也可以传入自己的任务：

```powershell
python -m a2a_demo.adk_demo --prompt "先计算根号 5，再写 Python 代码，然后翻译成中文，最后总结。"
```

### ADK 调用链路

`src/a2a_demo/adk_demo.py` 中有一个 `DEFAULT_AGENTS` 列表：

```python
DEFAULT_AGENTS = [
    ("math_agent", 9999, "远程 A2A 数学 Agent"),
    ("code_agent", 9998, "远程 A2A 编程 Agent"),
    ("translator_agent", 9997, "远程 A2A 翻译 Agent"),
    ("summarizer_agent", 9996, "远程 A2A 总结和规划 Agent"),
]
```

这个列表决定了 ADK demo 会连接哪些远程服务，以及连接顺序。当前示例使用的是 `SequentialAgent`，所以它不是自动路由，而是按列表顺序依次调用：

1. 先调用 `math_agent`，也就是端口 `9999` 的数学服务。
2. 再调用 `code_agent`，也就是端口 `9998` 的编程服务。
3. 再调用 `translator_agent`，也就是端口 `9997` 的翻译服务。
4. 最后调用 `summarizer_agent`，也就是端口 `9996` 的总结/规划服务。

每个远程 Agent 是这样创建的：

```python
agent = RemoteA2aAgent(
    name=name,
    agent_card=f"http://{host}:{port}/.well-known/agent.json",
    description=description,
)
```

这里最关键的是 `agent_card` 参数。它告诉 ADK：这个远程 Agent 的 Agent Card 在哪里。ADK 会访问：

```text
http://localhost:9999/.well-known/agent.json
http://localhost:9998/.well-known/agent.json
http://localhost:9997/.well-known/agent.json
http://localhost:9996/.well-known/agent.json
```

读到 Agent Card 后，ADK 就知道每个远程 Agent 的名称、描述、输入输出模式、技能和服务地址。然后 `SequentialAgent` 会把用户输入交给第一个远程 Agent，再把执行过程中的结果继续交给后续远程 Agent。

### 哪一步决定调用哪个 Agent

当前 demo 里，决定调用哪个 Agent 的位置是 `adk_demo.py` 的这段代码：

```python
root_agent = SequentialAgent(
    name="root_agent",
    description="按顺序运行多个远程 A2A Agent。",
    sub_agents=remote_agents,
)
```

`remote_agents` 来自 `DEFAULT_AGENTS`。因为使用的是 `SequentialAgent`，所以调用策略是固定顺序调用，不会根据意图动态选择。如果你只想调用某一个 Agent，可以直接用 `client.py` 指定端口；如果你想让模型根据任务自动选择 Agent，需要把 `SequentialAgent` 换成带路由能力的编排方式，例如自己写一个 router agent，根据用户意图选择目标端口或目标 `RemoteA2aAgent`。

## Agent Card 在哪里

Agent Card 不是手写 JSON 文件，而是在服务启动时由代码动态生成。

每个 Agent 模块都会定义一个 `DEFINITION`，例如数学 Agent 在 `src/a2a_demo/agents/math.py`：

```python
DEFINITION = AgentDefinition(
    name="MathAgent",
    description="解决数学计算和推理任务。",
    skill_id="math-calc",
    skill_name="数学计算",
    skill_description="解决算术、代数和分步骤数学推理任务。",
    tags=["数学", "推理", "计算"],
    examples=["1000 以内有多少个质数？", "根号 5 等于多少？"],
    system_prompt="...",
    default_port=9999,
)
```

通用封装在 `src/a2a_demo/agent_server.py` 的 `build_app()` 函数中。它会把 `AgentDefinition` 转换成 A2A SDK 的 `AgentSkill` 和 `AgentCard`：

```python
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
```

随后 `A2AStarletteApplication` 会把这个 `agent_card` 暴露为标准发现地址：

```text
GET /.well-known/agent.json
```

所以当你启动数学 Agent 后，可以直接打开：

```text
http://localhost:9999/.well-known/agent.json
```

启动其他 Agent 后，也可以分别查看：

```text
http://localhost:9998/.well-known/agent.json
http://localhost:9997/.well-known/agent.json
http://localhost:9996/.well-known/agent.json
```

## A2A Server 是如何包装已有 Agent 的

如果你已经有一个自己的 Agent，比如：

```python
class MyAgent:
    def run(self, user_input: str) -> str:
        return "result"
```

要接入 A2A，不需要重写内部逻辑，只需要加一层适配：

1. 定义 `AgentDefinition`，描述这个 Agent 的名称、能力、示例和端口。
2. 实现一个本地调用函数，把用户输入传给已有 Agent。
3. 调用 `run_agent(definition, llm_caller)` 或仿照 `LLMBackedAgentExecutor` 写自己的 executor。
4. executor 从 `context.get_user_input()` 读取 A2A 输入。
5. executor 调用已有 Agent 的 `run()` 方法。
6. executor 用 `new_agent_text_message()` 把结果转成 A2A 响应。
7. `A2AStarletteApplication` 暴露 Agent Card 和 A2A JSON-RPC endpoint。

本项目的四个示例 Agent 都复用了同一个封装层，因此新增 Agent 通常只需要新增一个 `src/a2a_demo/agents/*.py` 文件，填写 `DEFINITION` 和 `main()` 即可。

## 版本说明

当前依赖锁定为：

```text
a2a-sdk[http-server]==0.3.26
google-adk==2.1.0
```

原因是 `google-adk==2.1.0` 的 `RemoteA2aAgent` 仍依赖 `a2a-sdk` 0.3.x 的部分导出结构；直接安装最新 `a2a-sdk` 1.x 可能导致导入错误。这个版本组合已经在本 demo 中验证可用。

## 安全提示

- 不要提交真实 API key。
- 如果密钥曾经出现在公开提交、日志或聊天记录中，请立刻轮换。
- 生产环境请增加认证、限流、日志脱敏、超时控制和权限隔离。
