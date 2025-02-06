from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def recent_books_list(books_data):
    builder = InlineKeyboardBuilder()
    for i, book in enumerate(books_data):
        builder.button(text=f"{i+1}", callback_data=f"id_{book['id']}")
    builder.adjust(5)
    return builder.as_markup() if builder.buttons else InlineKeyboardMarkup(inline_keyboard=[])

def book_keyboard(url, download):
    builder = InlineKeyboardBuilder()
    builder.button(text="↗️ Url", url=url)
    builder.button(text="📥 Download", url=download)
    builder.adjust(1)
    return builder.as_markup() if builder.buttons else InlineKeyboardMarkup(inline_keyboard=[])
