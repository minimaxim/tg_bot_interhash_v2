from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, select, Boolean, BigInteger, SmallInteger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base

from loader import DATABASE_URL

Base = declarative_base()


class BaseMixin(object):
    id = Column(Integer, primary_key=True)

    engine = create_async_engine(f'postgresql+asyncpg://{DATABASE_URL}')

    def __init__(self, **kwargs) -> None:
        for kw in kwargs.items():
            self.__getattribute__(kw[0])
            self.__setattr__(*kw)

    @staticmethod
    def create_async_session(func):
        async def wrapper(*args, **kwargs):
            async with AsyncSession(bind=BaseMixin.engine) as session:
                return await func(*args, **kwargs, session=session)

        return wrapper

    @create_async_session
    async def save(self, session: AsyncSession = None) -> None:
        session.add(self)
        await session.commit()
        await session.refresh(self)

    @classmethod
    @create_async_session
    async def get(cls, pk: int, session: AsyncSession = None) -> Base:
        return await session.get(cls, pk)

    @classmethod
    @create_async_session
    async def all(cls, order_by: str = 'id', session: AsyncSession = None, **kwargs) -> list[Base]:
        return [obj[0] for obj in await session.execute(select(cls).filter_by(**kwargs).order_by(order_by))]

    @create_async_session
    async def delete(self, session: AsyncSession = None) -> None:
        await session.delete(self)
        await session.commit()


class Category(BaseMixin, Base):
    __tablename__: str = 'categories'

    start_id = Column(SmallInteger, ForeignKey('start.id', ondelete='CASCADE'), nullable=False)
    name = Column(VARCHAR(64), nullable=False, unique=True)
    is_published = Column(Boolean, default=True)

    def __str__(self):
        return self.name


class Brand(BaseMixin, Base):
    __tablename__: str = 'brands'

    category_id = Column(SmallInteger, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    name = Column(VARCHAR(64), unique=True, nullable=False)
    is_published = Column(Boolean, default=True)


    def __str__(self):
        return self.name


class Model(BaseMixin, Base):
    __tablename__: str = 'models'

    brand_id = Column(SmallInteger, ForeignKey('brands.id', ondelete='CASCADE'), nullable=False)
    name = Column(VARCHAR(64), unique=True, nullable=False)
    is_published = Column(Boolean, default=True)

    def __str__(self):
        return self.name


class User(BaseMixin, Base):
    __tablename__: str = 'users'

    id = Column(BigInteger, primary_key=True)
    name = Column(VARCHAR(128), nullable=False)
    start_name = Column(VARCHAR(128), nullable=True)
    category_name = Column(VARCHAR(128), nullable=True)
    brand_name = Column(VARCHAR(128), nullable=True)
    model_name = Column(VARCHAR(128), nullable=True)
    currency = Column(VARCHAR(5), nullable=True)
    coin = Column(VARCHAR(24), nullable=True)
    cost_electricity = Column(VARCHAR(128), nullable=True)
    hash = Column(VARCHAR(128), nullable=True)
    potreb = Column(VARCHAR(128), nullable=True)
    komm = Column(VARCHAR(128), nullable=True)

    def __str__(self):
        return self.id


class Start(BaseMixin, Base):
    __tablename__: str = 'start'

    id = Column(SmallInteger, primary_key=True)
    name = Column(VARCHAR(128), nullable=False)
    is_published = Column(Boolean, default=True, nullable=True)


class Coin(BaseMixin, Base):
    __tablename__: str = 'coins'

    id = Column(SmallInteger, primary_key=True)
    name = Column(VARCHAR(128), nullable=False)
    is_published = Column(Boolean, default=True, nullable=True)


class Currency(BaseMixin, Base):
    __tablename__: str = 'currencies'

    id = Column(SmallInteger, primary_key=True)
    name = Column(VARCHAR(128), nullable=False)
    is_published = Column(Boolean, default=True, nullable=True)

