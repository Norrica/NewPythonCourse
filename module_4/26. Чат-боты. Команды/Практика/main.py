# Задание 1: Напишите бота, который отвечает
#            на команду /time текущим временем
#            в формате HH:MM:SS
#
# Задание 2: Напишите бота, который принимает
#            команду /calc <число> <оператор> <число>
#            и возвращает результат операции
#
#            Добавьте обе команды в botfather


import random
import time
import operator

from pyrogram import Client, filters
from pyrogram.types import Message

import config

bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name="my_cool_bot",
)


@bot.on_message(filters=filters.command("time"))
async def time_command(client: Client, message: Message):
    current_time = time.strftime("%H:%M:%S")
    await message.reply(f"Текущее время: {current_time}")


@bot.on_message(filters=filters.command("calc"))
async def calc_command(client: Client, message: Message):
    ops = {
        "+": operator.add, "-": operator.sub,
        "*": operator.mul, "/": operator.truediv,
    }

    if len(message.command) != 4:
        await message.reply(
            "Неверное количество аргументов\n"
            "Пример использования:\n"
            "/calc 1 + 2\n"
            "Поддерживаемые операторы: +, -, *, /"
        )
        return

    _, left, op, right = message.command
    op = ops.get(op)
    if op is None:
        await message.reply("Неизвестный оператор")
        return
    if not left.isdigit() or not right.isdigit():
        await message.reply("Аргументы должны быть числами")
        return

    left, right = int(left), int(right)
    await message.reply(f"Результат: {op(left, right)}")


@bot.on_message()
async def echo(client: Client, message: Message):
    text = message.text
    if random.choice([True, False]):
        await message.reply(text)
    else:
        await message.reply(text[::-1])


bot.run()
