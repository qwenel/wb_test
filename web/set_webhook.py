import os
from dotenv import load_dotenv
from fastapi import APIRouter, Request
from aiogram.types import Update
from aiogram import Bot, Dispatcher

from app.handlers.message_handler import router_main
from main import logger

load_dotenv()


router_whook = APIRouter()


TG_BOT_TOKEN = os.getenv("TOKEN_BOT")

bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router_main)


async def set_webhook():
    await bot.delete_webhook(True)

    webhook_uri = os.getenv("WEB_HOOK_ADDRS") + TG_BOT_TOKEN

    await bot.set_webhook(webhook_uri)


@router_whook.post(f"/tg_updates/{TG_BOT_TOKEN}")
async def process_webhook(request: Request):
    logger.info(f"tg request: {await request.json()}")
    if TG_BOT_TOKEN == TG_BOT_TOKEN:
        update = Update(**await request.json())
        await dp.feed_update(bot, update)
        return {"result": "ok"}
    else:
        return {"error": "true", "status": "403"}


@router_whook.get("/")
async def root():
    logger.info("accessed ROOT page!")
    return {"text": "Welcome!"}
