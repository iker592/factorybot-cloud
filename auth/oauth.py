import os

from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import RedirectResponse

oauth = OAuth()

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


def setup_oauth_routes(app: FastAPI):
    @app.get("/auth/google")
    async def auth_google(request: Request):
        canonical = os.getenv("CANONICAL_HOST")
        if canonical and request.url.hostname != canonical:
            return RedirectResponse(f"https://{canonical}/auth/google")
        redirect_uri = str(request.url_for("auth_callback"))
        if os.getenv("CANONICAL_HOST"):
            redirect_uri = redirect_uri.replace("http://", "https://")
        return await oauth.google.authorize_redirect(request, redirect_uri)

    @app.get("/auth/callback")
    async def auth_callback(request: Request):
        token = await oauth.google.authorize_access_token(request)
        userinfo = token.get("userinfo")
        if not userinfo:
            return RedirectResponse("/login")

        request.session["user"] = {
            "email": userinfo["email"],
            "name": userinfo.get("name", ""),
            "picture": userinfo.get("picture", ""),
        }
        return RedirectResponse("/dev-ui/")

    @app.get("/logout")
    async def logout(request: Request):
        request.session.clear()
        return RedirectResponse("/login")
