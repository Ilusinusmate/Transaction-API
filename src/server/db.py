from contextlib import asynccontextmanager
from sqlmodel import create_engine, Session

from server.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)


async def get_session():
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e
    