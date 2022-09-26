import asyncio
import os

from aiogram import Bot, Dispatcher, types, executor

API_KEY = os.environ.get("BOT_KEY")
bot = Bot(API_KEY)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=["start"])
async def main(message: types.Message):
    await bot.send_message(message.from_user.id, text="У Вас есть новое совпадение")
    await asyncio.sleep(0.2)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.KeyboardButton("Привет)", callback_data="hello"))
    await bot.send_photo(message.from_user.id, photo=types.InputFile("static/img/hooty.jpg"), reply_markup=keyboard)


@dispatcher.callback_query_handler(text="hello")
async def button_callback(message: types.Message):
    await bot.send_message(message.from_user.id, text="Привет)")


if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=False)
