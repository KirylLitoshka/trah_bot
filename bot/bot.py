from aiogram import executor, Dispatcher, Bot
from setting import BOT_KEY
from utils.utils import on_shutdown, on_startup


def main():
    bot = Bot(BOT_KEY)
    dispatcher = Dispatcher(bot)
    executor.start_polling(
        dispatcher=dispatcher,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True
    )


if __name__ == "__main__":
    main()
