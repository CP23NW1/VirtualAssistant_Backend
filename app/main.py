from fastapi import FastAPI
from azure_openai import generate_message
from pydantic import BaseModel
from uvicorn import main


class UserMessage(BaseModel):
    role: str
    message: str


app = FastAPI()


@app.post("/api/user_message")
async def root(message: UserMessage):
    text = generate_message(str(message))
    return {"content": text}


if __name__ == "__main__":
    app.run()
