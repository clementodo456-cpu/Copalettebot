from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🖼 Convert Image", callback_data="cmd_convert"),
                InlineKeyboardButton(text="📖 How It Works", callback_data="cmd_how_it_works")
            ],
            [
                InlineKeyboardButton(text="ℹ️ About", callback_data="cmd_about")
            ]
        ]
    )
