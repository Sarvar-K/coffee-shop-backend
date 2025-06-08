from sqlalchemy import MetaData, Column, BigInteger
from sqlalchemy.orm import declarative_base

from core import configs

ModelBase = declarative_base(metadata=MetaData(schema=configs.POSTGRES_SCHEMA))


class AbstractModel(ModelBase):
    __tablename__ = None
    __abstract__ = True

    id = Column(BigInteger, primary_key=True)
