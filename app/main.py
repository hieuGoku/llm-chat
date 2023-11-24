from fastapi import FastAPI
from app.api.routes.api import app as api_router
from app.logger.logger import setup_applevel_logger

log = setup_applevel_logger(file_name="agents.log")

app = FastAPI()
app.include_router(router=api_router)


@app.get("/")
async def root():
    return {"message": "Hello there conversational ai user!"}
