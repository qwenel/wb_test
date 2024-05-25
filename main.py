import asyncio, os, signal
from aiogram import Bot, Dispatcher
from datetime import datetime, timedelta
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger

from app.handlers.message_handler import router_main
from api.scheduler.scheduler import (
    db_fill_job,
    process_unanswered_job,
    clear_old_shown_feedbacks_job,
)

from dotenv import load_dotenv

from apscheduler.schedulers.asyncio import AsyncIOScheduler


load_dotenv()


path = "logs/running.log"


db_fill_job_lock = asyncio.Lock()
process_unanswered_job_lock = asyncio.Lock()
clear_old_shown_feedbacks_job_lock = asyncio.Lock()


async def db_fill_job_wrapper():
    async with db_fill_job_lock:
        await db_fill_job()


async def process_unanswered_job_wrapper():
    async with process_unanswered_job_lock:
        await process_unanswered_job()


async def clear_old_shown_feedbacks_job_wrapper():
    async with clear_old_shown_feedbacks_job_lock:
        await clear_old_shown_feedbacks_job()


async def main():
    bot = Bot(token=os.getenv("TOKEN_BOT"))
    dp = Dispatcher()
    logger.add(
        path,
        format="{time} {level} {message}",
        rotation="100 KB",
        compression="zip",
    )

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    scheduler.add_job(db_fill_job_wrapper, trigger="interval", seconds=10)
    scheduler.add_job(
        clear_old_shown_feedbacks_job_wrapper, trigger="interval", hours=1
    )
    scheduler.add_job(
        process_unanswered_job_wrapper,
        trigger=IntervalTrigger(
            seconds=10, start_date=datetime.now() + timedelta(seconds=5)
        ),
    )
    dp.include_router(router_main)

    scheduler.start()

    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown(wait=False)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("До следующей встречи!")
