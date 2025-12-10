from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from fastapi import Query, Depends
import os
from datetime import datetime
from dotenv import load_dotenv
import uuid

load_dotenv()
class User(SQLModel, table=True):
    email: str = Field(primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    chat_history: List["ChatHistory"] = Relationship(back_populates="user")

class ChatHistory(SQLModel, table=True):
    id : str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_email
