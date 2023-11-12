from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from passlib.context import CryptContext
from loguru import logger

from sqlalchemy.exc import IntegrityError

from src.config import (
    SQLALCHEMY_DATABASE_URI,
    ADMIN_USERNAME,
    ADMIN_PASSWORD,
    TVTIME_TEST_USERNAME,
)
from src.models.api import UserOut
from src.models.db import Base, User


class PostgreSQLClient:
    def __init__(self, session: Session):
        self.session = session

    def get_user_out(self, username) -> UserOut:
        user = self.session.query(User).filter_by(username=username).first()
        if user is not None:
            return UserOut(user_id=user.id.hex, username=user.username, is_admin=user.is_admin, is_active=user.is_active)
        else:
            return None

    def get_user(self, username) -> User | None:
        return self.session.query(User).filter_by(username=username).first()

    def add_user(self, user: User):
        pass

    def close(self):
        self.session.close()


engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    session = session_maker()
    db_client = PostgreSQLClient(session)
    try:
        yield db_client
    finally:
        db_client.close()


def initilize_db():
    try:
        Base.metadata.create_all(engine)
        session = session_maker()
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(ADMIN_PASSWORD)
        try:
            user = User(username=ADMIN_USERNAME, hashed_password=hashed_password, is_admin=True)
            session.add(user)
            session.commit()
            session.close()
        except IntegrityError as exc:
            session.rollback()
            session.close()
            logger.debug("IntegrityError: {exc}", exc=exc)
    except Exception as exc:
        pass
