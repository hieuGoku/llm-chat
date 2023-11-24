"""API Routes."""
from fastapi import APIRouter
from app.api.routes.agent import router as agent_route
from app.api.routes.conversation import router as conversation_route
from app.api.routes.message import router as message_route

app = APIRouter()

app.include_router(
    agent_route,
    prefix="/agents",
    tags=["Agents"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    conversation_route,
    prefix="/conversations",
    tags=["Conversations"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    message_route,
    prefix="/messages",
    tags=["Messages"],
    responses={404: {"description": "Not found"}},
)
