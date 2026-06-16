from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, Uuid
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL)
sessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()
class History(Base):
    __tablename__ = "history"
    id=Column(Integer, primary_key=True, index=True)
    timestamp=Column(DateTime, server_default=func.now(), onupdate=func.now())
    user=Column(String)
    file_key=Column(String, unique=True)
    content=Column(String, nullable=True)
    job_id=Column(Uuid)
    mode=Column(String, default="research_mode")





