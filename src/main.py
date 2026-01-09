from aiogram import Bot,Dispatcher,F,Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message,File,Video,PhotoSize
import aiogram
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

bot = Bot(os.getenv("BOT"))
dp = Dispatcher()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("DONE")
