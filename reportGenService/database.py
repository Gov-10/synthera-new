from sqlalchemy import create_engine, Column, String, DateTime, func, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
load_dotenv()
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL)
sessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()
class Reports(Base):
    __tablename__ = "reports"
    id=Column(Integer, primary_key=True, index=True)
    username=Column(String)
    timestamp=Column(DateTime,server_now=func.now(), onupdate=func.now())
    file_key=Column(String, unique=True)
Base.metadata.create_all(bind=engine)
SQLAlchemyInstrumentor().instrument(engine=engine)

