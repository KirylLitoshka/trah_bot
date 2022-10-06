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
    elif message_type == "sticker":
        await message.answer_sticker(
            sticker=message_args["sticker_id"],
            reply_markup=build_keyboard(message_args)
        )
    else:
        print("CHECK MESSAGE TYPE!")  # replace with Exception
    if "delayed_message" in msg_option:
        await send_message(message, msg_option["delayed_message"])


def build_keyboard(args: dict):
    keyboard_args = args.get("keyboard", None)
    check_relationship = args["check_relationship"]
    if keyboard_args is None:
        return
    keyboard_args = register_user_choices(check_relationship, keyboard_args)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for keyboard_item in keyboard_args:
        keyboard.add(KeyboardButton(keyboard_item["text"]))
    return keyboard


def register_user_choices(check_relationship: bool, keyboard_data: list):
    user_id = str(User.get_current().id)
    users = Dispatcher.get_current().data["users"]
    if check_relationship:
        keyboard_data = keyboard_data[1:] if users[user_id]["relationship"] >= 0 else keyboard_data[:1]
    users[user_id]["registered_messages"] = [x["text"] for x in keyboard_data]
    users[user_id]["registered_answers_id"] = [x["answer_id"] for x in keyboard_data]
    return keyboard_data
