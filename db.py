import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
pool = None

async def db_start():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)
    print("DB started")

async def db_stop():
    await pool.close()