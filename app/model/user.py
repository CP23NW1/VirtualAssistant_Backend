from pydantic import BaseModel


class UserMessage(BaseModel):
    id_user: str
    role: str
    message: str
