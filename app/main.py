from fastapi import FastAPI
from azure_openai import generate_message
from pydantic import BaseModel


class UserMessage(BaseModel):
    message: str


app = FastAPI()


@app.post("/api/user_message")
async def root(message: UserMessage):
    return generate_message(str(message))
