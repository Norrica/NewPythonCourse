import time
import operator

from pyrogram import Client, filters
from pyrogram.types import Message

import buttons
import config
import keyboards
from custom_filters import button_filter
from weather import get_current_weather, get_forecast


bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name="my_cool_bot",
)


@bot.on_message(filters=filters.command("time") | button_filter(buttons.time_button))
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


@bot.on_message(filters=filters.command("help") | button_filter(buttons.help_button))
async def help_command(client: Client, message: Message):
    commands = await bot.get_bot_commands()
    text_commands = ""
    for command in commands:
        text_commands += f"/{command.command} - {command.description}\n"
    await message.reply(f"Список доступных команд:\n{text_commands}")


@bot.on_message(filters=filters.command("start") | button_filter(buttons.back_button))
async def start_command(client: Client, message: Message):
    await message.reply(
        "Привет! Я бот, который умеет считать и показывать время.\n"
        f"Нажми на кнопку {buttons.help_button.text} для получения списка команд.",
        reply_markup=keyboards.main_keyboard
    )


@bot.on_message(filters=filters.command("settings") | button_filter(buttons.settings_button))
async def settings_command(client: Client, message: Message):
    await message.reply(
        "Настройки",
        reply_markup=keyboards.settings_keyboard
    )


@bot.on_message(filters=filters.command("weather") | button_filter(buttons.weather_button))
async def weather_command(client: Client, message: Message):
    if message.command and len(message.command) > 1:
        city = message.command[1]
    else:
        city = "Москва"

    weather = get_current_weather(city)

    await message.reply(weather)


@bot.on_message(filters=filters.command("change_city") | button_filter(buttons.change_city_button))
async def change_city_command(client: Client, message: Message):
    await message.reply(
        "Эта функция пока не работает, но скоро заработает!"
    )


@bot.on_message()
async def unknown_message(client: Client, message: Message):
    await message.reply(
        "Неизвестная команда. "
        "Введите /help для получения списка команд"
    )


bot.run()
