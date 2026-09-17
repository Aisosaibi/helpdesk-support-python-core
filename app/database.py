import os
from typing import Generator

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

# SQLite keeps local development and tests runnable without a separate server.
# Set DATABASE_URL to a MySQL URL when deploying with the production database.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./helpdesk.db")
engine_kwargs = {"echo": True}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_kwargs)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
