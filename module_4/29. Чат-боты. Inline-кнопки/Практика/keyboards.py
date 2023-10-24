from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup

import buttons

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [buttons.time_button, buttons.weather_button, buttons.cats_button],
        [buttons.help_button, buttons.settings_button],
    ],
    resize_keyboard=True,
)

settings_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [buttons.change_city_button, buttons.back_button],
    ],
    resize_keyboard=True,
)

weather_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons.weather_current_inline_button],
        [buttons.weather_forecast_inline_button],
    ],
)

cats_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons.cats_random_inline_button],
    ],
)
