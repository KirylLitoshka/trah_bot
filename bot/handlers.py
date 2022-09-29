from aiogram.types import Message, User
from aiogram import Dispatcher, Bot
from utils import send_message




async def start(message: Message):
    users = Dispatcher.get_current().data["users"]
    options = Dispatcher.get_current().data["conversation"]
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {"option_choiced": "1"}
        await message.answer(text="У Вас есть новое совпадение")
        await send_message(message, options[users[user_id]["option_choiced"]])



async def echo(message: Message):
    # users = Dispatcher.get_current().data["users"]
    # user_id = message.from_user.id
    # try:
    #     if not users[user_id]:
    #         users[user_id] = {}
    #     users[user.id] = {
    #         "registered_messages": users[user.id].get("registered_messages", []),
    #         "option_choices": users[user.id].get("option_choices", [])
    #     }
    #     if message.text not in users[user.id]["registered_messages"]:
    #         # test print if message not in user pool (need replace to Exception)
    #         print("message not in pool")
    #         await bot.delete_message(message.chat.id, message.message_id)
    #     else:
    #         next_index = users[user.id]["registered_messages"].index(
    #             message.text) + 1
    #         users[user.id]["option_choices"].append(next_index)
    # except KeyError:
    #     print("KEY ERROR")
    # user_choice_sequence = [1] if not users[user.id].get(
    #     "option_choices") else users[user.id]["option_choices"]
    # msg_option = get_option_sequence(user_choice_sequence)
    # await send_message(message.from_user.id, msg_option)
    await message.answer(message.text)
