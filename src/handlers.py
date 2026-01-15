from aiogram import Bot,Dispatcher,F,Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message,File,Video,PhotoSize
import aiogram
from database.core import is_user_exists,create_user,subscribe,is_user_subbed
from database.files_database.files_core import create_file,delete_file,get_user_files
from keyboards import main_keyborad

router = Router()

@router.message(F.text == "Profile")
async def profile_handler(message:Message):
    pass