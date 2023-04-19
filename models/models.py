from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, DECIMAL, select, Boolean, BigInteger, SmallInteger, \
    TIMESTAMP
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, join

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

    @classmethod
    @create_async_session
    async def join(cls, right: Base, session: AsyncSession = None, **kwargs) -> list[tuple[Base, Base]]:
        return await session.execute(join(left=cls, right=right).filter_by(**kwargs))


class Category(BaseMixin, Base):
    __tablename__: str = 'categories'

    name = Column(VARCHAR(32), nullable=False, unique=True)
    is_published = Column(Boolean, default=True)

    def __str__(self):
        return self.name


class Role(BaseMixin, Base):
    __tablename__: str = 'roles'

    id = Column(SmallInteger, primary_key=True)
    role = Column(VARCHAR(10), unique=True, nullable=False)

    def __str__(self):
        return self.role

    async def users(self) -> list['User']:
        return await User.all(role_id=self.id)


class User(BaseMixin, Base):
    __tablename__: str = 'users'

    id = Column(BigInteger, primary_key=True)
    name = Column(VARCHAR(128), nullable=False)
    role_id = Column(SmallInteger, ForeignKey('roles.id', ondelete='NO ACTION'), nullable=True)

    def __str__(self):
        return self.id


class Start(BaseMixin, Base):
    __tablename__: str = 'start'

    id = Column(SmallInteger, primary_key=True)
    name = Column(VARCHAR(128), nullable=False)
    is_published = Column(Boolean, default=True, nullable=True)


class Text(BaseMixin, Base):
    __tablename__: str ='texts'

    id = Column(SmallInteger, primary_key=True)
    text = Column(VARCHAR(256), nullable=False)
    is_published = Column(Boolean, default=True, nullable=True)

# cоздать класс basket для заказов и выбрвть реплай