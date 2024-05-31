import os
from dotenv import load_dotenv
from fastapi import APIRouter, Request
from aiogram.types import Update
from aiogram import Bot, Dispatcher

from app.handlers.message_handler import router_main


load_dotenv()


router_whook = APIRouter()


TG_BOT_TOKEN = os.getenv("TOKEN_BOT")

bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router_main)


@router_whook.post("/tg_updates")
async def process_webhook(request: Request):

    if TG_BOT_TOKEN == TG_BOT_TOKEN:
        update = Update(**await request.json())
        await dp.feed_update(bot, update)
        return {"result": "ok"}
    else:
        return {"error": "true", "status": "403"}


@router_whook.get("/")
async def root():
    return {"text": "Welcome!"}
