from aiogram import Bot,Dispatcher,F,Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message,File,Video,PhotoSize
import aiogram

router = Router()

@router.message(F.text == "Profile")
async def profile_handler(message:Message):
    pass