from typing import Optional

from pydantic import BaseModel, PositiveInt

from app.schemas.base_db import BaseDB


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationDB(DonationCreate, BaseDB):
    user_id: int
