import asyncio, os
from aiogram import Bot, Dispatcher
from openai import AsyncOpenAI

from app.handlers.message_handler import router_main
from api.scheduler.scheduler import scheduled_db_fill_job

from dotenv import load_dotenv

from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()


async def main():
    bot = Bot(token=os.getenv('TOKEN_BOT'))
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    
    scheduler.add_job(scheduled_db_fill_job, trigger='interval', seconds=10)
    dp.include_router(router_main)
    
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('До следующей встречи!')
        exit()