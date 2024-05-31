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


async def main():
    bot = Bot(token=os.getenv("TOKEN_BOT"))
    dp = Dispatcher()
    logger.add(
        path,
        format="{time} {level} {message}",
        rotation="100 KB",
        compression="zip",
        colorize=True,
    )

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    scheduler.add_job(db_fill_job, trigger="interval", seconds=10)
    scheduler.add_job(clear_old_shown_feedbacks_job, trigger="interval", hours=1)
    scheduler.add_job(
        process_unanswered_job,
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
    except (KeyboardInterrupt, asyncio.exceptions.CancelledError, SystemExit):
        logger.info("До следующей встречи!")
