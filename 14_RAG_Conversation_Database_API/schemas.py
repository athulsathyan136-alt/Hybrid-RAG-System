from pydantic import BaseModel
from datetime import datetime


class QuestionRequest(BaseModel):

    question: str


class MessageResponse(BaseModel):

    id: int
    role: str
    message: str
    created_at: datetime

    class Config:

        from_attributes = True