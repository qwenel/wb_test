import asyncio, os
import aiohttp
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from datetime import datetime, timedelta
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger
from dotenv import load_dotenv

from api.scheduler.scheduler import (
    db_fill_job,
    process_unanswered_job,
    clear_old_shown_feedbacks_job,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from web.set_webhook import router_whook, set_webhook


load_dotenv()


TG_BOT_TOKEN = os.getenv("TOKEN_BOT")
LOGGER_PATH = os.getenv("LOGGER_PATH")
WEB_HOOK_ADDRS = os.getenv("WEB_HOOK_ADDRS")

logger.add(
    LOGGER_PATH,
    format="{time} {level} {message}",
    rotation="100 KB",
    compression="zip",
    colorize=True,
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    await set_webhook()
    logger.info("STARTING...")
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    scheduler.add_job(db_fill_job, trigger="interval", seconds=10)
    scheduler.add_job(clear_old_shown_feedbacks_job, trigger="interval", hours=1)
    scheduler.add_job(
        process_unanswered_job,
        trigger=IntervalTrigger(
            seconds=10, start_date=datetime.now() + timedelta(seconds=5)
        ),
    )

    scheduler.start()

    yield

    scheduler.shutdown(wait=False)


app = FastAPI(lifespan=lifespan)
app.include_router(router_whook)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)