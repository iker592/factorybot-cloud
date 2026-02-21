# Architecture

## Agent Structure

```
factorybot-cloud/
├── factorybot_cloud/
│   ├── __init__.py        # Package init
│   ├── agent.py           # Agent definition + tools
│   └── .env               # API key (not committed)
├── docs/                  # MkDocs documentation
├── mkdocs.yml             # Docs configuration
└── .gitignore
```

## How It Works

FactoryBot uses the Google ADK `Agent` class with Gemini 2.5 Flash as the reasoning model. The agent has access to Python function tools that simulate factory system integrations.

```
User Query → ADK Agent → Gemini 2.5 Flash → Tool Selection → Tool Execution → Response
```

## Multi-Agent Expansion

ADK supports multi-agent orchestration. Future architecture could include:

- **Monitor Agent** - continuous production line monitoring
- **Dispatch Agent** - routes requests to specialized sub-agents
- **Maintenance Agent** - predictive maintenance scheduling
- **Supply Chain Agent** - inventory optimization with MCP tool integrations

These can be orchestrated using ADK's `SequentialAgent`, `ParallelAgent`, or LLM-driven delegation.
