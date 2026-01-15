from sqlalchemy import select,exc 
from database.files_database.files_models import metadata_obj,files_table
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
    f"postgresql+asyncpg://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@localhost:5432/photo_saver",
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
            stmt = select(files_table)
            res = await conn.execute(stmt)
            return list(res.fetchall())
        except exc.SQLAlchemyError:
            raise exc.SQLAlchemyError("Error while executing")

async def is_file_exists(file_id:str) -> bool:
    async with AsyncSession(async_engine) as conn:
        try:
            stmt = select(files_table.c.username).where(files_table.c.filedata == file_id)
            res = await conn.execute(stmt)
            data = res.scalar_one_or_none()
            if data is not None:
                return True
            return False
        except exc.SQLAlchemyError:
            raise exc.SQLAlchemyError("Error while executing")         

async def create_file(username:str,file_name:str,fileid:str):
    async with AsyncSession(async_engine) as conn:
        async with conn.begin():
            try:
                stmt = files_table.insert().values(
                    username = username,
                    filedata = fileid,
                    filename = file_name
                )
                await conn.execute(stmt)
            except exc.SQLAlchemyError:
                raise exc.SQLAlchemyError("Error while executing")       
  
async def delete_file(file_id:str) -> bool:
    if not await is_file_exists(file_id):
        return False     
    async with AsyncSession(async_engine) as conn:
        async with conn.begin():
            try:
                stmt = files_table.delete(files_table).where(files_table.c.filedata == file_id)
                await conn.execute(stmt)
                return True
            except exc.SQLAlchemyError:
                raise exc.SQLAlchemyError("Error while executing")

async def get_user_files(username:str) -> dict:
    async with AsyncSession(async_engine) as conn:
        try:
            stmt = select(files_table.c.filename,files_table.c.filedata).where(files_table.c.username == username)
            res = await conn.execute(stmt)
            data = res.fetchall()
            result = {}
            for row in data:
                result[row[0]] = row[1]
            return result    
        except exc.SQLAlchemyError:
            raise exc.SQLAlchemyError("Error while executing")
                    
#asyncio.run(create_file("user1","test.txt","some_file_data_textfjkljfkldsfjkls"))
