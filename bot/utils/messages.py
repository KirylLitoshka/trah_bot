from setting import IMAGES_DIR, MEDIA_DIR
from aiogram.types import InputFile
from utils.keyboard import reply_keyboard
import asyncio


async def send_message(bot, user: dict, user_id: str, message_args: dict):
    if message_args["delay"]:
        await asyncio.sleep(message_args["delay"])
    if message_args["photo"]:
        await bot.send_photo(
            chat_id=user_id,
            photo=InputFile(f'{IMAGES_DIR}/{message_args["photo"]}'),
            caption=message_args["text"],
            reply_markup=reply_keyboard(user, message_args),
        )
    elif message_args["sticker"]:
        await bot.send_sticker(
            chat_id=user_id,
            sticker=message_args["sticker"],
            reply_markup=reply_keyboard(user, message_args),
        )
    elif message_args["voice"]:
        await bot.send_voice(
            chat_id=user_id,
            voice=InputFile(f"{MEDIA_DIR}/{message_args['voice']}"),
            caption=message_args["text"],
            reply_markup=reply_keyboard(user, message_args),
        )
    elif message_args["text"]:
        await bot.send_message(
            chat_id=user_id,
            text=message_args["text"],
            reply_markup=reply_keyboard(user, message_args),
        )
    else:
        print("CHECK MESSAGE TYPE!")  # replace with Exception
