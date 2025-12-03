from ninja import Schema
from typing import Optional, List
class InputSchema(Schema):
    text: str
    molecule : Optional[str]  = None
    tasks : Optional[List[str]] = None
    region : Optional[str] = None
    timeframe : Optional[int] = 5


class GetSignedUrl(Schema):
    file_name: str
    content_type : str
