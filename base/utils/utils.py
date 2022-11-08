from aiogram import Dispatcher

from base.handlers import back_to_root_bot, echo, restart
from base.utils.commands import set_bot_commands
from base.utils.storage import load_data, save_data


def on_startup(dirs, user_model):
    async def wrapper(dp: Dispatcher):
        await set_bot_commands(dp)
        dp.data["dirs"] = dirs
        dp.data["dialogs"] = load_data(dp.data["dirs"]["STORAGE_DIR"], "dialogs")
        dp.data["users"] = load_data(dp.data["dirs"]["STORAGE_DIR"], "users")
        dp.data["default_user_model"] = user_model
        dp.register_callback_query_handler(restart, lambda cmd: cmd.data == "restart")
        dp.register_message_handler(back_to_root_bot, commands=["back"])
        dp.register_message_handler(echo)

    return wrapper


async def on_shutdown(dp: Dispatcher):
    """
    Method that is executed when the application exits
    """
    save_data(dp.data["dirs"]["STORAGE_DIR"], "users", dp.data["users"])
    dp.stop_polling()
    await dp.wait_closed()
