from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.files import JSONStorage

from bot_mother.commands import set_bot_commands
from bot_mother.handlers import start, restart, process_gender, process_novel_link, change_language, \
    change_user_language
from bot_mother.profile import User
from bot_mother.settings import STORAGE_DIR


async def on_startup(dp: Dispatcher):
    await set_bot_commands(dp)
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(restart, commands=["restart"], state="*")
    dp.register_message_handler(change_language, commands=["language"], state="*")
    dp.register_callback_query_handler(
        change_user_language, lambda msg: msg.data == "ru" or msg.data == "en", state="*")
    dp.register_message_handler(process_gender, state=User.gender)
    dp.register_message_handler(process_novel_link, state=User.bot_type)


async def on_shutdown(dp: Dispatcher):
    dp.stop_polling()
    await dp.wait_closed()


def main():
    bot = Bot("")
    dispatcher = Dispatcher(bot, storage=JSONStorage(STORAGE_DIR))
    executor.start_polling(
        dispatcher=dispatcher,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True
    )


if __name__ == "__main__":
    main()
