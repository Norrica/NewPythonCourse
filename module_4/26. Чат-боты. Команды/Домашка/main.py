# Задание: Добавьте команду /help, которая будет
#          выводить список всех доступных команд.
#          Подсказка: используйте метод get_bot_commands
#          Удалите хендлер echo, он больше не нужен.
#          Вместо него должна быть отбивка о неизвестной команде.
#          Важно зарегистрировать хендлер для неизвестной
#          команды последним, чтобы он не перехватывал другие команды.
#          Добавьте команду /start, которая будет выводить
#          приветственное сообщение с подсказкой воспользоваться /help.


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


@bot.on_message(filters=filters.command("help"))
async def help_command(client: Client, message: Message):
    commands = await bot.get_bot_commands()
    text_commands = ""
    for command in commands:
        text_commands += f"/{command.command} - {command.description}\n"
    await message.reply(f"Список доступных команд:\n{text_commands}")


@bot.on_message(filters=filters.command("start"))
async def start_command(client: Client, message: Message):
    await message.reply(
        "Привет! Я бот, который умеет считать и показывать время.\n"
        f"Нажми на /help, чтобы узнать, что я умею."
    )


@bot.on_message()
async def unknown_message(client: Client, message: Message):
    await message.reply(
        "Неизвестная команда. "
        "Введите /help для получения списка команд"
    )


bot.run()
