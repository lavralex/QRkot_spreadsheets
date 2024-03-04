from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.schemas.base_db import BaseDB
from app.core.constants import (
    MAX_CHARITY_NAME_LENGTH,
    MIN_CHARITY_NAME_LENGTH,
    MIN_DESCRIPTION_LENGTH
)


class CharityProjectCreate(BaseModel):
    name: str = Field(
        min_length=MIN_CHARITY_NAME_LENGTH,
        max_length=MAX_CHARITY_NAME_LENGTH
    )
    description: str = Field(min_length=MIN_DESCRIPTION_LENGTH)
    full_amount: PositiveInt


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        min_length=MIN_CHARITY_NAME_LENGTH,
        max_length=MAX_CHARITY_NAME_LENGTH
    )
    description: Optional[str] = Field(min_length=MIN_DESCRIPTION_LENGTH)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate, BaseDB):
    pass