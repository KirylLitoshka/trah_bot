from aiogram import executor, Dispatcher, Bot
from setting import BOT_KEY
from utils.utils import on_shutdown, on_startup


def main():
    bot = Bot("5673471591:AAGs9ztr7LGRjQ64tjE5YxqgVb7EgESAyh8")
    dispatcher = Dispatcher(bot)
    executor.start_polling(
        dispatcher=dispatcher,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True
    )


if __name__ == "__main__":
    main()
