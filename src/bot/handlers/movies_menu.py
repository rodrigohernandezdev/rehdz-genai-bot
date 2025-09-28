from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, ConversationHandler

from src.agent.main import agent_executor
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
    """Calls the agent to get movie categories and displays them."""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(text="Buscando categorías de películas... 🤖")

    try:
        response = await agent_executor.ainvoke({
            "input": "¿Cuales categorías de películas hay registradas? Formatea la respuesta como una lista de viñetas de markdown (usando '-')."
        })
        agent_response = response.get("output", "No se han encontrado categorías.")
    except Exception as e:
        agent_response = f"No se han encontrado categorías"
        print(f"Error in movie_categories: {e}")

    await query.edit_message_text(text=agent_response, reply_markup=None, parse_mode=ParseMode.MARKDOWN)

    return ConversationHandler.END
