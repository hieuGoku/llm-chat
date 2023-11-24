import uuid
from sqlalchemy.orm import Session
from app.api.database import models
from app.api.schemas.conversation import ConversationCreateSchema


def get_conversation(db: Session, conversation_id: str):
    """
    Get a conversation by its id
    """
    return (
        db.query(models.Conversation)
        .filter(models.Conversation.id == conversation_id)
        .first()
    )


def get_conversations(db: Session, agent_id: str):
    """
    Get all conversations for an agent
    """
    return (
        db.query(models.Conversation)
        .filter(models.Conversation.agent_id == agent_id)
        .all()
    )


def create_conversation(db: Session, conversation: ConversationCreateSchema):
    """
    Create a conversation
    """
    db_conversation = models.Conversation(
        id=str(uuid.uuid4()),
        agent_id=conversation.agent_id,
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)

    return db_conversation