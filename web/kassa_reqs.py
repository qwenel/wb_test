import os
from dotenv import load_dotenv
from fastapi import APIRouter, Request

from api.robocassa.robocassa import parse_response, check_signature_result
from web.set_webhook import bot
from main import logger


router_kassa = APIRouter()


load_dotenv()


@router_kassa.get("/kassa/cqtNmI7phruR20R2U8Rz")
async def result_payment(request: Request) -> str:
    """Verification of notification (ResultURL).
    :param request: HTTP parameters.
    """
    req = request.query_params
    logger.info(f"GOT ROBOKASSA GET REQUEST (ResultURL): {req}")

    merchant_password_2 = os.getenv("SHOP_PWD2_TEST")
    param_request = parse_response(str(req))
    cost = param_request["OutSum"]
    number = param_request["InvId"]
    signature = param_request["SignatureValue"]

    if check_signature_result(number, cost, signature, merchant_password_2):
        logger.info("success payment")
        return f'OK{param_request["InvId"]}'
    logger.info("failure payment")
    return "bad sign"
