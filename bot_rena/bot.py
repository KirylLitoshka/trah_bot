from aiogram import Bot, Dispatcher, executor

from base.utils.utils import on_shutdown, on_startup
from bot_rena.setting import DEFAULT_USER_MODEL, STORAGE_DIRS


def main():
    bot = Bot("5712278473:AAHEc7mG4LzyEESR0A2Jls88BToSI1Y6UH0")
    dispatcher = Dispatcher(bot)
    executor.start_polling(
        dispatcher=dispatcher,
        on_startup=on_startup(STORAGE_DIRS, DEFAULT_USER_MODEL),
        on_shutdown=on_shutdown,
        skip_updates=True
    )


if __name__ == "__main__":
    main()
