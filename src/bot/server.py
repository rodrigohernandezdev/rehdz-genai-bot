from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
)

from src.config import TELEGRAM_TOKEN, MAIN_MENU, MOVIES_MENU, MUSIC_MENU
from src.bot.handlers.main_menu import start, main_menu
from src.bot.handlers.movies_menu import movies_menu, movie_categories
from src.bot.handlers.music_menu import music_menu
from src.bot.handlers.common import cancel

def run():
    """Run the bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(movies_menu, pattern="^movies$"),
                CallbackQueryHandler(music_menu, pattern="^music$"),
                CallbackQueryHandler(cancel, pattern="^cancel$"),
            ],
            MOVIES_MENU: [
                CallbackQueryHandler(movie_categories, pattern="^categories$"),
                CallbackQueryHandler(main_menu, pattern="^main$"),
                CallbackQueryHandler(cancel, pattern="^cancel$"),
            ],
            MUSIC_MENU: [
                CallbackQueryHandler(main_menu, pattern="^main$"),
                CallbackQueryHandler(cancel, pattern="^cancel$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
