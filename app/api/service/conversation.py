from sqlalchemy.orm import Session
from app.api.database.models import Conversation
from app.api.schemas.conversation import ConversationSchema, ConversationCreateSchema
from app.api.database.execute import conversation as conversation_execute


class ConversationService:
    """Conversation service class"""

    @staticmethod
    def get_conversation(db: Session, conversation_id: str) -> ConversationSchema:
        db_conversation = conversation_execute.get_conversation(db, conversation_id)

        return db_conversation

    @staticmethod
    def get_conversations(db: Session, agent_id: str) -> ConversationSchema:
        db_conversations = conversation_execute.get_conversations(db, agent_id)

        return db_conversations

    @staticmethod
    def create_conversation(
        db: Session, conversation: ConversationCreateSchema
    ) -> Conversation:
        db_conversation = conversation_execute.create_conversation(db, conversation)

        return db_conversation
