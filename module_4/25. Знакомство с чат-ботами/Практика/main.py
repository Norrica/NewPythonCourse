# Задание: создаём и настраиваем эхо-бота

from pyrogram import Client
from pyrogram.types import Message

import config

bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name="my_cool_bot",
)


@bot.on_message()
async def echo(client: Client, message: Message):
    await message.reply(message.text)


bot.run()
