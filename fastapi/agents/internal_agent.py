from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
import os
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Literal, Optional, List 
import json
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_key)
class State(BaseModel):
    user_input : str 
    route : Optional[Literal["orchestrator", "internal"]] = None 
    subtasks : Optional[List[str]] = None 
    response : Optional[str] = None 

def internal_node(state: State):
    return {"response" : "INTERNAL MODE ON"}
