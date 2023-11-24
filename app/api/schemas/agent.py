from datetime import datetime
from typing import List
from pydantic import BaseModel
from app.api.schemas.conversation import ConversationSchema


class AgentBaseSchema(BaseModel):
    """Base schema for Agent objects."""

    context: str
    first_message: str
    response_shape: str
    instructions: str


class AgentCreateSchema(AgentBaseSchema):
    """Schema for creating Agent objects."""

    pass


class AgentSchema(AgentBaseSchema):
    """Schema for Agent objects."""

    id: str
    timestamp: datetime = datetime.utcnow()
    conversations: List[ConversationSchema] = []

    class Config:
        orm_mode = True


class ChatAgentResponseSchema(BaseModel):
    """Base schema for ChatAgentResponse objects."""

    conversation_id: str
    response: str
