from fastapi import FastAPI
from app.database import Base, engine

app = FastAPI(title="Helpdesk Ticket System")


@app.get("/health")
def health_check():
    """Sanity check — confirms the app boots and responds."""
    return {"status": "ok"}

Base.metadata.create_all(bind=engine)
