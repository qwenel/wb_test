from fastapi import APIRouter, Request

from api.robocassa.robocassa import parse_response, check_signature_result, shop_pwd_2
from app.handlers.balance_handler import payment_status_failure, payment_status_success
from web.set_webhook import bot
from app.states.userStates import UserStates
from main import logger


router_kassa = APIRouter()


@router_kassa.get("/kassa/cqtNmI7phruR20R2U8Rz")
async def result_payment(request: Request) -> str:
    """Verification of notification (ResultURL).
    :param request: HTTP parameters.
    """
    req = request.query_params
    logger.info(f"GOT ROBOKASSA GET REQUEST (ResultURL): {req}")

    merchant_password_2 = shop_pwd_2
    param_request = parse_response(str(req))
    cost = param_request["OutSum"]
    number = param_request["InvId"]
    signature = param_request["SignatureValue"]

    if check_signature_result(number, cost, signature, merchant_password_2):
        logger.info("success payment")
        await payment_status_success(
            bot, number, cost, UserStates.balance_replenishment
        )
        return f'OK{param_request["InvId"]}'

    logger.info("failure payment")
    await payment_status_failure(bot, number, cost, UserStates.balance_replenishment)
    return "bad sign"
