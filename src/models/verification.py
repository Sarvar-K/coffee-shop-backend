from datetime import datetime

from sqlalchemy import Column, DateTime, BigInteger, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship

from db.base_models import AbstractModel


class Otp(AbstractModel):
    __tablename__ = 'otp'

    created_at = Column(DateTime, default=datetime.now, index=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False, index=True)
    code = Column(String(6), index=True, nullable=False)

    user = relationship('User')

    __table_args__ = (
        UniqueConstraint('code', 'user_id', name='unique_otp_code_user_id'),
    )
