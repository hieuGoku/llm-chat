from datetime import datetime
from pydantic import BaseModel


class ConversationBaseSchema(BaseModel):
    """Base schema for Conversation objects."""

    agent_id: str


class ConversationCreateSchema(ConversationBaseSchema):
    """Schema for creating Conversation objects."""

    pass


class ConversationSchema(ConversationBaseSchema):
    """Schema for Conversation objects."""

    id: str
    timestamp: datetime = datetime.utcnow()

    class Config:
        orm_mode = True
