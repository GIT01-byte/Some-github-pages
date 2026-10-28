import asyncio
import logging

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.telegram import TelegramAPIServer
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties

from config import settings
from handlers import router

logging.basicConfig(level=logging.INFO)


async def main():
    worker_url = settings.PROXY_URL.rstrip("/")

    api_server = TelegramAPIServer.from_base(worker_url)
    session = AiohttpSession(api=api_server)

    bot = Bot(
        token=settings.BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)

    print(f"Бот запущен через Cloudflare Worker: {worker_url}")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
