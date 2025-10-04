from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import CallbackContext

from src.agent.main import agent_executor


async def get_weather(update: Update, context: CallbackContext) -> None:
    """Fetches and returns the current weather for a specified city."""

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING,
    )

    if not context.args:
        await update.message.reply_text(
            "Por favor, proporciona el nombre de la ciudad.\nEjemplo: /clima Tu Ciudad"
        )
        return

    city = " ".join(context.args)

    try:
        response = await agent_executor.ainvoke({
            "input": f"""
            Busca el clima en la ciudad de {city}
            Proporciona la temperatura actual, las condiciones climáticas y cualquier otra información relevante.
            Responde en español de manera amigable y con emojis.
            Formato: texto simple, usa emojis para hacerlo visual.
            """
        })
        response_text = response["output"].strip()

    except Exception as e:
        print(f"Error getting weather from LLM: {e}")
        response_text = "No pude obtener el clima en este momento."

    await update.message.reply_text(
        text=response_text,
        reply_to_message_id=update.message.message_id
    )
