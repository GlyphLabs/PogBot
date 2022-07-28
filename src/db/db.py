from sqlalchemy import BigInteger, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from os import environ

Base = declarative_base()
engine = create_async_engine(url=environ["DATABASE_URL"])
session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class EconomyData(Base):  # type: ignore
    __tablename__ = "economy"
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    wallet = Column(Integer)
    bank = Column(Integer)
    bank_capacity = Column(Integer)

    @classmethod
    async def update_wallet(cls, id: int, new_amount: int) -> None:
        async with session() as s:
            await s.merge(EconomyData(id=id, wallet=new_amount))

    @classmethod
    async def get(cls, id: int):
        query = select(cls).where(cls.id == id)
        async with session() as s:
            results = await s.execute(query)
            if not results:
                d = EconomyData(id=id, wallet=0, bank=0, bank_capacity=20000)
                s.add()
                await s.commit()
                return EconomyData(id=id, wallet=0, bank=0, bank_capacity=20000)

        result = results.one()
        return result[0] if result else None

    @classmethod
    async def update_bank(cls, id: int, amt_to_add: int) -> None:
        async with session() as s:
            await s.execute(
                cls.update().where(cls.id == id).values(bank=cls.bank + amt_to_add)
            )

    @classmethod
    async def update_bank_capacity(cls, id: int, amt_to_add: int) -> None:
        async with session() as s:
            await s.execute(
                cls.update()
                .where(cls.id == id)
                .values(bank_capacity=cls.bank_capacity + amt_to_add)
                .on_conflict_do_nothing(index_elements=["id"])
            )

    def __repr__(self):
        return f"<EconomyData(id={self.id})>"


class GuildSettings(Base):  # type: ignore
    __tablename__ = "guild_settings"
    guild_id = Column(BigInteger, primary_key=True)
    chatbot_channel = Column(BigInteger)

    @classmethod
    async def update_chatbot_channel(cls, guild_id: int, channel_id: int):
        async with session() as s:
            await s.merge(
                GuildSettings(guild_id=guild_id, chatbot_channel=channel_id)
            )
            await s.commit()

    @classmethod
    async def get(cls, guild_id: int):
        query = select(cls).where(cls.guild_id == guild_id)
        async with session() as s:
            results = await s.execute(query)
        result = results.one()
        return result

    def __repr__(self):
        return f"<GuildSettings(guild_id={self.guild_id})>"
