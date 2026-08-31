from fastapi import FastAPI
from app.database import create_db_and_tables
from app.controllers.user_controller import router as user_router

app = FastAPI(title="Helpdesk Ticket System")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(user_router)
