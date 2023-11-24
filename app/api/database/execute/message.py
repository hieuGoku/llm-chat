import uuid
from sqlalchemy.orm import Session
from app.api.database import models
from app.api.schemas.message import MessageCreateSchema


def get_messages(db: Session, conversation_id: str):
    """
    Get all messages for a conversation
    """
    return (
        db.query(models.Message)
        .filter(models.Message.conversation_id == conversation_id)
        .all()
    )


def create_conversation_message(
    db: Session, message: MessageCreateSchema, conversation_id: str
):
    """
    Create a message for a conversation
    """
    db_message = models.Message(
        id=str(uuid.uuid4()),
        user_message=message.user_message,
        agent_message=message.agent_message,
        conversation_id=conversation_id,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return db_message
