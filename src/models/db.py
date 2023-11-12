from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4

Base = declarative_base()


class User(Base):  # pylint: disable=missing-class-docstring
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    username = Column(String, index=True, unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_admin = Column(Boolean(), default=False)
    # tvtime_accounts = relationship("TvTimeAccount", back_populates="owner")


# class TvTimeAccount(Base):  # pylint: disable=missing-class-docstring
#     __tablename__ = "tvtime_accounts"

#     id = Column(Integer, primary_key=True, index=True)
#     owner_id = Column(UUID, ForeignKey("users.id"))
#     tvtime_username = Column(String, index=True, unique=True)

#     owner = relationship("User", back_populates="tvtime_accounts")
