from fastapi import FastAPI
from app.azure_openai import generate_message
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.model.user import UserMessage
from app.routers import auth, user


app = FastAPI()

# origins = [
#     "http://localhost:3000",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["Auth"], prefix="/api/auth")
app.include_router(user.router, tags=["Users"], prefix="/api/users")


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with MongoDB"}


@app.post("/api/user_message")
async def root(message: UserMessage):
    text = generate_message(str(message))
    return {"content": text}


if __name__ == "__main__":
    app.run()
