from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
)

import src.config as config
from src.bot.handlers.common import cancel
from src.bot.handlers.date_menu import actual_date
from src.bot.handlers.main_menu import start, main_menu
from src.bot.handlers.movies_menu import movies_menu, movie_genres
from src.bot.handlers.music_menu import music_menu


def run():
    """Run the bot."""
    application = Application.builder().token(config.TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            config.MAIN_MENU: [
                CallbackQueryHandler(movies_menu, pattern="^movies$"),
                CallbackQueryHandler(actual_date, pattern="^date$"),
                CallbackQueryHandler(music_menu, pattern="^music$"),
                CallbackQueryHandler(cancel, pattern="^cancel$"),
            ],
            config.MOVIES_MENU: [
                CallbackQueryHandler(movie_genres, pattern="^genres$"),
                CallbackQueryHandler(main_menu, pattern="^main$"),
                CallbackQueryHandler(cancel, pattern="^cancel$"),
            ],
            config.MUSIC_MENU: [
                CallbackQueryHandler(main_menu, pattern="^main$"),
                CallbackQueryHandler(cancel, pattern="^cancel$"),
            ],
        },
        fallbacks=[
            CommandHandler("start", start),
            CommandHandler("cancel", cancel)
        ]
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("date", actual_date))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
