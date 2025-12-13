from ninja import Schema
from typing import Optional, List, Dict
from datetime import datetime
class InputSchema(Schema):
    text: str
    molecule : Optional[str]  = None
    tasks : Optional[List[str]] = None
    region : Optional[str] = None
    timeframe : Optional[int] = 5


class GetSignedUrl(Schema):
    file_name: str
    content_type : str

class ChatHistoryOut(Schema):
    id: str
    user_email: str
    file_key: str
    file_url: str
    data: Dict
    sources_links: List[str]
    timestamp: datetime