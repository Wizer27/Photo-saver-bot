from aiogram import Bot,Dispatcher,F,Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message,File,Video,PhotoSize
import aiogram
from database.core import is_user_exists,create_user,subscribe,is_user_subbed
from database.files_database.files_core import create_file,delete_file,get_user_files
from keyboards import main_keyborad

router = Router()

@router.message(CommandStart())
@router.message(F.text == "Start")
async def start_handler(message:Message):
    user_id = message.from_user.id
    user_ex = await is_user_exists(str(user_id))
    if not user_ex:
        await create_user(str(user_id))
    await message.answer(f"Welcome {message.from_user.username}",reply_markup=main_keyborad)
    
        

@router.message(F.text == "Profile")
async def profile_handler(message:Message):
    pass

