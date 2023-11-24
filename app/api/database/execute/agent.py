import uuid
from sqlalchemy.orm import Session
from app.api.database import models
from app.api.schemas.agent import AgentCreateSchema


def get_agents(db: Session):
    """
    Get all agents
    """
    return db.query(models.Agent).all()


def get_agent(db: Session, agent_id: str):
    """
    Get an agent by its id
    """
    return db.query(models.Agent).filter(models.Agent.id == agent_id).first()


def create_agent(db: Session, agent: AgentCreateSchema):
    """
    Create an agent in the database
    """
    db_agent = models.Agent(
        id=str(uuid.uuid4()),
        context=agent.context,
        first_message=agent.first_message,
        response_shape=agent.response_shape,
        instructions=agent.instructions,
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)

    return db_agent
