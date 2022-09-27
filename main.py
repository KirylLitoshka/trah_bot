from aiogram import Bot, Dispatcher, types, executor
import os

# options - local storage for telegram bot dialogs
options = {
    1: {
        "type": "photo",
        "message": {
            "photo": "static/img/dude.jpg",
            "text": "Привет",
            "keyboard": [
                {
                    "text": "Привет)"
                }
            ]
        },
        1: {
            "type": "text",
            "message": {
                "text": "Confirmed"
            }
        }
    }
}

API_KEY = os.environ.get("BOT_KEY")
bot = Bot(API_KEY)
dispatcher = Dispatcher(bot)
users = {}  # will be replaced by MongoDB storage


@dispatcher.message_handler(commands=["start"])
async def main(message: types.Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {"option_choices": [1]}
        await bot.send_message(message.from_user.id, text="У Вас есть новое совпадение")
    user_choice_sequence = users[message.from_user.id]["option_choices"]
    msg_option = get_option_sequence(user_choice_sequence)
    await send_message(message.from_user.id, msg_option)


@dispatcher.message_handler()
async def echo_check(message: types.Message):
    user = types.User.get_current()
    if message.text not in users[user.id]["registered_messages"]:
        print("message not in pool")  # test print if message not in user pool (need replace to Exception)
        await bot.delete_message(message.chat.id, message.message_id)
    next_index = users[user.id]["registered_messages"].index(message.text) + 1
    if not next_index:
        raise
    users[user.id]["option_choices"].append(next_index)
    user_choice_sequence = users[message.from_user.id]["option_choices"]
    msg_option = get_option_sequence(user_choice_sequence)
    await send_message(message.from_user.id, msg_option)


async def send_message(user_id: int, msg_option: dict):
    message_args = msg_option["message"]
    message_type = msg_option["type"]
    if message_type == "text":
        await bot.send_message(
            user_id,
            text=message_args["text"],
            reply_markup=build_keyboard(message_args)
        )
    elif message_type == "photo":
        await bot.send_photo(
            user_id,
            photo=types.InputFile(message_args["photo"]),
            caption=message_args["text"],
            reply_markup=build_keyboard(message_args)
        )
    else:
        print("CHECK MESSAGE TYPE!")  # replace with Exception


def build_keyboard(args: dict):
    keyboard_args = args.get("keyboard", None)
    if keyboard_args is None:
        return None
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    register_user_handle(keyboard_args)
    for keyboard_item in keyboard_args:
        keyboard.add(types.KeyboardButton(keyboard_item["text"]))
    return keyboard


def register_user_handle(args):
    user = types.User.get_current()
    users[user.id]["registered_messages"] = [x["text"] for x in args]


def get_option_sequence(indexes_list: list):
    result = None
    for index in indexes_list:
        if result is None:
            result = options[index]
        else:
            result = result[index]
    return result


if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=False)
