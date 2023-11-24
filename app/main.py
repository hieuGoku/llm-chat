from fastapi import FastAPI, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from app.api.routes.api import app as api_router
from app.logger.logger import custom_logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Logging All API Requests"""

    async def dispatch(self, request, call_next: RequestResponseEndpoint) -> Response:
        custom_logger.info(
            f"Request: {request.method} {request.url} {request.client.host}"
        )
        response = await call_next(request)
        custom_logger.info("Response status code: %s", response.status_code)
        return response


app = FastAPI()
app.add_middleware(LoggingMiddleware)
app.include_router(router=api_router)


@app.get("/")
async def root():
    return {"message": "Welcome to LLM Chat!"}
