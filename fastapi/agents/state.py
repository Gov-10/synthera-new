from pydantic import BaseModel
from typing import List, Optional
class State(BaseModel):
    user_input: str
    route : Optional[str] = None
    subtasks : Optional[List[str]] = None
    iqvia: Optional[str] = None
    exim : Optional[str] = None
    web : Optional[str] = None
    clinical: Optional[str] = None
    patent : Optional[str] = None
    internal : Optional[str] = None
    response: Optional[str] = None
