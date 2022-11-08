from aiogram import Bot, Dispatcher, executor

from bot_mother.commands import set_bot_commands
from bot_mother.handlers import (gender_selection, menu, novel_selection,
                                 picture_type_selection)
from bot_mother.storage import set_users


async def on_startup(dp: Dispatcher):
    await set_bot_commands(dp)
    set_users(dispatcher=dp)
    dp.register_message_handler(gender_selection, commands=["start"])
    dp.register_message_handler(
        picture_type_selection,
        lambda msg: msg.text in menu["gender"].values()
    )
    dp.register_message_handler(
        novel_selection,
        lambda msg: msg.text in menu["picture_type"].values()
    )


async def on_shutdown(dp: Dispatcher):
    dp.stop_polling()
    await dp.wait_closed()


def main():
    bot = Bot("5767674258:AAHmpIMRYeEFupfYt9M553DoP2GTXgLRJh8")
    dispatcher = Dispatcher(bot)
    executor.start_polling(
        dispatcher=dispatcher,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True
    )


if __name__ == "__main__":
    main()
