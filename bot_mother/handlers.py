from aiogram import Bot, Dispatcher, types

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
            "real": "https://t.me/denise_el_patrona_bot",
            "photo": "https://t.me/bruna_el_patrona_bot",
            "anime": "https://t.me/TestCucumber2Bot"
        },
        "male": {
            "real": "https://t.me/danielle_el_patrona_bot",
            "photo": "https://t.me/danielle_el_patrona_bot",
            "anime": "https://t.me/danielle_el_patrona_bot"
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
    users[user_id]["gender"] = next(
        (key for key, val in menu["gender"].items() if val == message.text), None)
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
    current_user["picture_type"] = next(
        (key for key, val in menu["picture_type"].items() if val == message.text), None)
    current_user["current_choices"] = "novels"
    novel_link = menu["novels"][current_user["gender"]
                                ][current_user["picture_type"]]
    await message.answer(
        text="Твой собеседник уже ждет тебя в чате.\nПереходи по ссылке",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("Начать общение", url=novel_link))
    )


async def restart(message: types.Message):
    users = Dispatcher.get_current().data["users"]
    try:
        del users[str(message.from_user.id)]
        await gender_selection(message)
    except KeyError:
        await gender_selection(message)
