# Задание: добавляем рандомайзер в хендлер echo,
#          бот отвечает либо эхом, либо перевёрнутым сообщением

import random

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
    text = message.text
    if random.choice([True, False]):
        await message.reply(text)
    else:
        await message.reply(text[::-1])


bot.run()
