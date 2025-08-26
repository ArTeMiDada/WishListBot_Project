from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from config import user, password, host, nameDB

engine = create_async_engine(url=f"mysql+aiomysql://{user}:{password}@{host}/{nameDB}")

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)
    reg_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    user: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Wish(Base):
    __tablename__ = 'wishes'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    cost: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(String(140))
    category: Mapped[int] = mapped_column(ForeignKey("categories.id"))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
