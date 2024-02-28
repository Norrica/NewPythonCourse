import logging
import os
import time
import traceback
from threading import Thread

import pygame

import http_client
from models import State, GameStatus

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
WHITE = (255, 255, 255)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = (19, 128, 117)  # Черный
BUTTON_TEXT_COLOR = (255, 255, 255)  # Белый
BUTTON_FONT_SIZE = 24


import sys
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    PWD = os.path.abspath(os.path.dirname(sys.executable))
else:
    PWD = os.path.abspath(os.path.dirname(__file__))


user_file_exists = os.path.isfile(os.path.join(PWD, ".user"))
if not user_file_exists:
    logging.error("Файл .user не найден. Создаю новый.")
    user_file = open(os.path.join(PWD, ".user"), "w")
    user_id = input("Введи идентификатор пользователя: ")
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

pygame.display.set_caption("Крестики-нолики")


class Game:
    def __init__(self):
        self.http_client = http_client.HttpClient()

        self.user = None

        self.board = [[None] * BOARD_ROWS for _ in range(BOARD_COLS)]
        self.player = None
        self.enemy = None
        self.game = None
        self.game_users = []
        self.moves = []
        self.current_state = State.MENU
        self.can_make_move = False
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.rating = None

    def prepare(self):
        user = self.http_client.get_user(user_id)
        if user is None:
            logging.error("Пользователь с таким идентификатором не найден. Проверьте файл .user")
            sys.exit(1)
        self.user = user

        already_running_game = self.http_client.get_active_game_by_user_id(user.user_id)
        if already_running_game is not None:
            game, game_users, moves = already_running_game
            self.update_game_info(game, game_users, moves, State.GAME_RUNNING)

    def update_game_info(self, game: http_client.Game, game_users: list[http_client.GameUser], moves: list[http_client.Move], current_state: State):
        self.game = game
        self.moves = moves
        self.refill_board(moves)
        self.player = [user for user in game_users if user.user_id == self.user.user_id][0] if len(game_users) == 2 else None
        self.enemy = [user for user in game_users if user.user_id != self.user.user_id][0] if len(game_users) == 2 else None
        self.game_users = game_users
        self.current_state = current_state

    def draw_menu_buttons(self, play_button_rect, rating_button_rect):
        pygame.draw.rect(self.screen, BUTTON_COLOR, play_button_rect, border_radius=20)
        font = pygame.font.SysFont("Arial", BUTTON_FONT_SIZE, True)
        play_text = font.render('Играть', True, BUTTON_TEXT_COLOR)
        play_text_rect = play_text.get_rect(center=play_button_rect.center)
        self.screen.blit(play_text, play_text_rect)

        pygame.draw.rect(self.screen, BUTTON_COLOR, rating_button_rect, border_radius=20)
        rating_text = font.render('Рейтинг', True, BUTTON_TEXT_COLOR)
        rating_text_rect = rating_text.get_rect(center=rating_button_rect.center)
        self.screen.blit(rating_text, rating_text_rect)

    # Отрисовка линий
    def draw_lines(self):
        # Горизонтальные линии
        pygame.draw.line(self.screen, LINE_COLOR, (50, 150), (350, 150), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (50, 250), (350, 250), LINE_WIDTH)

        # Вертикальные линии
        pygame.draw.line(self.screen, LINE_COLOR, (150, 50), (150, 350), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (250, 50), (250, 350), LINE_WIDTH)

    # Отрисовка фигур
    def draw_figures(self):
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
    def draw_nicknames(self, game_users):
        font = pygame.font.SysFont("Arial", 22, True)
        user1, user2 = game_users
        if user1.sign == '0':
            user1, user2 = user2, user1

        text = font.render(f"X {user1.username}  VS  {user2.username} O", True, WHITE)
        self.screen.blit(text, text.get_rect(center=(WIDTH // 2, 450)))
        if self.can_make_move:
            text = font.render("Твой ход!", True, WHITE)
            self.screen.blit(text, text.get_rect(center=(WIDTH // 2, 400)))

    def check_button_events(self, play_button_rect, rating_button_rect):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if play_button_rect.collidepoint(mouse_pos) and mouse_click[0]:
            self.current_state = State.GAME_WAITING

        if rating_button_rect.collidepoint(mouse_pos) and mouse_click[0]:
            self.current_state = State.RATING

    def check_can_make_move(self):
        can_make_move = True

        sign = self.player.sign
        count_x = sum([1 for row in self.board for cell in row if cell == 'X'])
        count_0 = sum([1 for row in self.board for cell in row if cell == '0'])
        if sign == 'X' and count_x > count_0:
            can_make_move = False
        if sign == '0' and count_0 >= count_x:
            can_make_move = False

        return can_make_move

    def check_game_events(self, events: list[pygame.event.Event]):
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

    def check_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                if self.game is not None and self.user is not None and self.current_state != State.GAME_FINISHED:
                    self.http_client.leave_game(self.user.user_id, self.game.game_id)
                pygame.quit()
                sys.exit(0)

        if self.current_state == State.MENU:
            self.check_button_events(play_button_rect, rating_button_rect)

        if self.current_state == State.GAME_RUNNING:
            self.check_game_events(events)

        if self.current_state in [State.GAME_FINISHED, State.RATING]:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.reset_game()
                        self.rating = None

    def draw_rating(self):
        font = pygame.font.SysFont("Arial", 24, True)
        text = font.render("Рейтинг", True, WHITE)
        self.screen.blit(text, (50, 50))

        if self.rating is None:
            text = font.render("Загрузка...", True, WHITE)
            self.screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            return

        found_in_first_five = False

        for i, rating_user in enumerate(self.rating[:5]):
            if rating_user.username == self.user.username:
                found_in_first_five = True
            text = font.render(f"{i + 1} — {rating_user.username} — {rating_user.wins}pts.", True, WHITE)
            self.screen.blit(text, (50, 100 + 50 * i))

        self.screen.blit(font.render(". . .", True, WHITE), (50, 100 + 50 * (i + 1)))

        if found_in_first_five:
            return

        user_in_rating = next((rating_user for rating_user in self.rating if rating_user.username == self.user.username), None)
        if user_in_rating is None:
            text = font.render(f"{self.user.username} — 0pts.", True, WHITE)
            self.screen.blit(text, (50, 150 + 50 * (i + 1)))
        else:
            text = font.render(f"{self.user.username} — {user_in_rating.wins}pts.", True, WHITE)
            self.screen.blit(text, (50, 150 + 50 * (i + 1)))

    def reset_game(self):
        self.game = None
        self.game_users = []
        self.moves = []
        self.board = [[None] * BOARD_ROWS for _ in range(BOARD_COLS)]
        self.can_make_move = False
        self.player = None
        self.enemy = None
        self.current_state = State.MENU

    def refill_board(self, moves):
        new_board = [[None] * BOARD_ROWS for _ in range(BOARD_COLS)]

        if moves is not None:
            for move in moves:
                new_board[move.row][move.col] = move.sign

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if new_board[row][col] is None and self.board[row][col] is not None and self.player is not None and self.player.sign == self.board[row][col]:
                    new_board[row][col] = self.board[row][col]

        self.board = new_board

    def threaded_info_getter(self):
        while True:
            try:
                time.sleep(0.5)

                if self.current_state == State.GAME_WAITING:
                    game, game_users, moves = None, [], []
                    if self.game is None:
                        response = self.http_client.join_game(self.user.user_id)
                        if response is None:
                            continue
                        game, game_users = response
                    else:
                        game_info = self.http_client.get_game_info(self.game.game_id)
                        if game_info is None:
                            continue
                        game, game_users, moves = game_info

                    if game is not None:
                        state = State.GAME_RUNNING if len(game_users) == 2 else State.GAME_WAITING
                        self.update_game_info(game, game_users, moves, state)
                        continue

                if self.current_state == State.GAME_RUNNING:
                    game_info = self.http_client.get_game_info(self.game.game_id)
                    if game_info is None:
                        continue
                    game, game_users, moves = game_info
                    print(game.status)
                    state = State.GAME_RUNNING if game.status == GameStatus.ACTIVE.value else State.GAME_FINISHED
                    self.update_game_info(game, game_users, moves, state)

                if self.current_state == State.RATING and self.rating is None:
                    rating = self.http_client.get_rating()
                    if rating is not None:
                        self.rating = rating

            except Exception as e:
                logging.error(f"Ошибка при получении информации: {traceback.format_exc()}")

    def run(self):
        info_thread = Thread(target=self.threaded_info_getter)
        info_thread.daemon = True
        info_thread.start()

        prepare_thread = Thread(target=self.prepare)
        prepare_thread.daemon = True
        prepare_thread.start()

        while True:
            self.clock.tick(60)

            self.screen.fill(BG_COLOR)

            if self.user is None:
                font = pygame.font.SysFont("Arial", 24, True)
                text = font.render("Загрузка...", True, WHITE)
                self.screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
                pygame.display.flip()
                continue
            else:
                caption = f"Крестики-нолики ({self.user.username})"
                if pygame.display.get_caption() != caption:
                    pygame.display.set_caption(caption)

            self.check_events()

            if self.current_state == State.MENU:
                self.draw_menu_buttons(play_button_rect, rating_button_rect)

            elif self.current_state == State.GAME_WAITING:
                text = "Ожидание второго игрока..."
                if self.game is None:
                    text = "Поиск игры..."

                font = pygame.font.SysFont("Arial", 24, True)
                text = font.render(text, True, WHITE)
                self.screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

            elif self.current_state == State.GAME_RUNNING:
                if self.game is None:
                    continue

                if self.game.status == GameStatus.FINISHED.value:
                    self.current_state = State.GAME_FINISHED
                    self.refill_board(self.moves)
                    continue

                self.can_make_move = self.check_can_make_move()

                self.draw_nicknames(self.game_users)
                self.draw_lines()
                self.draw_figures()

            elif self.current_state == State.GAME_FINISHED:
                winner = None
                if self.game.winner_id is not None:
                    winner = self.user if self.game.winner_id == self.user.user_id else self.enemy
                font = pygame.font.SysFont("Arial", 24, True)
                if winner is None:
                    text = font.render("Ничья!", True, WHITE)
                else:
                    text = font.render(f"Победитель — {winner.username}!", True, WHITE)

                self.screen.blit(text, text.get_rect(center=(WIDTH // 2, 450)))
                self.draw_lines()
                self.draw_figures()

            elif self.current_state == State.RATING:
                self.draw_rating()

            pygame.display.flip()


game = Game()
game.run()
