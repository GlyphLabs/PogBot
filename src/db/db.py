from __future__ import annotations
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import BigInteger, Integer, Column
from os import environ
from cachetools import TTLCache
from ormsgpack import packb, unpackb

Base = declarative_base()
engine = create_async_engine(url=environ["DATABASE_URL"])
session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class MsgPackMixin:
    def serialize(self):
        return packb({c.name: getattr(self, c.name) for c in self.__table__.columns})

    @classmethod
    def from_data(cls, data):
        return cls(**unpackb(data))

class EconomyData(Base, MsgPackMixin):  # type: ignore
    __tablename__ = "economy"
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    wallet = Column(Integer, nullable=False, default=0)
    bank = Column(Integer, nullable=False, default=0)
    bank_capacity = Column(Integer, nullable=False, default=0)
    cache: TTLCache = TTLCache(maxsize=100, ttl=60)

    @classmethod
    async def update_wallet(cls, id: int, wallet_amount: int) -> None:
        r = await cls.get(id)
        async with session() as s:
            r.wallet += wallet_amount
            await s.commit()
            cls.cache[id] = r.serialize()

    @classmethod
    async def get(cls, id: int) -> EconomyData:
        if id in cls.cache:
            return cls.from_data(cls.cache[id])
        query = select(cls).where(cls.id == id)
        async with session() as s:
            results = await s.execute(query)
            if not (result := results.first()):
                d = EconomyData(id=id, wallet=0, bank=0, bank_capacity=20000)
                s.add(d)
                await s.commit()
                cls.cache[id] = d.serialize()
                return d
            
            cls.cache[id] = result[0].serialize()

        return result[0]

    @classmethod
    async def update_bank(cls, id: int, bank_amount: int) -> None:
        async with session() as s:
            eco = await cls.get(id)
            eco.bank = bank_amount
            await s.commit()
            cls.cache[id] = eco.serialize()

    @classmethod
    async def update_bank_capacity(cls, id: int, bank_capacity: int) -> None:
        async with session() as s:
            eco = await cls.get(id)
            eco.bank_capacity = bank_capacity
            await s.commit()
            cls.cache[id] = eco.serialize()

    @classmethod
    async def withdraw(cls, id: int, amount: int) -> None:
        async with session() as s:
            eco = await cls.get(id)
            eco.wallet += amount
            eco.bank -= amount
            await s.commit()
            cls.cache[id] = eco.serialize()

    @classmethod
    async def deposit(cls, id: int, amount: int) -> None:
        async with session() as s:
            eco = await cls.get(id)
            eco.wallet -= amount
            eco.bank += amount
            await s.commit()
            cls.cache[id] = eco.serialize()

    def __repr__(self):
        return f"<EconomyData(id={self.id})>"


class GuildSettings(Base):  # type: ignore
    __tablename__ = "guild_settings"
    guild_id = Column(BigInteger, primary_key=True)
    chatbot_channel = Column(BigInteger)

    @classmethod
    async def update_chatbot_channel(cls, guild_id: int, channel_id: int):
        async with session() as s:
            await s.merge(GuildSettings(guild_id=guild_id, chatbot_channel=channel_id))
            await s.commit()

    @classmethod
    async def get(cls, guild_id: int):
        query = select(cls).where(cls.guild_id == guild_id)
        async with session() as s:
            results = await s.execute(query)
            if not (result := results.first()):
                return None
        return result[0]

    def __repr__(self):
        return f"<GuildSettings(guild_id={self.guild_id})>"
