from typing import List, Optional

from pydantic import BaseModel

from app.schemas.charity_project import CharityProjectDB


class Googl(BaseModel):
    link: str
    message: Optional[str]
    projects: List[CharityProjectDB]
