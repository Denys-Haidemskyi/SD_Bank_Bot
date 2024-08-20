import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router

async def main():
    bot = Bot(token='7166030078:AAHt-pld-2O0i6w2IG3zuJYgYmnDrsc5h5w')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except(KeyboardInterrupt):
        print('Ты убил бота!')
