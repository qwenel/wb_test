import os
from loguru import logger
from openai import AsyncOpenAI
from dotenv import load_dotenv
from api.wb.wb_feedbacks_ans import answer_feedback
from app.database.exec_methods.answer_methods import update_answer_text
from app.database.exec_methods.user_methods import update_user_props_after_generating
from app.database.vars import path


load_dotenv()


client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.proxyapi.ru/openai/v1"
)


async def generate_answer(
    tg_id: int,
    fb_id: str,
    fb_text: str,
    api_key: str,
    fb_rating: int,
    auto: bool,
    db=path,
) -> bool | str:

    ruls = ""

    if fb_rating > 3:
        ruls = """Напиши благодарственный ответ на отзыв к покупке на маркетплейсе от имени продавца. 
        Ответ должен соответствовать следующим критериям - ответ не должен содержать заполнители, 
        параметры для вставки (наприер {имя клиента|компания} и т.п.); - клиент имеет женский пол; 
        - не должен содержать информацию от кого этот ответ(например: "Команда продавцов" - такого 
        не должно быть в ответе); - не должно быть предложение клиенту об обмене товара или какой-то 
        компенсации. Пример ответа: Здравствуйте. Спасибо за то, что выбрали нас. Позвольте поблагодарить 
        Вас за отзыв. Мы очень рады, что Вам подошел Наш товар, носите с удовольствием. Будем рады видеть 
        Вас снова. Приятных покупок!  Дальше я передаю сам ответ покупателя:   """

    if fb_rating < 4:
        ruls = """Напиши сострадательный успокаивающий ответ на отзыв к покупке на маркетплейсе от имени продавца. 
        Ответ должен соответствовать следующим критериям - ответ не должен содержать заполнители, 
        параметры для вставки (наприер {имя клиента|компания} и т.п.); - клиент имеет женский пол; 
        - не должен содержать информацию от кого этот ответ(например: "Команда продавцов" - такого 
        не должно быть в ответе); - не должно быть предложение клиенту об обмене товара или какой-то 
        компенсации; - отзывы поступают лишь на товары эротического характера, старайся не упоминать название товара в ответе. 
        Пример ответа: Здравствуйте. Спасибо за то, что выбрали нас. Позвольте поблагодарить 
        Вас за отзыв. Нам очень жаль, что наш товар не оправдал Ваших ожиданий, мы уже делаем все возможное для того, 
        чтобы не допустить данных трудностей вновь. Будем рады видеть Вас снова. Приятных покупок! 
        Дальше я передаю сам ответ покупателя:   """

    try:
        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": ruls + fb_text,
                }
            ],
            model="gpt-3.5-turbo",
        )

        answer = chat_completion.choices[0].message.content

        if auto:
            logger.info(
                "GPT generated auto answer: fb_id: "
                + fb_id
                + "\n | text: "
                + fb_text
                + " |\n api_key "
                + api_key
            )
            if not await answer_feedback(fb_id, answer, api_key):
                return False

            await update_answer_text(tg_id, fb_id, answer, db)
            await update_user_props_after_generating(tg_id, db)
            return True

        logger.info(
            "GPT generated manual answer: fb_id: "
            + fb_id
            + "\n | text: "
            + fb_text
            + " |\n api_key "
            + api_key
        )
        await update_user_props_after_generating(tg_id, db)
        return answer

    except Exception as e:

        logger.error(
            e
            + "GPT ERROR: "
            + fb_id
            + "\n | text: "
            + fb_text
            + " |\n api_key "
            + api_key
        )
        return False
