from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.database.models import get_db
from app.api.schemas.conversation import ConversationSchema, ConversationCreateSchema
from app.api.service.conversation import ConversationService
from app.logger import logger

log = logger.get_logger(__name__)

router = APIRouter()
conversation_service = ConversationService()


@router.get("", response_model=List[ConversationSchema])
async def manage_conversations(agent_id: str, db: Session = Depends(get_db)):
    """
    Get all conversations for an agent endpoint.
    """
    log.info(f"Getting all conversations for agent id: {agent_id}")
    db_conversations = conversation_service.get_conversations(db, agent_id)
    log.info(f"Conversations: {db_conversations}")

    return db_conversations


@router.post("", response_model=ConversationSchema)
async def create_conversation(
    conversation: ConversationCreateSchema, db: Session = Depends(get_db)
):
    """
    Create a conversation linked to an agent
    """
    log.info(f"Creating conversation assigned to agent id: {conversation.agent_id}")
    db_conversation = conversation_service.create_conversation(db, conversation)
    log.info(f"Conversation created with id: {db_conversation.id}")

    return db_conversation
