from datetime import datetime

from telegram import Update
from telegram.constants import ParseMode, ChatAction
from telegram.ext import ConversationHandler, CallbackContext

from src.agent.main import llm


async def get_actual_date(update: Update, context: CallbackContext) -> int:
    """Returns the actual date."""

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING,
    )

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.delete_message()
    now = datetime.now()
    formatted_date = now.strftime("%A, %d %B %Y")

    try:
        response = await llm.ainvoke(f"""
        Debes responder al usuario en formato markdown la fecha actual en español.
        NO le respondas las instrucciones sino solo la respuesta de manera amigable puedes agregarle emojis.
        La fecha actual es {formatted_date}.
        Ademas agrega una frase motivacional al final relacionada con la fecha actual.
        """)
        response_text = response.content.strip()
    except Exception as e:
        print(f"Error getting date from LLM: {e}")
        response_text = "No puede obtener la fecha actual en este momento."

    send_args = {
        "chat_id": update.effective_chat.id,
        "text": response_text,
        "parse_mode": ParseMode.MARKDOWN,
    }

    if update.message:
        send_args["reply_to_message_id"] = update.message.message_id

    await context.bot.send_message(**send_args)

    return ConversationHandler.END
