from fastapi import FastAPI
from app.azure_openai import generate_message
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


class UserMessage(BaseModel):
    role: str
    message: str


app = FastAPI()
origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/user_message")
async def root(message: UserMessage):
    text = generate_message(str(message))
    return {"content": text}


if __name__ == "__main__":
    app.run()
