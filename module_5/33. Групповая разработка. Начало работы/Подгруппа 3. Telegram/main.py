from pyrogram import Client, filters
from pyrogram.types import Message

import buttons
import config
from custom_filters import button_filter
from keyboards import main_keyboard, settings_keyboard

bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name="tic_tac_toe_bot",
)


@bot.on_message(filters=filters.command("start") | button_filter(buttons.profile_button) | button_filter(buttons.back_button))
async def start_command(client: Client, message: Message):
    await client.send_message(
        chat_id=message.chat.id,
        text="Привет! Я бот, который помогает играть в игру 'Крестики-нолики'.",
        reply_markup=main_keyboard,
    )


@bot.on_message(filters=filters.command("rating") | button_filter(buttons.rating_button))
async def rating_command(client: Client, message: Message):
    text = "Я пока не умею показывать рейтинг. Но обязательно научусь!"
    await message.reply(text, reply_markup=main_keyboard)


@bot.on_message(filters=filters.command("settings") | button_filter(buttons.settings_button))
async def settings_command(client: Client, message: Message):
    text = "Здесь будут настройки. Но их пока нет."
    await message.reply(text, reply_markup=settings_keyboard)


@bot.on_message(filters=filters.command("sign_up") | button_filter(buttons.sign_up_button))
async def sign_up_command(client: Client, message: Message):
    text = "Здесь будет регистрация. Но её пока нет."
    await message.reply(text, reply_markup=settings_keyboard)


@bot.on_message()
async def unknown_message(client: Client, message: Message):
    await message.reply(
        "Неизвестная команда. "
        "Используйте кнопки внизу экрана, чтобы взаимодействовать с ботом."
    )


bot.run()
