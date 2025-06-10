from datetime import datetime

from sqlalchemy import Column, String, BigInteger, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from db.base_models import AbstractModel


class UserRole(AbstractModel):
    __tablename__ = 'user_role'

    ADMIN_ALIAS = 'admin'
    CLIENT_ALIAS = 'client'

    alias = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(300), nullable=False)


class User(AbstractModel):
    __tablename__ = 'user'

    created_at = Column(DateTime, default=datetime.now, index=True, nullable=False)
    edited_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    role_id = Column(BigInteger, ForeignKey('user_role.id'), nullable=False, index=True)
    phone_number = Column(String(32), index=True, unique=True, nullable=False)
    username = Column(String(128), index=True, unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=True)

    role = relationship('UserRole')

    @property
    def role_alias(self):
        return self.role.alias
