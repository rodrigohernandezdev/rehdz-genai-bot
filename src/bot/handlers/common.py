from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

async def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Cancelado. ¡Estaré por aquí si me necesitas! Solo usa /start.")
    return ConversationHandler.END
