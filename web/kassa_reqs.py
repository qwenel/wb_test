import os
from dotenv import load_dotenv
from fastapi import APIRouter, Request

from api.robocassa.robocassa import parse_response, check_signature_result
from main import logger


router_kassa = APIRouter()


load_dotenv()


@router_kassa.get("/kassa/cqtNmI7phruR20R2U8Rz")
async def result_payment(request: Request) -> str:
    """Verification of notification (ResultURL).
    :param request: HTTP parameters.
    """
    logger.info(f"GOT ROBOKASSA GET REQUEST (ResultURL): {await request.json()}")

    merchant_password_2 = os.getenv("SHOP_PWD2_TEST")
    param_request = parse_response(request)
    cost = param_request["OutSum"]
    number = param_request["InvId"]
    signature = param_request["SignatureValue"]

    if check_signature_result(number, cost, signature, merchant_password_2):
        logger.info("success")
        return f'OK{param_request["InvId"]}'
    return "bad sign"
