from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext


async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message with the available commands."""
    help_text = """
🤖 *Comandos disponibles* 🤖

/start - Iniciar el bot y mostrar el menú principal
/fecha - Obtener la fecha actual
/clima <ciudad> - Consultar el clima en una ciudad específica
/pelicula <nombre> - Buscar información de una película
/help - Mostrar este mensaje de ayuda
/cancel - Cancelar la operación actual

🎬 *Menú de Películas*:
- Desde el menú principal puedes acceder a las categorías de películas
- Buscar información detallada de películas específicas

📅 *Fecha y Hora*:
- Obtén la fecha actual con información adicional

🌡️ *Clima*:
- Consulta el clima actual de cualquier ciudad

¡Usa los comandos y disfruta de las funciones del bot! 😊

Ademas puedes chatear conmigo y te ayudaré en lo que necesites.
    """

    await update.message.reply_text(
        text=help_text.strip(),
        parse_mode=ParseMode.MARKDOWN,
        reply_to_message_id=update.message.message_id
    )
