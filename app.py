import os

from dotenv import load_dotenv

load_dotenv(os.path.join("agents", "factorybot_cloud", ".env"))

from google.adk.cli.fast_api import get_fast_api_app
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse

from auth.middleware import AuthMiddleware
from auth.oauth import setup_oauth_routes

app = get_fast_api_app(
    agents_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents"),
    web=True,
    allow_origins=["*"],
    host="0.0.0.0",
    port=8080,
)

# LIFO order: AuthMiddleware added first so it runs inside SessionMiddleware
app.add_middleware(AuthMiddleware)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "dev-secret-change-me"),
    session_cookie="adk_session",
    max_age=3600 * 24 * 7,
    same_site="lax",
    https_only=os.getenv("ENV", "dev") == "production",
)

setup_oauth_routes(app)


LOGIN_HTML = """<!DOCTYPE html>
<html>
<head>
  <title>FactoryBot Cloud - Sign In</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #0f0f0f;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
    }
    .card {
      background: #1a1a1a;
      border: 1px solid #333;
      border-radius: 16px;
      padding: 48px;
      text-align: center;
      max-width: 400px;
      width: 100%;
    }
    h1 { font-size: 24px; margin-bottom: 8px; }
    p { color: #888; margin-bottom: 32px; font-size: 14px; }
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 12px;
      background: #fff;
      color: #000;
      padding: 12px 24px;
      border-radius: 8px;
      text-decoration: none;
      font-size: 15px;
      font-weight: 500;
      transition: background 0.2s;
    }
    .btn:hover { background: #e0e0e0; }
    .btn svg { width: 20px; height: 20px; }
  </style>
</head>
<body>
  <div class="card">
    <h1>FactoryBot Cloud</h1>
    <p>Sign in to access the agent dashboard</p>
    <a href="/auth/google" class="btn">
      <svg viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
      Sign in with Google
    </a>
  </div>
</body>
</html>"""


@app.get("/login")
async def login_page():
    return HTMLResponse(LOGIN_HTML)


@app.get("/")
async def root(request: Request):
    user = request.session.get("user")
    if user:
        return HTMLResponse(
            f'<meta http-equiv="refresh" content="0;url=/dev-ui/">'
        )
    return HTMLResponse(
        '<meta http-equiv="refresh" content="0;url=/login">'
    )
