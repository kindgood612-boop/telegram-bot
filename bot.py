# bot.py

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from middlewares.permissions import PermissionMiddleware
from handlers import register_handlers

async def main():
    bot = Bot(
        token=BOT_TOKEN,
        parse_mode=ParseMode.HTML
    )

    dp = Dispatcher()

    # Middleware الصلاحيات
    dp.message.middleware(PermissionMiddleware())

    # تسجيل كل الهاندلرز
    register_handlers(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
