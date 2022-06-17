from fastapi import Depends
from fastapi import FastAPI
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from config import configer

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)


engine = create_async_engine(
    configer.get('DATABASE_URL'),
)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False,
)

app = FastAPI()


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@app.get('/')
async def root(session=Depends(get_session)):
    users = (await session.execute(select(User).limit(10))).scalars().all()
    return [x.email for x in users]
