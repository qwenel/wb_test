import os
from openai import AsyncOpenAI
from dotenv import load_dotenv


load_dotenv()


GPT_TOKEN = os.getenv("OPENAI_API_KEY")


client = AsyncOpenAI(
    api_key=GPT_TOKEN,
    base_url="https://api.proxyapi.ru/openai/v1"
)


async def generate_answer(user_message):
    print('Генерирую сообщение...')
    
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user", 
                "content": f"{user_message}"
            }
        ],
        model="gpt-3.5-turbo"
    )
    return chat_completion.choices[0].message.content


async def generate_start_answer():
    print('Генерирую начальное сообщение...')
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Ты любитель поддержать разговор и ответить на вопросы собеседника, тебе нужно представить себя и привлечь человека к разговору."
            },
            {
                "role": "user", 
                "content": f"Расскажи о себе"
            }
        ],
        model="gpt-3.5-turbo"
    )
    return chat_completion.choices[0].message.content