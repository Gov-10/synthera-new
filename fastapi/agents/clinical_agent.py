from langgraph.graphs import StateGraph, END
from pydantic import BaseModel

class State(BaseModel):
    message: str
def clincal_node(state: State):
    return {}
