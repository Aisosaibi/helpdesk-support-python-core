from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.database import create_db_and_tables

from app.controllers import ticket_controller, user_controller


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Helpdesk Ticket System", lifespan=lifespan)

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(ticket_controller.router)
app.include_router(user_controller.router)