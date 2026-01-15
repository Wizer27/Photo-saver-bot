from sqlalchemy import select,exc 
from database.models import metadata_obj,table
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from datetime import datetime,timedelta
from typing import List,Optional
from sqlalchemy.orm import sessionmaker
import asyncpg
import os
from dotenv import load_dotenv
import asyncio
import atexit
import uuid


load_dotenv()



async_engine = create_async_engine(
    f"postgresql+asyncpg://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@localhost:5432/photo_saver_def",
    pool_size=20,           
    max_overflow=50,       
    pool_recycle=3600,      
    pool_pre_ping=True,     
    echo=False
)


AsyncSessionLocal = sessionmaker(
    async_engine, 
    class_=AsyncSession,
    expire_on_commit=False
)

async def create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata_obj.create_all)

async def get_all_data() -> List:
    async with AsyncSession(async_engine) as conn:
        try:
            stmt = select(table)
            res = await conn.execute(stmt)
            return list(res.fetchall())
        except exc.SQLAlchemyError:
            raise exc.SQLAlchemyError("Error while executing")

async def is_user_exists(username:str) -> bool:
    async with AsyncSession(async_engine) as conn:
        try:
            stmt = select(table.c.username).where(table.c.username == username)
            res = await conn.execute(stmt)
            data = res.scalar_one_or_none()
            if data is not None:
                return data == username
            return False
        except exc.SQLAlchemyError:
            raise exc.SQLAlchemyError("Error while executing")        

async def create_user(user_id:str) -> bool:
    if await is_user_exists(user_id):
        return False 
    async with AsyncSession(async_engine) as conn:
        async with conn.begin():
            try:
                stmt = table.insert().values(
                    username = user_id,
                    sub = False
                )
                await conn.execute(stmt)
            except exc.SQLAlchemyError:
                raise exc.SQLAlchemyError("Error while executing")

async def subscribe(username:str) -> bool:
    if not await is_user_exists(username):
        return False
    async with AsyncSession(async_engine) as conn:
        async with conn.begin():
            try:
                stmt = table.update().where(table.c.username == username).values(sub = True)
                await conn.execute(stmt)
                return True
            except exc.SQLAlchemyError:
                raise exc.SQLAlchemyError("Error while executing")

async def is_user_subbed(username:str) -> bool:
    async with AsyncSession(async_engine) as conn:
        try:
            stmt = select(table.c.sub).where(table.c.username == username)
            res = await conn.execute(stmt)
            data = res.scalar_one_or_none()
            if data is not None:
                return data
            raise NameError("User not found") # поидеи никогда не произойдет 
        except exc.SQLAlchemyError as conn:
            raise exc.SQLAlchemyError("Error while executing")            



        