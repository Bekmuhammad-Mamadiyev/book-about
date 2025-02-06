import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import Command
import asyncio
import aiohttp

from config import API_TOKEN
from keyboards import book_keyboard, recent_books_list

logging.basicConfig(level=logging.INFO)

session = AiohttpSession()
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML, session=session)
dp = Dispatcher()


@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Xush kelibsiz.Botdagi kitoblar dbooks.org ushbu saytdan olinmoqda.")


@dp.message(F.text)
async def search_book(message: Message):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f'https://www.dbooks.org/api/search/{message.text}') as response:
                data = await response.json()
                if data.get("status") == "ok":
                    books = data["books"][:20]
                    ans_title = f"Results: {len(books)}"
                    ans_content = [
                        f"<b>{i + 1}.</b> {book['title']}   -   <i>{book['authors']}</i>"
                        for i, book in enumerate(books)
                    ]

                    ans = ans_title + "\n\n" + "\n\n".join(ans_content)
                    await message.answer(text=ans, reply_markup=recent_books_list(books_data=books))
                else:
                    await message.answer("Book not found 😭")
        except Exception as e:
            logging.error(e)


@dp.callback_query(F.data.startswith("id_"))
async def choosing_interests(query: CallbackQuery):
    await query.message.delete()
    book_id = query.data.split("_")[1]
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f'https://www.dbooks.org/api/book/{book_id}') as response:
                data = await response.json()
                if data.get("status") == "ok":
                    book_title = data['title']
                    book_description = data['description']
                    book_authors = data['authors']
                    book_publisher = data['publisher']
                    book_pages = data['pages']
                    book_year = data['year']
                    book_image = data['image']
                    book_url = data['url']
                    book_download = data['download']

                    content = (
                        f"<b>Title:</b> {book_title}\n\n"
                        f"<b>Description:</b> {book_description}\n\n"
                        f"<b>Authors:</b> <i>{book_authors}</i>\n\n"
                        f"<b>Publisher:</b> {book_publisher}\n"
                        f"<b>Pages:</b> {book_pages}\n"
                        f"<b>Year:</b> {book_year}\n"
                    )

                    await query.message.answer_photo(
                        photo=book_image,
                        caption=content,
                        reply_markup=book_keyboard(url=book_url, download=book_download)
                    )
        except Exception as e:
            logging.error(e)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
