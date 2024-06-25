import os
from fastapi import APIRouter, Request
from loguru import logger
from dotenv import load_dotenv

from app.database.export.export import get_data_from_db_to_export

load_dotenv(override=True)


router_export = APIRouter()


SHEET_ID = os.getenv("SHEETS_ID")


@router_export.get(f"/sheets/{SHEET_ID}")
async def update_sheets(request: Request):
    logger.info("TRYING TO UPDATE SHEETS")
    try:
        await get_data_from_db_to_export()
        return {"status": "200", "text": "update is done succesfully"}
    except Exception as ex:
        logger.error(ex)
        return {"error": "true", "status": "503", "text": "failed to update sheet"}
