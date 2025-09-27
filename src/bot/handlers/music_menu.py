from telegram import Update
from telegram.ext import CallbackContext
from src.bot.keyboards import get_music_menu_keyboard
from src.config import MUSIC_MENU

async def music_menu(update: Update, context: CallbackContext) -> int:
    """Displays the music menu."""
    query = update.callback_query
    await query.answer()
    reply_markup = get_music_menu_keyboard()
    await query.edit_message_text(
        text="¡Vamos a la música! Elige una opción:",
        reply_markup=reply_markup
    )
    return MUSIC_MENU
