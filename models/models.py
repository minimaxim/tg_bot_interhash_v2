from sqlalchemy import Column, Integer, VARCHAR, select, Boolean, BigInteger, SmallInteger
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

    id = Column(SmallInteger, primary_key=True)
    name = Column(VARCHAR(64), nullable=False, unique=True)
    is_published = Column(Boolean, default=True)

    def __str__(self):
        return self.name


class User(BaseMixin, Base):
    __tablename__: str = 'users'

    id = Column(BigInteger, primary_key=True)
    name = Column(VARCHAR(128), nullable=True)
    username = Column(VARCHAR(128), nullable=True)
    start_name = Column(VARCHAR(128), nullable=True)
    category_name = Column(VARCHAR(128), nullable=True)
    model_name = Column(VARCHAR(128), nullable=True)
    kolvo = Column(VARCHAR(128), nullable=True)
    call_me = Column(VARCHAR(128), nullable=True)
    discont = Column(VARCHAR(5), nullable=True)
    power = Column(VARCHAR(128), nullable=True)
    currency = Column(VARCHAR(5), nullable=True)
    coin = Column(VARCHAR(24), nullable=True)
    cost_electricity = Column(VARCHAR(128), nullable=True)
    hash = Column(VARCHAR(128), nullable=True)
    potreb = Column(VARCHAR(128), nullable=True)
    komm = Column(VARCHAR(128), nullable=True)
    promo = Column(VARCHAR(128), nullable=True)
    date = Column(VARCHAR(28), nullable=True)

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


class Power(BaseMixin, Base):
    __tablename__: str = 'powers'

    id = Column(SmallInteger, primary_key=True)
    name = Column(VARCHAR(128), nullable=False)
    is_published = Column(Boolean, default=True, nullable=True)


class Discont(BaseMixin, Base):
    __tablename__: str = 'disconts'

    id = Column(SmallInteger, primary_key=True)
    name = Column(VARCHAR(128), nullable=False)
    is_published = Column(Boolean, default=True, nullable=True)


class Promo(BaseMixin, Base):
    __tablename__: str = 'promocodes'

    id = Column(SmallInteger, primary_key=True)
    name = Column(VARCHAR(128), nullable=False)
    is_published = Column(Boolean, default=True, nullable=True)


class Application(BaseMixin, Base):
    __tablename__: str = 'aplications'

    id = Column(SmallInteger, primary_key=True)
    name = Column(VARCHAR(128), nullable=False)
    is_published = Column(Boolean, default=True, nullable=True)


class Admin(BaseMixin, Base):
    __tablename__: str = 'admin'

    id = Column(BigInteger, primary_key=True)
    name = Column(VARCHAR(32), nullable=False)
