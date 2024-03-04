from datetime import datetime as dt

from sqlalchemy import Column, Integer, Boolean, DateTime, CheckConstraint

from app.core.db import Base
from app.core.constants import INVESTED_DEFAULT


class BaseModel(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint(
            'full_amount > 0',
            name='full_amount_greater_zero'
        ),
        CheckConstraint(
            'invested_amount >= 0',
            name='invested_amount_zero_or_greater'
        )
    )

    id = Column(Integer, primary_key=True)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=INVESTED_DEFAULT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=dt.now)
    close_date = Column(DateTime, nullable=True)
