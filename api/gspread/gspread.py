import gspread
from dotenv import load_dotenv
from loguru import logger


load_dotenv(override=True)


gc = gspread.service_account(filename="cred.json")


async def perform_gspread_update(data):
    wks = gc.open("feedbacks_bot_data").sheet1

    wks.update(
        [
            [
                "Дата регистрации",
                "Username",
                "Номер телефона",
                "Количество магазинов",
                "API-ключи",
                "Количество ответов",
                "Дата последнего ответа",
                "Баланс",
                "Дата последней покупки",
                "Сумма всех покупок",
            ]
        ],
        "A1",
    )

    wks.format("A1:J1", {"textFormat": {"bold": True}})

    wks.update(data, "A2")
