from telegram import Update
from telegram.constants import ParseMode, ChatAction
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


async def movie_genres(update: Update, context: CallbackContext) -> int:
    """Calls the agent to get movie genres and displays them."""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(text="Buscando categorías de películas... 🤖")

    try:
        response = await agent_executor.ainvoke({
            "input": """
            ¿Cuales categorías de películas hay registradas?
            Formatea la respuesta como una lista de viñetas de markdown (usando '-').
            Agrega emojis relacionados con los géneros de películas.
            Responde solo con la lista de categorías y nada más.
            """
        })
        agent_response = response.get("output", "No se han encontrado categorías.")
    except Exception as e:
        agent_response = f"No se han encontrado categorías"
        print(f"Error in movie_genres: {e}")

    await query.edit_message_text(text=agent_response, reply_markup=None, parse_mode=ParseMode.MARKDOWN)

    return ConversationHandler.END


async def search_movie_handler(update: Update, context: CallbackContext) -> int:
    """Handles the command to search for movies."""
    if not context.args:
        await update.message.reply_text(
            "Por favor proporciona el nombre de una película.\nEjemplo: /pelicula El Padrino")
        return ConversationHandler.END

    movie_query = " ".join(context.args)

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING,
    )

    try:
        response = await agent_executor.ainvoke({
            "input": f"""Busca información sobre la película '{movie_query}'.
            Formatea la respuesta en markdown de esta manera:
            - Usa **negrita** para el título y año
            - Agrega emojis relevantes (⭐ para calificación, 🎬 para película, etc)
            - Separa las secciones claramente
            - Si hay múltiples resultados, muestra maximo 2 resultados y solo las que tengan Sinapsis
            - Incluye: Título, Año, Calificación, Resumen
            - Muestra las mas valoradas o recientes primero
            - Mantén la información concisa y bien estructurada
            Responde solo con la información de la película y nada más.
            """
        })
        agent_response = response.get("output", f"No se encontró información sobre '{movie_query}'.")
        if agent_response == "":
            agent_response = f"No se encontró información sobre '{movie_query}'."
    except Exception as e:
        agent_response = f"Ocurrió un error al buscar la película."
        print(f"Error in search_movie_handler: {e}")

    await update.message.reply_text(text=agent_response, parse_mode=ParseMode.MARKDOWN)

    return ConversationHandler.END
