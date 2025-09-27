from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🎬 Películas", callback_data="movies")],
        [InlineKeyboardButton("🎵 Música", callback_data="music")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_movies_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("📂 Buscar categorías", callback_data="categories")],
        [InlineKeyboardButton("🔙 Volver", callback_data="main")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_music_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🔙 Volver", callback_data="main")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)
