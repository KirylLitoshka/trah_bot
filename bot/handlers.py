from aiogram.types import Message
from aiogram import Dispatcher, Bot
from utils import send_message


async def start(message: Message):
    users = Dispatcher.get_current().data["users"]
    options = Dispatcher.get_current().data["conversation"]
    user_id = str(message.from_user.id)
    if user_id not in users or "last_choiced_option" not in users[user_id]:
        users[user_id] = {"last_choiced_option": "1"}
        await message.answer(text="У Вас есть новое совпадение")
    await send_message(message, options[users[user_id]["last_choiced_option"]])


async def echo(message: Message):
    dispatcher = Dispatcher.get_current()
    users = dispatcher.data["users"]
    options = dispatcher.data["conversation"]
    user_id = str(message.from_user.id)
    bot = Bot.get_current()
    if user_id not in users:
        users[user_id] = {}
        await start(message)
        await bot.delete_message(message.chat.id, message.message_id)
        return
    users[user_id].setdefault("registered_messages", [])
    users[user_id].setdefault("last_choiced_option", "1")
    users[user_id].setdefault("relationship", 0)
    if users[user_id]["last_choiced_option"] == list(options.keys())[-1]:
        users[user_id]["registered_messages"] = []
        users[user_id]["registered_answers_id"] = []
    if message.text not in users[user_id]["registered_messages"]:
        await bot.delete_message(message.chat.id, message.message_id)
        return
    else:
        choice_index = users[user_id]["registered_messages"].index(message.text)
        if len(users[user_id]["registered_messages"]) > 1 :
            relation_choice_value = -1 if choice_index == 0 else 1
            users[user_id]["relationship"] += relation_choice_value
        users[user_id]["last_choiced_option"] = users[user_id]["registered_answers_id"][choice_index]
    await send_message(message, options[users[user_id]["last_choiced_option"]])

