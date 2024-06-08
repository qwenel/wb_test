import decimal
import os
from urllib import parse
from dotenv import load_dotenv
import hashlib


load_dotenv()


shop_id = os.getenv("SHOP_ID")
shop_pwd_1 = os.getenv("SHOP_PWD1_TEST")
shop_pwd_2 = os.getenv("SHOP_PWD2_TEST")


def create_pay_link(out_sum: int, invId: int, desc: str) -> str:
    url = generate_payment_link(
        merchant_login=shop_id,
        merchant_password_1=shop_pwd_1,
        cost=out_sum / 1.0,
        number=invId,
        description=desc,
        is_test=1,
    )
    return url


def calculate_signature(*args) -> str:
    """Create signature MD5."""
    return hashlib.md5(":".join(str(arg) for arg in args).encode()).hexdigest()


def generate_payment_link(
    merchant_login: str,  # Merchant login
    merchant_password_1: str,  # Merchant password
    cost: decimal,  # Cost of goods, RU
    number: int,  # Invoice number
    description: str,  # Description of the purchase
    is_test=0,
    robokassa_payment_url="https://auth.robokassa.ru/Merchant/Index.aspx",
) -> str:
    """URL for redirection of the customer to the service."""
    signature = calculate_signature(merchant_login, cost, number, merchant_password_1)

    data = {
        "MerchantLogin": merchant_login,
        "OutSum": cost,
        "InvId": number,
        "Description": description,
        "SignatureValue": signature,
        "IsTest": is_test,
    }
    return f"{robokassa_payment_url}?{parse.urlencode(data)}"


def result_payment(merchant_password_2: str, request: str) -> str:
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


def parse_response(request: str) -> dict:
    """
    :param request: Link.
    :return: Dictionary.
    """
    params = {}

    for item in request.split("&"):
        key, value = item.split("=")
        params[key] = value
    return params


def check_signature_result(
    order_number: int,  # invoice number
    received_sum: decimal,  # cost of goods, RU
    received_signature: hex,  # SignatureValue
    password: str,  # Merchant password
) -> bool:
    signature = calculate_signature(received_sum, order_number, password)
    if signature.lower() == received_signature.lower():
        return True
    return False
