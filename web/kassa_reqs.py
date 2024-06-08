from dotenv import load_dotenv
from fastapi import APIRouter, Request

from api.robocassa.robocassa import parse_response, check_signature_result


load_dotenv()


router_kassa = APIRouter()


@router_kassa.get("/kassa/cqtNmI7phruR20R2U8Rz")
def result_payment(merchant_password_2: str, request: Request) -> str:
    """Verification of notification (ResultURL).
    :param request: HTTP parameters.
    """
    param_request = parse_response(request)
    cost = param_request["OutSum"]
    number = param_request["InvId"]
    signature = param_request["SignatureValue"]

    if check_signature_result(number, cost, signature, merchant_password_2):
        return f'OK{param_request["InvId"]}'
    return "bad sign"
