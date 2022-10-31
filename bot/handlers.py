from aiogram import types, Dispatcher
from utils.messages import sending_messages_till_answer
from utils.choices import on_choice_action


async def create_new_user(dp_data, user_id):
    dp_data["users"][user_id] = {
        "last_received_message_id": None,
        "keks": 0,
        "loc": None,
        "registered_answers": [{"text": "/start", "next_id": "0", "on_choice": None}],
    }


async def echo(message: types.Message):
    dispatcher = Dispatcher.get_current()
    user_id = str(message.from_user.id)
    if user_id not in dispatcher.data["users"]:
        await create_new_user(dispatcher.data, user_id)
    current_user = dispatcher.data["users"][user_id]
    possible_answers = current_user["registered_answers"]
    answer_texts = [item["text"] for item in possible_answers]
    if message.text not in answer_texts:
        await dispatcher.bot.delete_message(message.chat.id, message.message_id)
        return
    current_user["registered_answers"] = []
    choice_index = answer_texts.index(message.text)
    if possible_answers[choice_index]["on_choice"]:
        on_choice_expression = possible_answers[choice_index]["on_choice"]
        on_choice_action(current_user, on_choice_expression)
    next_dialog_id = possible_answers[choice_index]["next_id"]
    current_user["last_received_message_id"] = next_dialog_id
    try:
        await sending_messages_till_answer(dispatcher, current_user, user_id, next_dialog_id)
    except KeyError:
        # Концовка (переделать, т.к выходит до отправки последнего сообщения)
        return
