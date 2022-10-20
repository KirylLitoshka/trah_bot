from aiogram import Bot
from aiogram.types import Message

class Messanger:
    def __init__(self, dialogs: dict) -> None:
        self.dialogs = dialogs
        self.bot = Bot.get_current()
        self.commands = ["/start", "/one_more"]


    async def send_message(self, message: Message):
        user_id = message.from_user.id
        await self.bot.send_message(user_id, "echo")

        
        