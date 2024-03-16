import logging
import os
import sys
import time
from threading import Thread

import pygame

from http_client import HttpClient
from models import State

pygame.init()
pygame.display.set_caption("Крестики-нолики")

WIDTH, HEIGHT = 400, 500
BG_COLOR = (28, 170, 156)

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = (19, 128, 117)
BUTTON_TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 24

LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SPACE = 55
CIRCLE_RADIUS = 40
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

WHITE = (255, 255, 255)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

play_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)

user_file_name = ".user"
user_file_exists = os.path.isfile(user_file_name)
if not user_file_exists:
    logging.error(f"Файл {user_file_name} не найден. Создаю новый.")
    with open(user_file_name, "w") as user_file:
        user_file.write(input("Введи идентификатор пользователя: "))


with open(user_file_name, "r") as user_file:
    user_id = user_file.read()
    if user_id == "":
        logging.error(f"Идентификатор пользователя не найден. Положи его в файл {user_file_name}")
        sys.exit(1)


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.current_state = State.MENU
        self.sign = 'X'
        self.board = [[None] * BOARD_ROWS for _ in range(BOARD_COLS)]
        self.user = None
        self.http_client = HttpClient()

    def prepare(self):
        while self.user is None:
            user = self.http_client.get_user(user_id)
            if user is None:
                logging.error(f"Пользователь с таким идентификатором не найден. Проверьте файл {user_file_name} или подключение к серверу")
                time.sleep(1)
                continue

            self.user = user

    def check_button_events(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if play_button_rect.collidepoint(mouse_pos) and mouse_click[0]:
            self.current_state = State.GAME_RUNNING

    def check_game_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x = event.pos[0] - 50
                mouse_y = event.pos[1] - 50

                if mouse_x >= 0 and mouse_y >= 0:
                    row = int(mouse_y // 100)
                    col = int(mouse_x // 100)

                    if row < BOARD_ROWS and col < BOARD_COLS and self.board[row][col] is None:
                        self.board[row][col] = self.sign
                        self.sign = '0' if self.sign == 'X' else 'X'

    def check_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        if self.current_state == State.GAME_RUNNING:
            self.check_game_events(events)
        if self.current_state == State.MENU:
            self.check_button_events()
        if self.current_state in [State.GAME_RUNNING, State.GAME_FINISHED]:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.current_state = State.MENU

    def draw_menu(self):
        if self.user is None:
            font = pygame.font.SysFont("Arial", FONT_SIZE, True)
            text = font.render("Загрузка...", True, WHITE)
            self.screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            return

        caption = f"Крестики-нолики ({self.user.username})"
        pygame.display.set_caption(caption)

        font = pygame.font.SysFont("Arial", FONT_SIZE, True)
        pygame.draw.rect(self.screen, BUTTON_COLOR, play_button_rect, border_radius=20)
        play_text = font.render('Играть', True, BUTTON_TEXT_COLOR)
        self.screen.blit(play_text, play_text.get_rect(center=play_button_rect.center))

    def draw_lines(self):
        # Горизонтальные линии
        pygame.draw.line(self.screen, LINE_COLOR, (50, 150), (350, 150), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (50, 250), (350, 250), LINE_WIDTH)
        # Вертикальные линии
        pygame.draw.line(self.screen, LINE_COLOR, (150, 50), (150, 350), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (250, 50), (250, 350), LINE_WIDTH)

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

    def draw_game_running(self):
        self.draw_lines()
        self.draw_figures()

    def run(self):
        prepare_thread = Thread(target=self.prepare)
        prepare_thread.daemon = True
        prepare_thread.start()

        while True:
            self.clock.tick(60)
            self.screen.fill(BG_COLOR)

            self.check_events()

            if self.current_state == State.MENU:
                self.draw_menu()

            if self.current_state == State.GAME_RUNNING:
                self.draw_game_running()

            pygame.display.flip()


game = Game()
game.run()
