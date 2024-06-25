import os
from dotenv import load_dotenv
from fastapi import APIRouter, Request
from aiogram.types import Update
from aiogram import Bot, Dispatcher
from loguru import logger
from app.handlers.message_handler import router_main


load_dotenv(override=True)


router_whook = APIRouter()


TG_BOT_TOKEN = os.getenv("TOKEN_BOT")

bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router_main)


async def set_webhook():
    logger.info("setting webhook")
    info = await bot.get_webhook_info()

    logger.info(
        f"WebHook info: {info.url}, size: {len(info.url)}, {info.model_dump_json()}"
    )

    if len(info.url) != 0:
        await bot.delete_webhook(True)

    webhook_uri = os.getenv("WEB_HOOK_ADDRS") + TG_BOT_TOKEN

    await bot.set_webhook(webhook_uri)


@router_whook.post(f"/tg_updates/{TG_BOT_TOKEN}")
async def process_webhook(request: Request):
    logger.info(f"tg request: {await request.json()}")
    try:
        if TG_BOT_TOKEN == TG_BOT_TOKEN:
            update = Update(**await request.json())
            await dp.feed_update(bot, update)
            return {"result": "ok"}
        else:
            return {"error": "true", "status": "403"}
    except Exception as ex:
        logger.error(ex)
    return {"error": "true", "status": "500"}


@router_whook.get("/")
async def root():
    logger.info("accessed ROOT page!")
    return {"text": "Welcome!"}
