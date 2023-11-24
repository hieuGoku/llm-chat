from sqlalchemy.orm import Session
from typing import List
from app.api.schemas.message import (
    MessageSchema,
    MessageCreateSchema,
)
from app.api.database.execute import message as message_execute


class MessageService:
    """Chat service class"""

    @staticmethod
    def get_messages(db: Session, conversation_id: str) -> List[MessageSchema]:
        db_messages = message_execute.get_messages(db, conversation_id)

        return db_messages

    @staticmethod
    def create_conversation_message(
        db: Session,
        message: MessageCreateSchema,
        conversation_id: str,
    ) -> MessageSchema:
        db_message = message_execute.create_conversation_message(db, message, conversation_id)

        return db_message
