import logging
from enum import Enum

import pygame

import http_client

import os

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 400, 500
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
CIRCLE_RADIUS = 40
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55
# RGB: Цвета
RED = (255, 0, 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_COLOR = (0, 0, 0)  # Черный
BUTTON_TEXT_COLOR = (255, 255, 255)  # Белый
BUTTON_FONT_SIZE = 22


import sys
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    PWD = os.path.abspath(os.path.dirname(sys.executable))
else:
    PWD = os.path.abspath(os.path.dirname(__file__))

class State(Enum):
    MENU = 0
    RATING = 1
    GAME_WAITING = 2
    GAME_RUNNING = 3
    GAME_FINISHED = 4
    SERVER_PENDING = 5


user_file_exists = os.path.isfile(os.path.join(PWD, ".user"))
if not user_file_exists:
    logging.error("Файл .user не найден. Создаю новый.")
    user_file = open(os.path.join(PWD, ".user"), "w")
    user_id = input("Введите идентификатор пользователя: ")
    user_file.write(user_id)
    user_file.close()


with open(os.path.join(PWD, ".user"), "r") as user_file:
    user_id = user_file.read()
    if user_id == "":
        logging.error("Идентификатор пользователя не найден. Положи его в файл .user")
        sys.exit(1)

# Создаем кнопку "Играть"
play_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2, BUTTON_WIDTH,
                               BUTTON_HEIGHT)
# Создаем кнопку "Рейтинг"
rating_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + BUTTON_HEIGHT, BUTTON_WIDTH,
                                 BUTTON_HEIGHT)


