from aiogram import Dispatcher, types

from base.utils.choices import on_choice_action
from base.utils.messages import sending_messages_till_answer
from base.utils.storage import save_user


async def create_new_user(dp_data, user_id, username):
    dp_data["users"][user_id] = dp_data["default_user_model"].copy()
    dp_data["users"][user_id]["id"] = user_id
    dp_data["users"][user_id]["username"] = username.title()


async def echo(message: types.Message):
    dispatcher = Dispatcher.get_current()
    user_id = str(message.from_user.id)
    if user_id not in dispatcher.data["users"]:
        await create_new_user(dispatcher.data, user_id, message.from_user.first_name)
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
        await back_to_root_bot(message, finish=True)
        return


async def back_to_root_bot(message: types.Message, finish: bool = None):
    msg = "Больше историй ждет тебя в @el_patrona_bot 💋"
    inline_keyboard = types.InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="📚  Перейти в каталог историй",
                    url="https://t.me/el_patrona_bot",
                )
            ]
        ],
    )
    if finish:
        msg = "Cпасибо за прочтение!\n" + msg
        inline_keyboard.add(
            types.InlineKeyboardButton("Начать историю сначала", callback_data="restart")
        )
    await message.answer(
        text=msg,
        reply_markup=inline_keyboard,
    )


async def restart(query: types.CallbackQuery):
    user_id = str(query.from_user.id)
    dispatcher = Dispatcher.get_current()
    await create_new_user(dispatcher.data, user_id, dispatcher.data["users"][user_id]["username"])
    current_user = dispatcher.data["users"][user_id]
    await sending_messages_till_answer(dispatcher, current_user, user_id, "0")
