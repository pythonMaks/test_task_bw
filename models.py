import asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy import MetaData, Table, select

DATABASE_URL = "postgresql+asyncpg://bewise:bewise@localhost/bewise"

async def fetch_table_content(table_name: str):
    engine = create_async_engine(DATABASE_URL, future=True)
    async with engine.begin() as conn:
        metadata = MetaData()
        await conn.run_sync(metadata.reflect)
        
        table = metadata.tables.get(table_name)
        if table is None:
            raise ValueError(f"Table {table_name} does not exist")

        result = await conn.execute(select(table))
        return result.fetchall()


table_name = "questions"  # Замените на имя вашей таблицы
content = asyncio.run(fetch_table_content(table_name))
for row in content:
    print(row)
