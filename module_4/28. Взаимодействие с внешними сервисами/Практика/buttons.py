from pyrogram.types import KeyboardButton
from pyrogram import emoji

# Общие кнопки
back_button = KeyboardButton(f"{emoji.BACK_ARROW} Назад")

# Кнопки главного меню
time_button = KeyboardButton(f"{emoji.ALARM_CLOCK} Время")
help_button = KeyboardButton(f"{emoji.WHITE_QUESTION_MARK} Помощь")
settings_button = KeyboardButton(f"{emoji.GEAR} Настройки")
weather_button = KeyboardButton(f"{emoji.SUN_BEHIND_CLOUD} Погода")

# Кнопки настроек
change_city_button = KeyboardButton(f"{emoji.CITYSCAPE} Изменить город")
