from datetime import datetime
from pydantic import BaseModel


class MessageBaseSchema(BaseModel):
    """Base schema for Message objects."""

    user_message: str
    agent_message: str


class MessageCreateSchema(MessageBaseSchema):
    """Schema for creating Message objects."""

    pass


class MessageSchema(MessageBaseSchema):
    """Schema for Message objects."""

    id: str
    timestamp: datetime = datetime.utcnow()
    conversation_id: str

    class Config:
        orm_mode = True


class UserMessageSchema(BaseModel):
    """Base schema for UserMessage objects."""

    conversation_id: str
    message: str
