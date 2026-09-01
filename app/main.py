from fastapi import FastAPI

from app.controllers import  comment_controller

app = FastAPI(
    title="HelpDesk Support System",
    description= "Our HelpDesk Support System coming through soon",
    version="Unlimited"
)


app.include_router(comment_controller.router)

@app.get("/")
def read_root():
    return {"message": "HelpDesk support system API is up and running"}

