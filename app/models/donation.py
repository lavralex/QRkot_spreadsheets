from sqlalchemy import Column, Text, ForeignKey, Integer

from app.models.base_model import BaseModel


class Donation(BaseModel):
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
