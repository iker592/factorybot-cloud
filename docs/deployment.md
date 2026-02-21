# Deployment

## Cloud Run (Current)

FactoryBot is deployed serverless on Google Cloud Run.

**Live URL:** `https://factorybot-cloud-379933901191.us-central1.run.app`

### Deploy from source

```bash
# Authenticate
gcloud auth login
gcloud config set project gen-lang-client-0612021813

# Enable APIs
gcloud services enable run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com

# Deploy
adk deploy cloud_run \
  --project gen-lang-client-0612021813 \
  --region us-central1 \
  --service_name factorybot-cloud \
  --with_ui \
  factorybot_cloud
```

### What happens under the hood

1. ADK generates a Dockerfile and packages your agent
2. Cloud Build creates a container image
3. Image is pushed to Artifact Registry
4. Cloud Run deploys the container with auto-scaling

### Configuration

| Setting | Value |
|---|---|
| Region | us-central1 |
| Port | 8000 |
| Scaling | 0 to N (scale to zero) |
| UI | Included (`--with_ui`) |

## Alternative: Vertex AI Agent Engine

For managed sessions, memory, and enterprise security, consider deploying to Agent Engine:

```bash
adk deploy agent_engine \
  --project gen-lang-client-0612021813 \
  --region us-central1 \
  --display_name "FactoryBot Cloud"
```

See the [ADK deployment docs](https://google.github.io/adk-docs/deploy/) for details.
