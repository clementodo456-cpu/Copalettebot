from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.main import get_main_keyboard

router = Router()

HELP_TEXT = (
    "🛠 **Img2basebot Help & Commands**\n\n"
    "• /start - Launch the bot and main menu\n"
    "• /convert - Begin image-to-Base64 conversion mode\n"
    "• /help - Display usage guidelines\n"
    "• /about - Technical details and bot version\n"
    "• /cancel - Abort active conversion processes\n\n"
    "💡 **Tip:** Send any image directly without typing a command to begin conversion immediately."
)

@router.message(Command("help"))
async def cmd_help_explicit(message: Message):
    await message.answer(HELP_TEXT, reply_markup=get_main_keyboard(), parse_mode="Markdown")
