from aiogram import Bot, Dispatcher, executor

from base.utils.utils import on_shutdown, on_startup
from bot_daniel.setting import DEFAULT_USER_MODEL, STORAGE_DIRS


def main():
    bot = Bot("5585358026:AAFZ_MdfbBW70b2Ds9QdtqBXfLmHI1cjBb4")
    dispatcher = Dispatcher(bot)
    executor.start_polling(
        dispatcher=dispatcher,
        on_startup=on_startup(STORAGE_DIRS, DEFAULT_USER_MODEL),
        on_shutdown=on_shutdown,
        skip_updates=True
    )


if __name__ == "__main__":
    main()
