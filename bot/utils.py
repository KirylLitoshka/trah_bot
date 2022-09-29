from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InputFile
from setting import IMAGES_DIR

async def send_message(message: Message, msg_option: dict):
    message_args = msg_option["message"]
    message_type = msg_option["type"]
    if message_type == "text":
        await message.answer(
            text=message_args["text"],
            reply_markup=build_keyboard(message_args)
        )
    elif message_type == "photo":
        await message.answer_photo(
            photo=InputFile(f'{IMAGES_DIR}/{message_args["photo"]}'),
            caption=message_args["text"],
            reply_markup=build_keyboard(message_args)
        )
    else:
        print("CHECK MESSAGE TYPE!")  # replace with Exception


def build_keyboard(args: dict):
    keyboard_args = args.get("keyboard", None)
    if keyboard_args is None:
        return None
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    # register_user_handle(keyboard_args)
    for keyboard_item in keyboard_args:
        keyboard.add(KeyboardButton(keyboard_item["text"]))
    return keyboard