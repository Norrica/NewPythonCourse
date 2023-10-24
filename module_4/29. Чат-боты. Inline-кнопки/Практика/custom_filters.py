from pyrogram import filters
from pyrogram.types import Message, KeyboardButton, InlineKeyboardButton, CallbackQuery


def button_filter(button: KeyboardButton):
    async def func(_, __, message: Message):
        return message.text == button.text

    return filters.create(func, "ButtonFilter", button=button)


def inline_button_filter(inline_button: InlineKeyboardButton):
    async def func(_, __, query: CallbackQuery):
        return query.data == inline_button.callback_data

    return filters.create(func, "InlineButtonFilter", inline_button=inline_button)
