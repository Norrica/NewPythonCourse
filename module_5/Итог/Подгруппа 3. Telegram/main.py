import re

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, ForceReply

import config
from custom_filters import reply_text_filter
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
    name="my_cool_bot",
)

new_user_text = "Привет! Я бот, который помогает играть в игру 'Крестики-нолики'.\n" \
                "Ты ещё не зарегистрирован. Ответь своим никнеймом на это сообщение, чтобы зарегистрироваться.\n\n" \
                "Никнейм должен содержать от 3 до 9 символов и состоять из букв латинского алфавита и цифр."


@bot.on_message(filters=filters.command("start"))
async def start_command(client: Client, message: Message):
    user = await client.http_client.get_user(message.from_user.id)
    if user is None:
        text = new_user_text
    else:
        text = f"Привет, {user.username}!\n\nТвой ID: `{user.user_id}`\n\nЧтобы посмотреть рейтинг, введи /rating."

    force_reply = ForceReply(True) if user is None else None

    await client.send_message(
        chat_id=message.chat.id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=force_reply,
    )


@bot.on_message(filters=filters.command("rating"))
async def settings_command(client: Client, message: Message):
    user = await client.http_client.get_user(message.from_user.id)
    if user is None:
        return await message.reply("Ты не зарегистрирован. Используй /start, чтобы зарегистрироваться.")

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
        me = next((rating_user for rating_user in rating if user.username == rating_user.username), None)
        if me is not None:
            text += f"\nТвой рейтинг: {me.wins}"
        else:
            text += "\nТвой рейтинг: 0"

    await message.reply(text)


@bot.on_message(filters=filters.reply & reply_text_filter(new_user_text))
async def change_city_reply(client: Client, message: Message):
    validate = re.match(r"^[a-zA-Z0-9]{3,9}$", message.text)
    if validate is None:
        return await message.reply("Никнейм должен содержать от 3 до 9 символов и состоять из букв латинского алфавита и цифр.")

    user = await client.http_client.create_user(message.from_user.id, message.text)
    if user is None:
        return await message.reply("Не удалось зарегистрироваться. Попробуйте позже.")

    await message.reply("Регистрация прошла успешно!")


@bot.on_message()
async def unknown_message(client: Client, message: Message):
    await message.reply(
        "Неизвестная команда. "
        "Введите /help для получения списка команд"
    )


bot.run()
