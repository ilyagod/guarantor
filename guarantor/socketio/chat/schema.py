from datetime import datetime

from pydantic import BaseModel


class ChatMessageSchema(BaseModel):
    user_id: int
    message: str
    created_at: datetime

    class Config:
        orm_mode = True


class RequestChatMessageSchema(BaseModel):
    user_id: int
    message: str
