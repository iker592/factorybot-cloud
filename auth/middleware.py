from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse

PUBLIC_PATHS = {"/", "/login", "/auth/google", "/auth/callback", "/logout"}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        user = request.session.get("user")
        if not user:
            return RedirectResponse("/login", status_code=303)

        return await call_next(request)
