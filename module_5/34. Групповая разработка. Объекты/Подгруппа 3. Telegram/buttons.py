from pyrogram.types import KeyboardButton
from pyrogram import emoji

# Общие кнопки
back_button = KeyboardButton(f"{emoji.BACK_ARROW} Назад")

# Кнопки главного меню
profile_button = KeyboardButton(f"{emoji.PERSON} Профиль")
rating_button = KeyboardButton(f"{emoji.CROWN} Рейтинг")
settings_button = KeyboardButton(f"{emoji.GEAR} Настройки")

# Кнопки настроек
sign_up_button = KeyboardButton(f"{emoji.PEN} Регистрация")
