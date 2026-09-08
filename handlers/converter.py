import os
import uuid
import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, FSInputFile

from config import MAX_FILE_SIZE_BYTES, MAX_FILE_SIZE_MB, ALLOWED_MIME_TYPES, TELEGRAM_MESSAGE_LIMIT
from keyboards.converter import get_output_options_keyboard, get_cancel_keyboard
from keyboards.main import get_main_keyboard
from services.base64_converter import convert_file_to_base64, generate_data_uri, save_base64_to_temp_file
from utils.helpers import get_image_metadata, safe_remove_file, format_size

router = Router()
logger = logging.getLogger(__name__)

class ConvertState(StatesGroup):
    waiting_for_image = State()
    image_processed = State()

@router.message(Command("convert"))
@router.callback_query(F.data == "cmd_convert")
async def start_conversion(event: Message | CallbackQuery, state: FSMContext):
    await state.set_state(ConvertState.waiting_for_image)
    text = "📥 Send me an image (as a Photo or Document file) to convert to Base64."
    if isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.answer(text, reply_markup=get_cancel_keyboard())
    else:
        await event.answer(text, reply_markup=get_cancel_keyboard())

@router.message(Command("cancel"))
@router.callback_query(F.data == "cmd_cancel")
async def cancel_action(event: Message | CallbackQuery, state: FSMContext):
    data = await state.get_data()
    temp_path = data.get("temp_file_path")
    if temp_path:
        safe_remove_file(temp_path)
    
    await state.clear()
    text = "🚫 Action cancelled. Send /start or /convert when you are ready again."
    if isinstance(event, CallbackQuery):
        await event.answer("Cancelled")
        await event.message.answer(text, reply_markup=get_main_keyboard())
    else:
        await event.answer(text, reply_markup=get_main_keyboard())

@router.message(StateFilter(ConvertState.waiting_for_image), F.photo | F.document)
@router.message(F.photo | F.document)
async def process_image_upload(message: Message, state: FSMContext, bot: Bot):
    status_msg = await message.answer("⏳ Downloading image...")
    file_id = None
    file_name = "image.png"
    file_size = 0

    if message.photo:
        photo = message.photo[-1]
        file_id = photo.file_id
        file_size = photo.file_size or 0
        file_name = f"photo_{photo.file_unique_id}.jpg"
    elif message.document:
        doc = message.document
        if doc.mime_type not in ALLOWED_MIME_TYPES and not doc.mime_type.startswith("image/"):
            await status_msg.edit_text("❌ Unsupported file type. Please upload JPG, PNG, WEBP, or GIF images.")
            return
        file_id = doc.file_id
        file_size = doc.file_size or 0
        file_name = doc.file_name or "document.png"

    if file_size > MAX_FILE_SIZE_BYTES:
        await status_msg.edit_text(f"❌ File size exceeds maximum limit of {MAX_FILE_SIZE_MB} MB.")
        return

    os.makedirs("temp_downloads", exist_ok=True)
    temp_path = os.path.join("temp_downloads", f"{uuid.uuid4().hex}_{file_name}")

    try:
        tg_file = await bot.get_file(file_id)
        await bot.download_file(tg_file.file_path, destination=temp_path)
        
        await status_msg.edit_text("🔄 Analyzing image...")
        metadata = get_image_metadata(temp_path)
        
        if metadata["mime_type"] not in ALLOWED_MIME_TYPES:
            safe_remove_file(temp_path)
            await status_msg.edit_text("❌ Invalid or unsupported image format detected.")
            return

        base64_str, raw_b64_size = await convert_file_to_base64(temp_path)
        
        await state.update_data(
            temp_file_path=temp_path,
            metadata=metadata,
            base64_str=base64_str,
            raw_b64_size=raw_b64_size
        )
        await state.set_state(ConvertState.image_processed)

        info_text = (
            "🖼 **Image Information**\n\n"
            f"• **Filename:** `{metadata['filename']}`\n"
            f"• **Format:** {metadata['format']}\n"
            f"• **MIME Type:** `{metadata['mime_type']}`\n"
            f"• **Dimensions:** {metadata['width']}x{metadata['height']} px\n"
            f"• **Original Size:** {metadata['size_formatted']}\n"
            f"• **Base64 Size:** {format_size(raw_b64_size)}\n\n"
            "Select output format below:"
        )

        await status_msg.edit_text(info_text, reply_markup=get_output_options_keyboard(), parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error processing image: {e}", exc_info=True)
        safe_remove_file(temp_path)
        await status_msg.edit_text("❌ Failed to process image. Ensure file is a valid image format.")

@router.callback_query(StateFilter(ConvertState.image_processed), F.data.startswith("fmt_"))
async def handle_format_selection(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    
    base64_str = data.get("base64_str")
    metadata = data.get("metadata")
    temp_path = data.get("temp_file_path")

    if not base64_str or not metadata:
        await callback.message.answer("❌ Session expired. Upload image again.", reply_markup=get_main_keyboard())
        await state.clear()
        return

    output_fmt = callback.data.split("_")[1]
    
    if output_fmt == "data_uri":
        result_text = generate_data_uri(base64_str, metadata["mime_type"])
        prefix = f"data_uri_{metadata['filename']}"
    else:
        result_text = base64_str
        prefix = f"base64_{metadata['filename']}"

    if len(result_text) <= TELEGRAM_MESSAGE_LIMIT:
        formatted_message = f"```\n{result_text}\n```"
        await callback.message.answer(formatted_message, parse_mode="Markdown")
    else:
        out_path = await save_base64_to_temp_file(result_text, prefix)
        document = FSInputFile(out_path, filename=f"{prefix}.txt")
        await callback.message.answer_document(
            document=document,
            caption="📄 Result exceeded message length limit and is attached above as a text file."
        )
        safe_remove_file(out_path)

    safe_remove_file(temp_path)
    await callback.message.answer("✅ Conversion complete! Send another image anytime.", reply_markup=get_main_keyboard())
    await state.clear()
