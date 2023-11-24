from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, ForeignKey, String, DateTime, JSON
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime


SQLALCHEMY_DATABASE_URL = "sqlite:///agents.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Agent(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    context = Column(String, nullable=False)
    first_message = Column(String, nullable=False)
    response_shape = Column(JSON, nullable=False)
    instructions = Column(String, nullable=False)

    conversations = relationship("Conversation", back_populates="agent")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("agents.id"))
    timestap = Column(DateTime, default=datetime.utcnow)

    agent = relationship("Agent", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user_message = Column(String)
    agent_message = Column(String)

    conversation_id = Column(String, ForeignKey("conversations.id"))
    conversation = relationship("Conversation", back_populates="messages")


Base.metadata.create_all(bind=engine)
