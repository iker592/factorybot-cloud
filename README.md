# FactoryBot Cloud

AI-powered factory operations agent built with [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) and deployed serverless on Cloud Run with Google OAuth login.

## Links

| What | URL |
|---|---|
| Live Agent | https://factorybot-cloud-ayckui2y6q-uc.a.run.app |
| Dev UI | https://factorybot-cloud-ayckui2y6q-uc.a.run.app/dev-ui/ |
| Docs | https://iker592.github.io/factorybot-cloud/ |
| GCP Console | [Cloud Run Service](https://console.cloud.google.com/run/detail/us-central1/factorybot-cloud?project=gen-lang-client-0612021813) |

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
| Auth | Google OAuth2 via Authlib |
| Runtime | Cloud Run (serverless) |
| Docs | MkDocs Material + GitHub Pages |
| CI/CD | GitHub Actions |
| Language | Python 3.13 |

## Project Structure

```
factorybot-cloud/
├── agents/
│   └── factorybot_cloud/
│       ├── __init__.py
│       ├── agent.py            # Gemini 2.5 Flash agent + tools
│       └── .env                # Local API keys (gitignored)
├── auth/
│   ├── middleware.py            # Session-based route protection
│   └── oauth.py                # Google OAuth2 via Authlib
├── docs/                       # MkDocs documentation
├── .github/workflows/
│   ├── deploy.yml              # Cloud Run auto-deploy
│   └── docs.yml                # GitHub Pages auto-deploy
├── app.py                      # FastAPI wrapper with auth
├── Dockerfile
├── mkdocs.yml
└── requirements.txt
```

## Quick Start

```bash
# Clone and setup
git clone https://github.com/iker592/factorybot-cloud.git
cd factorybot-cloud
uv venv .venv --python 3.13
source .venv/bin/activate
uv pip install -r requirements.txt

# Configure environment
cat > agents/factorybot_cloud/.env << 'EOF'
GOOGLE_API_KEY="your-gemini-api-key"
GOOGLE_CLIENT_ID="your-oauth-client-id"
GOOGLE_CLIENT_SECRET="your-oauth-client-secret"
SESSION_SECRET_KEY="your-random-secret"
EOF

# Run locally
uvicorn app:app --host 0.0.0.0 --port 8080
```

Then open http://localhost:8080, sign in with Google, and select `factorybot_cloud`.

## GCP Setup

| Resource | Detail |
|---|---|
| Project | `gen-lang-client-0612021813` |
| Region | `us-central1` |
| Service | `factorybot-cloud` on Cloud Run |
| Secrets | `google-client-secret` in Secret Manager |
| OAuth | Configured in APIs & Services > Credentials |

## CI/CD

| Workflow | Trigger |
|---|---|
| **Deploy to Cloud Run** | Push to `main` (ignores docs-only changes) |
| **Deploy docs to GitHub Pages** | Push to `main` that touches `docs/` or `mkdocs.yml` |

### GitHub Secrets

`GCP_SA_KEY`, `GOOGLE_CLIENT_ID`, `SESSION_SECRET_KEY`, `GOOGLE_API_KEY` + `google-client-secret` via GCP Secret Manager.

## Auth Flow

1. User visits app -> middleware checks session cookie
2. No session -> redirect to `/login`
3. "Sign in with Google" -> Google OAuth2 consent
4. Callback -> set session cookie -> redirect to `/dev-ui/`
