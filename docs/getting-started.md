# Getting Started

## Prerequisites

- Python 3.10+ (3.13 recommended)
- [uv](https://docs.astral.sh/uv/) package manager
- Google Cloud account with billing enabled
- Gemini API key from [AI Studio](https://aistudio.google.com/app/apikey)

## Installation

```bash
git clone https://github.com/iker592/factorybot-cloud.git
cd factorybot-cloud

# Create virtual environment
uv venv .venv --python 3.13
source .venv/bin/activate

# Install dependencies
uv pip install google-adk
```

## Configuration

Create a `.env` file inside the `factorybot_cloud/` directory:

```bash
echo 'GOOGLE_API_KEY="your-gemini-api-key"' > factorybot_cloud/.env
```

## Running Locally

### Web UI (recommended for development)

```bash
adk web --port 8080
```

Open [http://localhost:8080](http://localhost:8080), select `factorybot_cloud` from the dropdown, and start chatting.

### CLI Mode

```bash
adk run factorybot_cloud
```

## Tools

FactoryBot comes with two built-in tools:

### `get_system_status(component)`

Check the status of factory components: `assembly_line`, `inventory`, or `quality_control`.

### `create_work_order(task, priority)`

Create work orders with priority levels: `low`, `normal`, `high`, or `critical`.
