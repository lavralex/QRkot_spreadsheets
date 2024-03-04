from sqlalchemy import Column, String, Text

from app.models.base_model import BaseModel
from app.core.constants import MAX_CHARITY_NAME_LENGTH


class CharityProject(BaseModel):
    name = Column(
        String(MAX_CHARITY_NAME_LENGTH),
        unique=True,
        nullable=False
    )
    description = Column(
        Text,
        nullable=False
    )
