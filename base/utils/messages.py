import asyncio

from aiogram.types import InputFile, MediaGroup

from base.utils.keyboard import reply_keyboard
from base.utils.storage import save_user


async def sending_messages_till_answer(dispatcher, user, user_id, next_message_id):
    reply_message = dispatcher.data["dialogs"][next_message_id]
    while not reply_message["choices"]:
        await send_message(
            dispatcher=dispatcher,
            user=user,
            user_id=user_id,
            message_args=reply_message,
        )
        next_message_id = reply_message.get("jump_id") or str(int(next_message_id) + 1)
        reply_message = dispatcher.data["dialogs"][next_message_id]
        user["last_received_message_id"] = next_message_id
    await send_message(
        dispatcher=dispatcher,
        user=user,
        user_id=user_id,
        message_args=reply_message,
    )


async def send_message(dispatcher, user: dict, user_id: str, message_args: dict):
    bot = dispatcher.bot
    if message_args["delay"]:
        await asyncio.sleep(message_args["delay"])
    if message_args["photo"]:
        img_dir = dispatcher.data["dirs"]["IMAGES_DIR"]
        photo_gallery = message_args["photo"].split("%")
        if len(photo_gallery) == 1:
            await bot.send_photo(
                chat_id=user_id,
                photo=InputFile(f'{img_dir}/{message_args["photo"]}'),
                caption=message_args["text"],
                reply_markup=reply_keyboard(user, message_args),
            )
        else:
            media_group = MediaGroup()
            for photo in photo_gallery:
                media_group.attach_photo(InputFile(f"{img_dir}/{photo}"))
            await bot.send_media_group(
                chat_id=user_id,
                media=media_group,
            )
    elif message_args["sticker"]:
        await bot.send_sticker(
            chat_id=user_id,
            sticker=message_args["sticker"],
            reply_markup=reply_keyboard(user, message_args),
        )
    elif message_args["voice"]:
        media_dir = dispatcher.data["dirs"]["MEDIA_DIR"]
        await bot.send_voice(
            chat_id=user_id,
            voice=InputFile(f"{media_dir}/{message_args['voice']}"),
            caption=message_args["text"],
            reply_markup=reply_keyboard(user, message_args),
        )
    elif message_args["text"]:
        msg = message_args["text"]
        if "*" in msg:
            print(f"* in {msg:}")
            msg = msg.replace("*", user["username"])
        await bot.send_message(
            chat_id=user_id,
            text=msg,
            parse_mode="HTML",
            reply_markup=reply_keyboard(user, message_args),
        )
    else:
        print("CHECK MESSAGE TYPE!")  # replace with Exception
    await save_user(dispatcher, user_id, user)
