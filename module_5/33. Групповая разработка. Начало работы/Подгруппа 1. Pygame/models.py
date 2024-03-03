from enum import Enum


class State(Enum):
    MENU = 0            # Главное меню
    GAME_WAITING = 1    # Ожидание начала игры
    GAME_RUNNING = 2    # Игра
    GAME_FINISHED = 3   # Игра завершена
