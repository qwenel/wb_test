from fastapi import APIRouter, Request

from api.robocassa.robocassa import parse_response, check_signature_result, shop_pwd_2
from app.database.exec_methods.payments_method import get_user_id_by_payment_id
from app.handlers.balance_handler import payment_status_failure, payment_status_success
from web.set_webhook import bot
from app.states.userStates import UserStates
from loguru import logger


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

    user_id = await get_user_id_by_payment_id(number)

    if (
        check_signature_result(number, cost, signature, merchant_password_2)
        and user_id is not None
    ):
        logger.info(f"success payment, user_id: {user_id[0]}")
        await payment_status_success(bot, user_id[0], int(float(cost)))
        return f"OK{number}"

    logger.info("failure payment")
    await payment_status_failure(bot, user_id[0], int(float(cost)))
    return "bad sign"
