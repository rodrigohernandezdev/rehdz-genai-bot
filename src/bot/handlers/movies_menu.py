from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from src.bot.keyboards import get_movies_menu_keyboard
from src.config import MOVIES_MENU

async def movies_menu(update: Update, context: CallbackContext) -> int:
    """Displays the movies menu."""
    query = update.callback_query
    await query.answer()
    reply_markup = get_movies_menu_keyboard()
    await query.edit_message_text(
        text="Perfecto, estamos en la sección de películas. Elige una opción:",
        reply_markup=reply_markup
    )
    return MOVIES_MENU

async def movie_categories(update: Update, context: CallbackContext) -> int:
    """Displays the movie categories and ends the conversation path."""
    query = update.callback_query
    await query.answer()
    categories_text = """**🎬 Categorías de Películas**

Estos son algunos de los géneros disponibles:

- Acción
- Comedia
- Drama
- Terror
- Ciencia Ficción

Para volver a empezar, escribe /start."""
    await query.edit_message_text(text=categories_text, reply_markup=None)
    return ConversationHandler.END
