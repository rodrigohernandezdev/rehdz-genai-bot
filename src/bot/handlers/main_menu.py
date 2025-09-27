from telegram import Update
from telegram.ext import CallbackContext
from src.bot.keyboards import get_main_menu_keyboard
from src.config import MAIN_MENU

async def start(update: Update, context: CallbackContext) -> int:
    """Sends a message with three inline buttons attached."""
    reply_markup = get_main_menu_keyboard()
    await update.message.reply_text("¡Bienvenido! Estoy aquí para ayudarte con películas y música. ¿Por dónde empezamos?", reply_markup=reply_markup)
    return MAIN_MENU

async def main_menu(update: Update, context: CallbackContext) -> int:
    """Displays the main menu."""
    query = update.callback_query
    await query.answer()
    reply_markup = get_main_menu_keyboard()
    await query.edit_message_text(
        text="Estás de vuelta en el menú principal. ¿Qué exploramos ahora?",
        reply_markup=reply_markup
    )
    return MAIN_MENU
