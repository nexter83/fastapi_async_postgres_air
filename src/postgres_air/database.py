from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from postgres_air.config import settings

user = settings.POSTGRES_USER
password = settings.POSTGRES_PASSWORD
host = settings.POSTGRES_HOST
port = settings.DATABASE_PORT
db = settings.POSTGRES_DB

ASYNC_SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL, echo=True)
schema_engine = engine.execution_options(schema_translate_map={None: db})
async_session = sessionmaker(
    schema_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session


def get_session():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'options': '-csearch_path={}'.format(db)})
    session = Session(bind=engine.connect())
    try:
        yield session
    finally:
        session.close()
