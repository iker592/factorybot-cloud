# Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                          GITHUB                                     │
│                                                                     │
│  iker592/factorybot-cloud                                           │
│  ┌──────────────┐    ┌──────────────┐                               │
│  │ deploy.yml   │    │  docs.yml    │                               │
│  │ (Cloud Run)  │    │ (GH Pages)  │                               │
│  └──────┬───────┘    └──────┬───────┘                               │
│         │ push to main      │ push to main (docs/)                  │
└─────────┼───────────────────┼───────────────────────────────────────┘
          │                   │
          ▼                   ▼
┌──────────────────┐  ┌─────────────────┐
│  GOOGLE CLOUD    │  │  GITHUB PAGES   │
│  (Cloud Run)     │  │                 │
│                  │  │  MkDocs Material│
│                  │  │  iker592.github │
│                  │  │  .io/factorybot │
│                  │  └─────────────────┘
│                  │
│  ┌────────────────────────────────────┐
│  │         Cloud Run Service          │
│  │      (scale 0 → 20 instances)     │
│  │                                    │
│  │  ┌──────────────────────────────┐  │
│  │  │        FastAPI (app.py)      │  │
│  │  │                              │  │
│  │  │  ┌────────────────────────┐  │  │
│  │  │  │  SessionMiddleware     │  │  │
│  │  │  │  ┌──────────────────┐  │  │  │
│  │  │  │  │  AuthMiddleware  │  │  │  │
│  │  │  │  │                  │  │  │  │
│  │  │  │  │  /login ─────────┼──┼──┼──┼─── Public
│  │  │  │  │  /auth/google ───┼──┼──┼──┼──► Google OAuth2
│  │  │  │  │  /auth/callback ◄┼──┼──┼──┼─── Google OAuth2
│  │  │  │  │  /logout ────────┼──┼──┼──┼─── Public
│  │  │  │  │                  │  │  │  │
│  │  │  │  │  /dev-ui/ ───────┼──┼──┼──┼─── Protected
│  │  │  │  │  /run_sse ───────┼──┼──┼──┼─── Protected
│  │  │  │  └──────────────────┘  │  │  │
│  │  │  └────────────────────────┘  │  │
│  │  └──────────────────────────────┘  │
│  │                                    │
│  │  ┌──────────────────────────────┐  │
│  │  │   ADK Agent (factorybot)     │  │
│  │  │   Model: Gemini 2.5 Flash    │  │
│  │  │                              │  │
│  │  │   Tools:                     │  │
│  │  │   ├─ get_system_status()     │  │
│  │  │   └─ create_work_order()     │  │
│  │  └──────────────┬───────────────┘  │
│  └─────────────────┼──────────────────┘
│                    │
│  Secrets:          │
│  ├─ Secret Manager │
│  │  (OAuth secret) │
│  └─ Env vars       │
│    (API keys)      │
└────────────────────┼──────────────────
                     │
                     ▼
          ┌─────────────────────┐
          │   Gemini API        │
          │   (Vertex AI)       │
          │                     │
          │   gemini-2.5-flash  │
          └─────────────────────┘
```

## Request Flow

```
User ──► Cloud Run (any URL)
           │
           ├─ Non-canonical host?
           │  └─► Redirect to canonical host
           │
           ├─ No session cookie?
           │  └─► /login ──► Google OAuth2 ──► /auth/callback ──► set cookie
           │
           └─ Authenticated?
              └─► /dev-ui/ ──► ADK Web UI
                    │
                    └─► User sends message
                         │
                         └─► ADK Agent ──► Gemini 2.5 Flash
                              │                    │
                              │◄── tool calls ◄────┘
                              │
                              └─► Response to user
```

## Key Components

| Component | Role |
|---|---|
| **Cloud Run** | Serverless container, scales to zero when idle |
| **FastAPI** | Wraps ADK with session + auth middleware (LIFO order) |
| **Google OAuth2** | Via Authlib, canonical host redirect for multi-URL support |
| **ADK Agent** | Gemini 2.5 Flash with 2 factory tools |
| **CI/CD** | Auto-deploy on push to main, docs auto-publish to GitHub Pages |
| **Secret Manager** | OAuth client secret stored securely, API keys via env vars |

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

## Multi-Agent Expansion

ADK supports multi-agent orchestration. Future architecture could include:

- **Monitor Agent** - continuous production line monitoring
- **Dispatch Agent** - routes requests to specialized sub-agents
- **Maintenance Agent** - predictive maintenance scheduling
- **Supply Chain Agent** - inventory optimization with MCP tool integrations

These can be orchestrated using ADK's `SequentialAgent`, `ParallelAgent`, or LLM-driven delegation.
