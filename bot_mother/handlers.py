from aiogram import types
from aiogram.dispatcher import FSMContext
from bot_mother.profile import User
from bot_mother.settings import GENDER_CHOICES, BOT_TYPES, NOVELS_LINK, NOVELS_TEXT


async def start(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state in User.states:
        return
    async with state.proxy() as data:
        if "language" not in data:
            await User.language.set()
            user_language = "ru" if message.from_user.language_code == "ru" else "en"
            data["language"] = user_language
            await User.next()
        else:
            await User.gender.set()
        user_language = data['language']
    await message.answer(
        text=GENDER_CHOICES[user_language]['text'],
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text)] for text in GENDER_CHOICES[user_language]["buttons"]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


async def process_gender(message: types.Message, state: FSMContext):
    if message.text == "/restart":
        return await restart(message, state)
    elif message.text == "/language":
        return await change_language(message)
    async with state.proxy() as data:
        user_language = data['language']
        if message.text not in GENDER_CHOICES[user_language]["buttons"]:
            return await message.delete()
        data["gender"] = message.text
    await User.next()
    await message.answer(
        text=BOT_TYPES[user_language]["text"],
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text)] for text in BOT_TYPES[user_language]["buttons"]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        ),
        parse_mode="HTML"
    )


async def process_novel_link(message: types.Message, state: FSMContext):
    if message.text == "/restart":
        return await restart(message, state)
    elif message.text == "/language":
        return await change_language(message)
    async with state.proxy() as data:
        user_language = data['language']
        if message.text not in BOT_TYPES[user_language]["buttons"]:
            return await message.delete()
        data["bot_type"] = message.text
        link = NOVELS_LINK[user_language][data["gender"]][data["bot_type"]]
        await message.answer(
            text=NOVELS_TEXT[user_language]["text"],
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[[
                    types.InlineKeyboardButton(
                        text=NOVELS_TEXT[user_language]["link_text"],
                        url=link
                    )]]
            ),
        )
    await state.set_state("*")


async def change_language(message: types.Message):
    await message.answer(
        text="Choose your language",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[[
                types.InlineKeyboardButton("RU", callback_data="ru"),
                types.InlineKeyboardButton("EN", callback_data="en")
            ]]
        )
    )


async def change_user_language(query: types.CallbackQuery, state: FSMContext):
    language = query.data
    async with state.proxy() as data:
        data['language'] = language
    await restart(query.message, state)


async def restart(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.set_state(None)
    await start(message, state)
