from aiogram import Dispatcher
from utils.commands import set_bot_commands
from storage.storage import load_data, save_data
from handlers import echo


async def on_startup(dp: Dispatcher):
    await set_bot_commands(dp)
    dp.data['dialogs'] = load_data("dialogs")
    dp.data['users'] = load_data("users")
    dp.register_message_handler(echo)


async def on_shutdown(dp: Dispatcher):
    """
    Method that is executed when the application exits
    """
    save_data("users", dp.data["users"])
    dp.stop_polling()
    await dp.wait_closed()
