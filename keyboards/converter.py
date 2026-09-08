from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_output_options_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔤 Base64", callback_data="fmt_base64"),
                InlineKeyboardButton(text="🌐 Data URI", callback_data="fmt_data_uri")
            ],
            [
                InlineKeyboardButton(text="❌ Cancel", callback_data="cmd_cancel")
            ]
        ]
    )

def get_cancel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❌ Cancel", callback_data="cmd_cancel")
            ]
        ]
    )
