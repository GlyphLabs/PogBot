from __future__ import annotations
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import BigInteger, Integer, Column
from os import environ
from cachetools import TTLCache
from ormsgpack import packb, unpackb
from typing import Optional

Base = declarative_base()
engine = create_async_engine(url=environ["DATABASE_URL"])
session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class MsgPackMixin:
    def serialize(self):
        return packb(
            {
                column.name: getattr(self, column.name)
                for column in self.__table__.columns
                if not column.name.startswith("_")
            }
        )

    @classmethod
    def from_data(cls, data):
        return cls(**unpackb(data))


class EconomyData(Base, MsgPackMixin):  # type: ignore
    __tablename__ = "economy"
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    wallet = Column(Integer, nullable=False, default=0)
    bank = Column(Integer, nullable=False, default=0)
    bank_capacity = Column(Integer, nullable=False, default=0)
    cache: TTLCache[int, bytes] = TTLCache(maxsize=100, ttl=60)

    @classmethod
    async def update_wallet(cls, id: int, wallet_amount: int) -> None:
        async with session() as s:
            results = await s.execute(select(cls).where(cls.id == id))
            record = results.one()[0]
            record.wallet = record.wallet + wallet_amount
            await s.commit()

            cls.cache[id] = record.serialize()

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
            results = await s.execute(select(cls).where(cls.id == id))
            record = results.one()[0]
            record.bank = record.bank + bank_amount
            await s.commit()

            cls.cache[id] = record.serialize()

    @classmethod
    async def update_bank_capacity(cls, id: int, bank_capacity: int) -> None:
        async with session() as s:
            results = await s.execute(select(cls).where(cls.id == id))
            record = results.one()[0]
            record.bank_capacity = record.bank_capacity + bank_capacity
            await s.commit()

            cls.cache[id] = record.serialize()

    @classmethod
    async def withdraw(cls, id: int, amount: int) -> None:
        async with session() as s:
            results = await s.execute(select(cls).where(cls.id == id))
            record = results.one()[0]
            record.wallet = record.wallet + amount
            record.bank = record.bank - amount
            await s.commit()

            cls.cache[id] = record.serialize()

    @classmethod
    async def deposit(cls, id: int, amount: int) -> None:
        async with session() as s:
            results = await s.execute(select(cls).where(cls.id == id))
            record = results.one()[0]
            record.wallet = record.wallet - amount
            record.bank = record.bank + amount
            await s.commit()

            cls.cache[id] = record.serialize()

    def __repr__(self):
        return f"<EconomyData(id={self.id})>"


class GuildSettings(Base, MsgPackMixin):  # type: ignore
    __tablename__ = "guild_settings"
    guild_id = Column(BigInteger, primary_key=True)
    chatbot_channel = Column(BigInteger)
    cache: TTLCache[int, bytes] = TTLCache(maxsize=100, ttl=60)

    @classmethod
    async def update_chatbot_channel(cls, guild_id: int, channel_id: int):
        g_settings = await cls.get(guild_id)
        async with session() as s:
            if not g_settings:
                s.add(GuildSettings(guild_id=guild_id, chatbot_channel=channel_id))
                await s.commit()
            else:
                async with session() as s:
                    results = await s.execute(
                        select(cls).where(cls.guild_id == guild_id)
                    )
                    record = results.one()[0]
                    record.chatbot_channel = channel_id
                    await s.commit()

                cls.cache[guild_id] = record.serialize()
                await s.commit()

    @classmethod
    async def get(cls, guild_id: int) -> Optional[GuildSettings]:
        if data := cls.cache.get(guild_id):
            return cls.from_data(data)
        query = select(cls).where(cls.guild_id == guild_id)
        async with session() as s:
            results = await s.execute(query)
            if not (result := results.first()):
                return None
            cls.cache[guild_id] = result[0].serialize()
        return result[0]

    def __repr__(self):
        return f"<GuildSettings(guild_id={self.guild_id})>"
