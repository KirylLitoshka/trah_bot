import pathlib
import json
import os
from aiogram import Dispatcher, Bot, executor, types

STORAGE_DIR = os.path.join(pathlib.Path(__file__).parent, "storage")


async def on_startup(dp: Dispatcher):
    with open(f"{STORAGE_DIR}/users.json", mode="r", encoding="utf8") as user_storage:
        users_data = json.loads(user_storage.read())
        dp.data['users'] = users_data

    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "💟 Перезапустить бота")
        ]
    )
    dp.register_message_handler(gender_selection, commands=["start"])
    dp.register_message_handler(picture_type_selection, lambda msg: msg.text in menu["gender"].values())
    dp.register_message_handler(novel_selection, lambda msg: msg.text in menu["picture_type"].values())


async def on_shutdown(dp: Dispatcher):
    dp.stop_polling()
    await dp.wait_closed()


menu = {
    "gender": {
        "male": "💁‍♂️ Парни",
        "female": "💁‍♀️ Девушки"
    },
    "picture_type": {
        "real": "💋 Реалистичные 2D арты",
        "photo": "📸 Фотографии",
        "anime": "🍭 Аниме 2D арты"
    },
    "novels": {
        "female": {
            "real": "https://t.me/TestCucumber2Bot",
            "photo": "https://t.me/TestCucumber2Bot",
            "anime": "https://t.me/TestCucumber2Bot"
        },
        "male": {
            "real": "https://t.me/TestCucumberBot",
            "photo": "https://t.me/TestCucumberBot",
            "anime": "https://t.me/TestCucumberBot"
        }
    }
}


async def create_new_user(user_id, users_storage):
    users_storage[str(user_id)] = {
        "gender": None,
        "picture_type": None,
        "current_choices": "gender"
    }


async def gender_selection(message: types.Message):
    users = Dispatcher.get_current().data["users"]
    if message.from_user.id not in users:
        await create_new_user(message.from_user.id, users)
    await message.answer(
        text="С кем ты хочешь начать свой диалог?",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton("💁‍♂️ Парни")],
                [types.KeyboardButton("💁‍♀️ Девушки")],
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


async def picture_type_selection(message: types.Message):
    users = Dispatcher.get_current().data["users"]
    user_id = str(message.from_user.id)
    if message.text not in menu[users[user_id]["current_choices"]].values():
        await Bot.get_current().delete_message(message.chat.id, message.message_id)
    users[user_id]["gender"] = next((key for key, val in menu["gender"].items() if val == message.text), None)
    users[user_id]["current_choices"] = "picture_type"
    await message.answer(
        text="Выберите визуальный стиль изображений в истории.\n\n"
             "<i>В наших историях Вы можете увидеть арты и фотографии с контентом сексуального характера 🔞</i>",
        parse_mode="HTML",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton("💋 Реалистичные 2D арты")],
                [types.KeyboardButton("📸 Фотографии")],
                [types.KeyboardButton("🍭 Аниме 2D арты")],
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


async def novel_selection(message: types.Message):
    users = Dispatcher.get_current().data["users"]
    user_id = str(message.from_user.id)
    current_user = users[user_id]
    if message.text not in menu[users[user_id]["current_choices"]].values():
        await Bot.get_current().delete_message(message.chat.id, message.message_id)
    current_user["picture_type"] = next((key for key, val in menu["picture_type"].items() if val == message.text), None)
    current_user["current_choices"] = "novels"
    novel_link = menu["novels"][current_user["gender"]][current_user["picture_type"]]
    await message.answer(
        text="Твой собеседник уже ждет тебя в чате.\nПереходи по ссылке",
        reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Начать общение", url=novel_link))
    )


async def restart(message: types.Message):
    users = Dispatcher.get_current().data["users"]
    try:
        del users[str(message.from_user.id)]
        await gender_selection(message)
    except KeyError:
        await gender_selection(message)


def main():
    bot = Bot("5767674258:AAHmpIMRYeEFupfYt9M553DoP2GTXgLRJh8")
    dispatcher = Dispatcher(bot)
    executor.start_polling(
        dispatcher=dispatcher,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True
    )


if __name__ == "__main__":
    main()
