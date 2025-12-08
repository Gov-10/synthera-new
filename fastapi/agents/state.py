from pydantic import BaseModel
from typing import List, Optional
class State(BaseModel):
    user_email : Optional[str] = None
    user_id: Optional[str] = None
    user_input: str
    route : Optional[str] = None
    subtasks : Optional[List[str]] = None
    iqvia: Optional[dict] = None
    exim : Optional[dict] = None
    web : Optional[str] = None
    clinical: Optional[dict] = None
    patent : Optional[dict] = None
    internal : Optional[str] = None
    report : Optional[str] = None
    pdf_s3_key : Optional[str] = None
    pdf_url : Optional[str] = None 
    response: Optional[str] = None
