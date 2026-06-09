import db
import json

CREATE_QUERY = """
CREATE TABLE IF NOT EXISTS flashcards (
  id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  collection TEXT NOT NULL,
  content JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
INSERT_QUERY = """
INSERT INTO flashcards( collection, content )
VALUES ($1, $2)
"""

GET_QUERY = """
SELECT id, collection,content, created_at
FROM flashcards
WHERE collection = $1
ORDER BY created_at DESC
"""

DELETE_QUERY= """
DELETE FROM flashcards
WHERE id = $1
"""




async def create_table():
    async with db.pool.acquire() as conn:
        await conn.execute(CREATE_QUERY)

async def insert_table(collection_name: str, content: list[dict]):
  async with db.pool.acquire() as conn:
    async with conn.transaction():
      for i in content:
        await conn.execute(
          INSERT_QUERY,
          collection_name, 
          i
        )

async def get_table(collection_name: str):
  async with db.pool.acquire() as conn:
    rows = await conn.fetch(GET_QUERY, collection_name)
    result = [{**dict(row), "created_at": row["created_at"].isoformat()} for row in rows]
    return result
async def delete_table(id: int):
  async with db.pool.acquire() as conn:
    async with conn.transaction():
        await conn.execute(
          DELETE_QUERY,
          id
        )

    


