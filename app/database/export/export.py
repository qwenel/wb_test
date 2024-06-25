from api.gspread.gspread import perform_gspread_update
from app.database.connection import create_connection
from app.database.exec_methods.shop_methods import get_apis_list
from app.database.vars import path


async def get_data_from_db_to_export(db=path):
    conn = await create_connection(db)
    cursor = await conn.cursor()

    await cursor.execute(
        "SELECT tg_id, register_date, username, phone_number, count_ans, last_answer_date, balance, last_payment_date, payments_sum FROM users"
    )

    users = await cursor.fetchall()

    if len(users) != 0:

        users_info = []

        for user_info in users:
            apis_list = await get_apis_list(user_info[0], db)
            if apis_list is None:
                apis_list = []
            user_info = format_info(user_info, apis_list)
            users_info.append(user_info)

        await perform_gspread_update(users_info)

    await conn.commit()
    await conn.close()


def format_info(users, additional_data):
    users = list(users)
    users = users[1:]
    shop_count = len(additional_data)

    if additional_data is not None:
        additional_data = ", ".join(additional_data)
    else:
        additional_data = "0"

    users.insert(3, shop_count)
    users.insert(4, additional_data)

    return users
