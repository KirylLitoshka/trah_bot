from aiogram import executor, Dispatcher, Bot
from setting import BOT_KEY
from messanger import Messanger
from storage import load_data, save_data
from utils import set_bot_commands
from handlers import start, echo, back


async def on_startup(dp: Dispatcher):
    await set_bot_commands(dp)
    dialogs = await load_data("dialogs") 
    users = await load_data("users")
    dp.data['messanger'] = Messanger(dialogs, users)
    # dp.register_message_handler(start, commands=["start", "continue"])
    # dp.register_message_handler(back, commands=["back"])
    dp.register_message_handler(echo)


async def on_shutdown(dp: Dispatcher):
    """
    Method that is executed when the application exits
    """
    dp.stop_polling()
    await save_data("users", dp.data["users"])
    await dp.wait_closed()


def main():
    bot = Bot(BOT_KEY)
    dispatcher = Dispatcher(bot)
    executor.start_polling(
        dispatcher=dispatcher, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True
    )


if __name__ == "__main__":
    main()
