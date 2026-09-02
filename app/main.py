from fastapi import FastAPI
from app.database import create_db_and_tables
from app.controllers import ticket_controller, user_controller, auth_controller, comment_controller

create_db_and_tables()

app = FastAPI(title="Helpdesk Ticket System")

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(ticket_controller.router)
app.include_router(comment_controller.router)
