from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
import os
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Literal, Optional, List
import json
from .clinical_agent import clinical_node
from .exim_agent import exim_node
from .iqvia_agent import iqvia_node
from .patent_agent import patent_node
from .web_agent import web_node
from .master import graph
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_key)
class State(BaseModel):
    user_input : str 
    route : Optional[str]= None
    subtasks : Optional[List[str]] = None
    exim : Optional[str] = None
    iqvia : Optional[str] = None
    web : Optional[str] = None
    clinical : Optional[str] = None
    patent : Optional[str] = None
    response : Optional[str] = None

def orchestrator_node(state: State):
    if not state.subtasks:
        return {"response" : "NO AGENTS SELECTED BY MASTER AGENT"}
    return {"__next__": state.subtasks}

graph.add_node("iqvia", iqvia_node)
graph.add_node("exim", exim_node)
graph.add_node("web", web_node)
graph.add_node("clinical", clinical_node)
graph.add_node("patent", patent_node)
graph.add_edge("web", END)
graph.add_edge("iqvia", END)
graph.add_edge("exim", END)
graph.add_edge("clinical", END)
graph.add_edge("patent", END)

