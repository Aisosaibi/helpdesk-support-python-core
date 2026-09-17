from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_db_and_tables
from app.controllers import ticket_controller, user_controller, auth_controller, comment_controller

create_db_and_tables()

app = FastAPI(title="Helpdesk Ticket System")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(ticket_controller.router)
app.include_router(comment_controller.router)
