from aiogram.types import (
    Message,
    BotCommand,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


async def set_bot_commands(dispatcher):  # dispatcher: Dispatcher
        await dispatcher.bot.set_my_commands(
            [
                BotCommand("continue", "Продолжить"),
                BotCommand("back", "Вернуться в рут-бот"),
            ]
        )


async def back(message: Message):
    inline_keyboard = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Тыц",
                    url="",  # link to root bot
                )
            ]
        ],
    )
    await message.answer(
        text="Для перехода в основной канал нажмите кнопку ниже",
        reply_markup=inline_keyboard,
    )
