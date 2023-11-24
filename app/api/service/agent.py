from sqlalchemy.orm import Session
from app.api.database.models import Agent
from app.api.schemas.agent import (
    AgentCreateSchema,
)
from app.api.database.execute import agent as agent_execute


class AgentService:
    """Agent service class"""

    @staticmethod
    def create_agent(db: Session, agent: AgentCreateSchema) -> Agent:
        db_agent = agent_execute.create_agent(db, agent)

        return db_agent

    @staticmethod
    def get_agent(db: Session, agent_id: str) -> Agent:
        db_agent = agent_execute.get_agent(db, agent_id)

        return db_agent

    @staticmethod
    def get_agents(db: Session) -> list:
        db_agents = agent_execute.get_agents(db)

        return db_agents
