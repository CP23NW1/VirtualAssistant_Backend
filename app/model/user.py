from pydantic import BaseModel


class UserMessage(BaseModel):
    role: str
    message: str
