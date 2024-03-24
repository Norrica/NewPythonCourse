import re

from pyrogram import Client, filters
from pyrogram.types import Message, ForceReply
from pyrogram.enums import ParseMode


import buttons
import config
from custom_filters import button_filter, reply_text_filter
from keyboards import main_keyboard, settings_keyboard
from http_client import HttpClient


class Client(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.http_client = HttpClient()

    def stop(self, *args, **kwargs):
        self.http_client.close_session()
        return super().stop(*args, **kwargs)


bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name="tic_tac_toe_bot",
)


@bot.on_message(filters=filters.command("start") | button_filter(buttons.profile_button) | button_filter(buttons.back_button))
async def start_command(client: Client, message: Message):
    user = await client.http_client.get_user(message.from_user.id)
    if user is None:
        text = "Привет! Я бот, который помогает играть в игру 'Крестики-нолики'.\n\n" \
                "Ты ещё не зарегистрирован. Открой настройки, чтобы зарегистрироваться"
    else:
        text = f"Привет, {user.username}!\n\nТвой ID: `{user.user_id}`\n\nЧтобы посмотреть рейтинг, введи /rating."

    await client.send_message(
        chat_id=message.chat.id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_keyboard,
    )


@bot.on_message(filters=filters.command("rating") | button_filter(buttons.rating_button))
async def rating_command(client: Client, message: Message):
    user = await client.http_client.get_user(message.from_user.id)
    if user is None:
        return await message.reply("Ты не зарегистрирован. Используй настройки чтобы зарегистрироваться.")

    rating = await client.http_client.get_rating()
    if rating is None:
        return await message.reply("Не удалось получить рейтинг. Попробуйте позже.")

    found_in_first_10 = False

    text = "Топ-10 игроков:\n\n"
    for i, rating_user in enumerate(rating[:10]):
        if rating_user.username == user.username:
            found_in_first_10 = True
        text += f"{i + 1}. {rating_user.username} - {rating_user.wins}\n"

    if not found_in_first_10:
        me = None
        for rating_user in rating:
            if user.username == rating_user.username:
                me = rating_user
                break

        if me is not None:
            text += f"\nТвой рейтинг: {me.wins}"
        else:
            text += "\nТвой рейтинг: 0"

    await message.reply(text, reply_markup=main_keyboard)


@bot.on_message(filters=filters.command("settings") | button_filter(buttons.settings_button))
async def settings_command(client: Client, message: Message):
    text = "Здесь настройки. Тут можно поменять свой никнейм."
    await message.reply(text, reply_markup=settings_keyboard)


sign_up_text = "Ответь своим никнеймом на это сообщение, чтобы зарегистрироваться.\n\nНикнейм должен содержать от 3 до 9 символов и состоять из букв латинского алфавита и цифр."
@bot.on_message(filters=filters.command("sign_up") | button_filter(buttons.sign_up_button))
async def sign_up_command(client: Client, message: Message):
    user = await client.http_client.get_user(message.from_user.id)
    if user is not None:
         text = "Ты уже зарегистрирован."
    else:
        text = sign_up_text

    await message.reply(text, reply_markup=ForceReply(True) if user is None else settings_keyboard)


@bot.on_message(filters=filters.reply & reply_text_filter(sign_up_text))
async def sign_up_reply(client: Client, message: Message):
    validate = re.match(r"^[a-zA-Z0-9]{3,9}$", message.text)
    if validate is None:
        return await message.reply("Никнейм должен содержать от 3 до 9 символов и состоять из букв латинского алфавита и цифр.", reply_markup=settings_keyboard)

    user = await client.http_client.create_user(message.from_user.id, message.text)
    if user is None:
        return await message.reply("Не удалось зарегистрироваться. Попробуйте позже.", reply_markup=settings_keyboard)

    await message.reply("Регистрация прошла успешно!", reply_markup=settings_keyboard)


@bot.on_message()
async def unknown_message(client: Client, message: Message):
    await message.reply(
        "Неизвестная команда. "
        "Используйте кнопки внизу экрана, чтобы взаимодействовать с ботом."
    )


bot.run()
