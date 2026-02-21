# FactoryBot Cloud

AI-powered factory operations agent built with [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) and deployed serverless on Cloud Run.

## What it does

FactoryBot is an intelligent assistant that helps factory operators:

- **Monitor production lines** - check assembly line status, efficiency, and daily output
- **Track inventory** - view stock levels and low-stock alerts
- **Quality control** - monitor defect rates and threshold warnings
- **Work orders** - create and manage factory floor tasks with priority levels

## Tech Stack

| Component | Technology |
|---|---|
| Agent Framework | Google ADK 1.25.1 |
| Model | Gemini 2.5 Flash |
| Runtime | Cloud Run (serverless) |
| Language | Python 3.13 |

## Quick Start

```bash
# Clone and setup
git clone https://github.com/iker592/factorybot-cloud.git
cd factorybot-cloud
uv venv .venv --python 3.13
source .venv/bin/activate
uv pip install google-adk

# Configure API key
echo 'GOOGLE_API_KEY="your-key"' > factorybot_cloud/.env

# Run locally
adk web --port 8080
```

Then open [http://localhost:8080](http://localhost:8080) and select `factorybot_cloud`.
