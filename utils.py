from pydantic import BaseModel, datetime_parse
from datetime import datetime

class Message(BaseModel):
    role: str
    content: str


