from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.database.models import get_db
from app.api.schemas.agent import (
    AgentCreateSchema,
    AgentSchema,
)
from app.api.service.agent import AgentService
from app.logger import logger

log = logger.get_logger(__name__)

router = APIRouter()
agent_service = AgentService()


@router.get("", response_model=List[AgentSchema])
async def manage_agents(db: Session = Depends(get_db)):
    """
    Get all agents endpoint.
    """
    log.info("Getting all agents")
    db_agents = agent_service.get_agents(db)
    log.info(f"Agents: {db_agents}")

    return db_agents


@router.post("", response_model=AgentSchema)
async def create_agent(agent: AgentCreateSchema, db: Session = Depends(get_db)):
    """
    Create an agent endpoint.
    """
    log.info(f"Creating agent: {agent.json()}")
    db_agent = agent_service.create_agent(db, agent)
    log.info(f"Agent created with id: {db_agent.id}")

    return db_agent
