import asyncio, os
from aiogram import Bot, Dispatcher

from app.handlers.message_handler import router_main

from dotenv import load_dotenv


load_dotenv()


async def main():
    bot = Bot(token=os.getenv('TOKEN_BOT'))
    dp = Dispatcher()
    
    dp.include_router(router_main)
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('До следующей встречи!')
        exit()