import re
from aiogram import Dispatcher
from utils.commands import set_bot_commands
from storage.storage import load_data, save_data
from handlers import echo


async def on_startup(dp: Dispatcher):
    await set_bot_commands(dp)
    dp.data["dialogs"] = load_data("dialogs")
    dp.data["users"] = load_data("users")
    dp.register_message_handler(echo)


async def on_shutdown(dp: Dispatcher):
    """
    Method that is executed when the application exits
    """
    save_data("users", dp.data["users"])
    dp.stop_polling()
    await dp.wait_closed()


def check_args():
    pass


def on_choice_action(user: dict, applied_expession):
    param_name = re.search("[a-z]+", applied_expession).group()
    if param_name in user:
        expression_sign = re.search("[+|-]+", applied_expession).group()
        expression_value = re.search("[0-9]+", applied_expession).group()
        pass
