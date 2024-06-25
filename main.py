import os
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
from app.database.export.export import get_data_from_db_to_export
from web.set_webhook import router_whook, set_webhook
from web.kassa_reqs import router_kassa
from web.export_sheets import router_export


load_dotenv(override=True)


LOGGER_PATH = os.getenv("LOGGER_PATH")


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.add(
        LOGGER_PATH,
        format="{time} {level} {message}",
        rotation="100 KB",
        compression="zip",
        colorize=True,
    )
    logger.info("LOGGER IS SET")

    await get_data_from_db_to_export()

    logger.info("STARTING...")
    await set_webhook()
    logger.info("WEBHOOK IS SET...")
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
app.include_router(router_kassa)
app.include_router(router_export)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
