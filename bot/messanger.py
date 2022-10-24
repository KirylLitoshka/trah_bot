import asyncio
from aiogram import Bot
from aiogram.types import Message, InputFile, ReplyKeyboardRemove
from setting import IMAGES_DIR, MEDIA_DIR


class Messanger:
    def __init__(self, dialogs: dict, users: dict) -> None:
        self.dialogs = dialogs
        self.users = users
        self.bot = Bot.get_current()
        self.commands = ["/start", "/one_more"]

    async def create_new_user(self, user_id: str):
        self.users[user_id] = {
            "last_received_message_id": "0",
            "audacity": 0,
            "registered_answers": [{"answer_text": "/start", "next_id": "0"}],
        }

    async def send_message(self, message: Message, user_id: str):
        print(message.text)
        if user_id not in self.users:
            await self.create_new_user(user_id)
        current_user = self.users[user_id]
        user_registestered_answers = [
            item["answer_text"] for item in current_user["registered_answers"]
        ]
        if message.text not in user_registestered_answers:
            await self.bot.delete_message(message.chat.id, message.message_id)
            return
        choice_index = user_registestered_answers.index(message.text)
        reply_message_args = self.dialogs[
            current_user["registered_answers"][choice_index]["next_id"]
        ]
        await self._send_message(user_id, reply_message_args)
        if not reply_message_args["choices"]:
            reply_message_args = self.dialogs[current_user["last_received_message_id"]]
            await self._send_message(user_id, reply_message_args)

    async def _send_message(self, user_id: str, message_args: dict):
        if message_args["delay"]:
            await asyncio.sleep(message_args["delay"])
        if message_args["photo"]:
            await self.bot.send_photo(
                chat_id=user_id,
                photo=InputFile(f'{IMAGES_DIR}/{message_args["photo"]}'),
                caption=message_args["text"],
                reply_markup=self._build_reply_keyboard(user_id, message_args),
            )
        elif message_args["sticker"]:
            await self.bot.send_sticker(
                chat_id=user_id,
                sticker=message_args["sticker"],
                reply_markup=self._build_reply_keyboard(user_id, message_args),
            )
        elif message_args["voice"]:
            await self.bot.send_voice(
                chat_id=user_id,
                voice=InputFile(f"{MEDIA_DIR}/{message_args['voice']}"),
                caption=message_args["text"],
                reply_markup=self._build_reply_keyboard(user_id, message_args),
            )
        elif message_args["text"]:
            await self.bot.send_message(
                chat_id=user_id,
                text=message_args["text"],
                reply_markup=self._build_reply_keyboard(user_id, message_args),
            )
        else:
            print("CHECK MESSAGE TYPE!")  # replace with Exception

    def _build_reply_keyboard(self, user_id, message_args):
        if not message_args["choices"]:
            self.users[user_id]["registered_answers"] = []
            return ReplyKeyboardRemove()
        print(message_args)
