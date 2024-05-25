import asyncio, os, signal
from aiogram import Bot, Dispatcher
from datetime import datetime, timedelta
from apscheduler.triggers.interval import IntervalTrigger

from app.handlers.message_handler import router_main
from api.scheduler.scheduler import (
    db_fill_job,
    process_unanswered_job,
    clear_old_shown_feedbacks_job,
)

from dotenv import load_dotenv

from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()


async def main():
    bot = Bot(token=os.getenv("TOKEN_BOT"))
    dp = Dispatcher()
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


def handle_exit(loop):
    tasks = asyncio.all_tasks(loop)
    for task in tasks:
        task.cancel()

    loop.stop()
    loop.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(handle_exit(loop)))

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("До следующей встречи!")
        exit()
