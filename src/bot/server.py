from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

import src.config as config
from src.bot.handlers.common import cancel
from src.bot.handlers.conversation import handle_conversation
from src.bot.handlers.date_menu import get_actual_date
from src.bot.handlers.main_menu import start, main_menu
from src.bot.handlers.movies_menu import movies_menu, movie_genres, search_movie_handler
from src.bot.handlers.music_menu import music_menu
from src.bot.handlers.weather_menu import get_weather


def run():
    """Run the bot."""
    application = Application.builder().token(config.TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            config.MAIN_MENU: [
                CallbackQueryHandler(movies_menu, pattern="^movies$"),
                CallbackQueryHandler(get_actual_date, pattern="^date$"),
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
    application.add_handler(CommandHandler("fecha", get_actual_date))
    application.add_handler(CommandHandler("clima", get_weather))
    application.add_handler(CommandHandler("pelicula", search_movie_handler))

    # Handler for normal conversation (text messages that are not commands)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_conversation)
    )

    application.run_polling(allowed_updates=Update.ALL_TYPES)