class Game:
    def __init__(self):
        self.http_client = http_client.HttpClient()

        self.user = None

        self.board = [[None] * BOARD_ROWS for _ in range(BOARD_COLS)]
        self.player = None
        self.enemy = None
        self.game = None
        self.current_state = State.MENU
        self.can_make_move = False
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.rating = None

    def __prepare(self):
        pygame.display.set_caption("Крестики-нолики")

        user = self.http_client.get_user(user_id)
        if user is None:
            logging.error("Пользователь с таким идентификатором не найден. Проверьте файл .user")
            sys.exit(1)
        self.user = user

        already_running_game = self.http_client.get_active_game_by_user_id(user.user_id)
        if already_running_game is not None:
            game, game_users, moves = already_running_game
            self.__update_game_info(game, game_users, moves, State.GAME_RUNNING)

    def __update_game_info(self, game: http_client.Game, game_users: list[http_client.GameUser], moves: list[http_client.Move], current_state: State):
        self.game = game
        self.moves = moves
        self.__refill_board(moves)
        self.player = game_users[0] if game_users[0].user_id == self.user.user_id else game_users[1]
        self.enemy = [user for user in game_users if user.user_id != self.user.user_id][0] if len(game_users) == 2 else None
        self.current_state = current_state

    def __draw_menu_buttons(self, play_button_rect, rating_button_rect):
        pygame.draw.rect(self.screen, BUTTON_COLOR, play_button_rect)

        # Текст кнопки "Играть"
        font = pygame.font.Font(None, BUTTON_FONT_SIZE)
        play_text = font.render('Играть', True, BUTTON_TEXT_COLOR)
        play_text_rect = play_text.get_rect(center=play_button_rect.center)
        self.screen.blit(play_text, play_text_rect)

        pygame.draw.rect(self.screen, BUTTON_COLOR, rating_button_rect)

        # Текст кнопки "Рейтинг"
        rating_text = font.render('Рейтинг', True, BUTTON_TEXT_COLOR)
        rating_text_rect = rating_text.get_rect(center=rating_button_rect.center)
        self.screen.blit(rating_text, rating_text_rect)

    # Отрисовка линий
    def __draw_lines(self):
        # Горизонтальные линии
        pygame.draw.line(self.screen, LINE_COLOR, (50, 150), (350, 150), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (50, 250), (350, 250), LINE_WIDTH)

        # Вертикальные линии
        pygame.draw.line(self.screen, LINE_COLOR, (150, 50), (150, 350), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (250, 50), (250, 350), LINE_WIDTH)

    # Отрисовка фигур
    def __draw_figures(self):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.board[row][col] == 'X':
                    # Рассчитываем центр клетки
                    center_x = col * 100 + 50 + 50
                    center_y = row * 100 + 50 + 50

                    # Рассчитываем диагонали крестика
                    # Диагональ слева-наверху на право-внизу
                    pygame.draw.line(self.screen, CROSS_COLOR,
                                     (center_x - SPACE + 25, center_y - SPACE + 25),
                                     (center_x + SPACE - 25, center_y + SPACE - 25),
                                     CROSS_WIDTH)
                    # Диагональ справа-наверху на лево-внизу
                    pygame.draw.line(self.screen, CROSS_COLOR,
                                     (center_x + SPACE - 25, center_y - SPACE + 25),
                                     (center_x - SPACE + 25, center_y + SPACE - 25),
                                     CROSS_WIDTH)
                elif self.board[row][col] == '0':
                    # Отрисовка нолика
                    center = (int(col * 100 + 100), int(row * 100 + 100))
                    pygame.draw.circle(self.screen, CIRCLE_COLOR, center, CIRCLE_RADIUS, CIRCLE_WIDTH)

    # Отображение никнеймов
    def __draw_nicknames(self, game_users):
        font = pygame.font.Font(None, 36)
        game_user_1, game_user_2 = game_users
        if game_user_1.sign == '0':
            game_users[0], game_users[1] = game_users[1], game_users[0]

        text1 = font.render(game_users[0].username, True, RED)
        text2 = font.render(game_users[1].username, True, RED)
        self.screen.blit(text1, (50, 450))
        self.screen.blit(text2, (300, 450))

    def __check_button_events(self, play_button_rect, rating_button_rect):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if play_button_rect.collidepoint(mouse_pos) and mouse_click[0]:
            self.current_state = State.GAME_WAITING

        if rating_button_rect.collidepoint(mouse_pos) and mouse_click[0]:
            self.rating = self.http_client.get_rating()
            self.current_state = State.RATING

    def __check_game_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.can_make_move:
                mouse_x = event.pos[0] - 50
                mouse_y = event.pos[1] - 50

                if mouse_x >= 0 and mouse_y >= 0:
                    row = int(mouse_y // 100)
                    col = int(mouse_x // 100)

                    if row < BOARD_ROWS and col < BOARD_COLS and self.board[row][col] is None:
                        self.can_make_move = False
                        self.board[row][col] = self.player.sign
                        self.http_client.make_move(self.user.user_id, self.game.game_id, row, col, self.player.sign)

    def __check_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if self.current_state == State.MENU:
            self.__check_button_events(play_button_rect, rating_button_rect)

        if self.current_state == State.GAME_RUNNING:
            self.__check_game_events(events)

        if self.current_state in [State.GAME_FINISHED, State.RATING]:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__reset_game()

    def __draw_rating(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Рейтинг", True, RED)
        self.screen.blit(text, (50, 50))

        if self.rating is None:
            return

        for i, rating_user in enumerate(self.rating):
            text = font.render(f"{i + 1}. {rating_user.username} - {rating_user.wins}", True, RED)
            self.screen.blit(text, (50, 100 + 50 * i))

    def __reset_game(self):
        self.game = None
        self.board = [[None] * BOARD_ROWS for _ in range(BOARD_COLS)]
        self.can_make_move = False
        self.player = None
        self.enemy = None
        self.current_state = State.MENU

    def __refill_board(self, moves):
        new_board = [[None] * BOARD_ROWS for _ in range(BOARD_COLS)]
        for move in moves:
            new_board[move.row][move.col] = move.sign

        self.board = new_board

    def __check_winner(self, board):
        # Проверка горизонтальных и вертикальных комбинаций
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
                return board[i][0]  # Горизонтальная победа
            if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
                return board[0][i]  # Вертикальная победа

        # Проверка диагональных комбинаций
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
            return board[0][0]  # Главная диагональ
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
            return board[0][2]  # Побочная диагональ

        # Если ни один из игроков не выиграл
        return None

    def __threaded_info_getter(self):
        while True:
            pass


    def run(self):
        self.__prepare()

        while True:
            self.clock.tick(5)

            self.screen.fill(BG_COLOR)

            if self.current_state == State.MENU:
                self.__draw_menu_buttons(play_button_rect, rating_button_rect)

            elif self.current_state == State.GAME_WAITING:
                if self.game is None:
                    response = self.http_client.join_game(self.user.user_id)
                    if response is None:
                        continue
                    self.game, game_users = response
                else:
                    response = self.http_client.get_game_info(self.game.game_id)
                    if response is None:
                        continue
                    self.game, game_users, _ = response

                self.player = game_users[0] if game_users[0].user_id == self.user.user_id else game_users[1]
                self.enemy = [user for user in game_users if user.user_id != self.user.user_id][0] if len(game_users) == 2 else None
                if len(game_users) == 2:
                    self.current_state = State.GAME_RUNNING
                    continue

                font = pygame.font.Font(None, 36)
                text = font.render("Ожидание второго игрока...", True, RED)
                self.screen.blit(text, (50, 450))

            elif self.current_state == State.GAME_RUNNING:
                self.__draw_lines()
                self.__draw_figures()

                game_info = self.http_client.get_game_info(self.game.game_id)
                if game_info is None:
                    continue

                self.game, game_users, moves = game_info
                if self.game.status == http_client.GameStatus.FINISHED.value:
                    self.current_state = State.GAME_FINISHED
                    self.game = None
                    self.__refill_board(moves)
                    continue

                self.__refill_board(moves)
                self.__draw_nicknames(game_users)

                if len(moves) != 0 and moves[-1].user_id != self.player.user_id:
                    self.can_make_move = True
                elif len(moves) == 0:
                    x_sign_user = game_users[0] if game_users[0].sign == 'X' else game_users[1]
                    if x_sign_user.user_id == self.player.user_id:
                        self.can_make_move = True

                self.__draw_figures()

            elif self.current_state == State.GAME_FINISHED:
                winner_sign = self.__check_winner(self.board)
                winner = self.player if winner_sign == self.player.sign else self.enemy
                font = pygame.font.Font(None, 36)
                if winner_sign is None:
                    text = font.render("Ничья", True, RED)
                else:
                    text = font.render(f"Победил {winner.username}", True, RED)

                self.screen.blit(text, (50, 450))
                self.__draw_lines()
                self.__draw_figures()

            elif self.current_state == State.RATING:
                self.__draw_rating()

            self.__check_events()
            pygame.display.update()


game = Game()
game.run()
