from fastapi import FastAPI
from routes.card import router
from db import db_start, db_stop
from model.FlashCard import create_table

app = FastAPI()

@app.on_event("startup")
async def startup():
    await db_start()
    await create_table()

@app.on_event("shutdown")
async def shutdown():
    await db_stop()


app.include_router(router)