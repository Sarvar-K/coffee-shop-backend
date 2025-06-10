from datetime import datetime

from sqlalchemy import Column, DateTime, Boolean, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from db.base_models import AbstractModel


class Session(AbstractModel):
    __tablename__ = 'session'

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False, index=True)
    is_terminated = Column(Boolean, default=False, nullable=False)
    terminated_at = Column(DateTime, nullable=True)

    user = relationship('User')
