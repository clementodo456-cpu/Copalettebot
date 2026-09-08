from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.main import get_main_keyboard

router = Router()

START_TEXT = (
    "👋 **Welcome to Img2basebot!**\n\n"
    "I convert your image files into Base64 encoded strings ready for HTML, CSS, JavaScript, APIs, and databases.\n\n"
    "Choose an option below or directly send an image to get started."
)

HOW_IT_WORKS_TEXT = (
    "📖 **How It Works:**\n\n"
    "1️⃣ Send an image (Photo or Document format).\n"
    "2️⃣ I will extract metadata and process the image without quality loss.\n"
    "3️⃣ Choose your output format: **Raw Base64** or **Data URI**.\n"
    "4️⃣ Receive your output as plain text or as a `.txt` file for large inputs."
)

ABOUT_TEXT = (
    "ℹ️ **About Img2basebot**\n\n"
    "• **Version:** 1.0.0\n"
    "• **Framework:** Python 3.11+ / aiogram 3.x\n"
    "• **Supported Formats:** JPG, PNG, WEBP, GIF\n"
    "• **Privacy:** Images are processed entirely in memory or temporary storage and immediately deleted."
)

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(START_TEXT, reply_markup=get_main_keyboard(), parse_mode="Markdown")

@router.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(ABOUT_TEXT, reply_markup=get_main_keyboard(), parse_mode="Markdown")

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HOW_IT_WORKS_TEXT, reply_markup=get_main_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "cmd_how_it_works")
async def cb_how_it_works(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(HOW_IT_WORKS_TEXT, reply_markup=get_main_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "cmd_about")
async def cb_about(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(ABOUT_TEXT, reply_markup=get_main_keyboard(), parse_mode="Markdown")
