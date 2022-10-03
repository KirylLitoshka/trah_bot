from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InputFile, User
from aiogram import Dispatcher
from setting import IMAGES_DIR
import asyncio


async def send_message(message: Message, msg_option: dict):
    message_args = msg_option["message"]
    message_type = msg_option["type"]
    await asyncio.sleep(message_args.get("delay", 0.5))
    if message_type == "text":
        await message.answer(
            text=message_args["text"], reply_markup=build_keyboard(message_args)
        )
    elif message_type == "photo":
        await message.answer_photo(
            photo=InputFile(f'{IMAGES_DIR}/{message_args["photo"]}'),
            caption=message_args["text"],
            reply_markup=build_keyboard(message_args),
        )
    else:
        print("CHECK MESSAGE TYPE!")  # replace with Exception
    if "delayed_message" in msg_option:
        await send_message(message, msg_option["delayed_message"])


def build_keyboard(args: dict):
    keyboard_args = args.get("keyboard", None)
    if keyboard_args is None:
        return None
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    register_user_choices(keyboard_args)
    for keyboard_item in keyboard_args:
        keyboard.add(KeyboardButton(keyboard_item["text"]))
    return keyboard


def register_user_choices(kb_args: dict):
    user_id = str(User.get_current().id)
    users = Dispatcher.get_current().data["users"]
    users[user_id]["registered_messages"] = [x["text"] for x in kb_args]
    users[user_id]["registered_answers_id"] = [x["answer_id"] for x in kb_args]
