from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel


class BaseDB(BaseModel):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: dt
    close_date: Optional[dt]

    class Config:
        orm_mode = True