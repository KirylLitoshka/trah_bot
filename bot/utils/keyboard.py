from aiogram import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


def reply_keyboard(user, message_args):
    dialogs = Dispatcher.get_current().data["dialogs"]
    if not message_args["choices"]:
        user["registered_answers"] = []
        return ReplyKeyboardRemove()
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        user_answers = []
        for index, choice in enumerate(message_args["choices"]):
            choice_message = dialogs[choice]
            keyboard.add(KeyboardButton(choice_message["text"]))
            next_id = (
                choice_message["jump_id"]
                if choice_message["jump_id"]
                else str(int(choice) + 1)
            )
            on_choice = None
            if message_args["choices_param"]:
                on_choice = message_args["choices_param"][index]["on_choice"]
            user_answers.append(
                {
                    "text": choice_message["text"],
                    "next_id": next_id,
                    "on_choice": on_choice,
                }
            )
        user["registered_answers"] = user_answers
        return keyboard
