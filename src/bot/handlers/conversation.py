import logging
from datetime import datetime

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from src.agent.main import agent_with_chat_history, format_response_for_telegram

logger = logging.getLogger(__name__)


async def handle_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    user_message = update.message.text

    logger.info(f"User {user_id} sent: {user_message[:50]}...")

    if not user_message or not user_message.strip():
        await update.message.reply_text("Por favor envía un mensaje válido.")
        return

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING,
    )

    try:
        start_time = datetime.now()

        response = agent_with_chat_history.invoke(
            {"input": user_message},
            config={"configurable": {"session_id": user_id}}
        )

        processing_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"Response generated in {processing_time:.2f} seconds for user {user_id}")

        raw_output = response.get("output", "Lo siento, no pude generar una respuesta.")
        formatted_output = format_response_for_telegram(raw_output)

        await update.message.reply_text(
            formatted_output,
            reply_to_message_id=update.message.message_id
        )

    except Exception as e:
        logger.error(f"Error processing message from {user_id}: {str(e)}")
        await update.message.reply_text(
            "Perdona, ocurrió un error al procesar tu mensaje. Por favor, intenta de nuevo más tarde.",
            reply_to_message_id=update.message.message_id,
        )
