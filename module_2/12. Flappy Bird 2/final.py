import pygame as pg
import pygame_menu
import random

pg.init()
pg.display.set_caption('Flappy Bird')
# Определение констант
FPS = 1000 // 60
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
PIPE_WIDTH = 80
PIPE_GAP = 250
SPEED = 5
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Flappy Bird')
score = 0
font = pg.font.Font(None, 36)  # Шрифт для отображения очков


def draw_score():
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))


def draw_text(text: str, xy: list[int, int]):  # ДЗ 3
    score_text = font.render(text, True, (0, 0, 0))
    screen.blit(score_text, (xy[0], xy[1]))


class Bird(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([BIRD_WIDTH, BIRD_HEIGHT])
        # self.image.fill((255, 255, 0))
        self.image = pg.image.load('bird.png')
        self.image = pg.transform.scale(self.image, size=[BIRD_WIDTH, BIRD_HEIGHT])
        self.sprite_copy = self.image
        self.rect = self.image.get_rect(
            center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        )
        self.gravity = 1
        self.lift = -10
        self.velocity = 0

    def update(self):
        self.image = pg.transform.rotate(
            self.sprite_copy, -self.velocity)
        self.velocity += self.gravity
        self.rect.y += self.velocity
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = self.lift


class Pipe(pg.sprite.Sprite):
    TOP = 1
    BOTTOM = 2

    def __init__(self, type, gap_start):
        super().__init__()
        self.image = pg.image.load('pipe.png')
        self.image = pg.transform.scale(self.image, [PIPE_WIDTH, self.image.get_height() / 2])
        if type == self.TOP:
            self.image = pg.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(bottomleft=(SCREEN_WIDTH, gap_start))
        elif type == self.BOTTOM:
            self.rect = self.image.get_rect(topleft=(SCREEN_WIDTH, gap_start + PIPE_GAP))
        self.passed = False

    def update(self):
        self.rect.x -= SPEED
        if self.rect.right < 0:
            self.kill()


bird = Bird()
pipes = pg.sprite.Group()


def make_pipes():
    gap_start = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
    top_pipe = Pipe(Pipe.TOP, gap_start)
    bottom_pipe = Pipe(Pipe.BOTTOM, gap_start)
    pipes.add(top_pipe, bottom_pipe)


def animate_gameover():  # ДЗ 3
    bird.sprite_copy = pg.transform.flip(bird.sprite_copy, False, True)
    FPS = 15
    bird.gravity = -0.7  # Меняем гравитацию для подпрыгивания вверх
    bird.velocity = 0  # Обнуляем скорость
    for i in range(20):  # Количество кадров анимации подпрыгивания
        bird.update()
        screen.fill(WHITE)
        pipes.update()
        pipes.draw(screen)
        draw_score()
        screen.blit(bird.image, bird.rect)
        pg.display.update()
        pg.time.delay(FPS)
    bird.gravity = 0.7  # Меняем гравитацию для подпрыгивания вниз
    bird.velocity = 0  # Обнуляем скорость
    while bird.rect.y < SCREEN_HEIGHT - BIRD_HEIGHT:
        bird.update()  # Обновляем положение птицы с учетом гравитации
        screen.fill(WHITE)
        pipes.update()
        pipes.draw(screen)
        screen.blit(bird.image, bird.rect)
        draw_score()

        pg.display.update()
        pg.time.delay(FPS)
    bird.sprite_copy = pg.transform.flip(bird.sprite_copy, False, True)


def main():
    # lives = 3  # ДЗ 3
    global score
    global SPEED  # ДЗ  4 и 5
    bird.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
    bird.velocity = 0
    pipes.empty()
    make_pipes()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    bird.jump()
                # global SPEED # Домашнее задание 3
                # if event.key == pg.K_RIGHT:
                #     SPEED +=10
                # if event.key == pg.K_LEFT:
                #     SPEED -=10

        pipes.update()
        if pipes.sprites()[-1].rect.x <= SCREEN_WIDTH / 3:
            make_pipes()

        for p in pipes:
            if p.rect.right < bird.rect.left and not p.passed:
                p.passed = True
                score += 0.5

        bird.update()

        collisions = pg.sprite.spritecollide(bird, pipes, False)
        if collisions:
            # lives -= 1# ДЗ 3. Необходимо добавить атрибут птице, по аналогии с is_passed для труб.
            # if lives <= 0:# ДЗ 3
            animate_gameover()  # ДЗ 1
            show_end_screen()
            return

        screen.fill(WHITE)
        screen.blit(bird.image, bird.rect)
        pipes.draw(screen)
        draw_score()
        # draw_text(f'Lives: {lives}', [10, 30]) # ДЗ 3
        pg.display.update()
        pg.time.delay(FPS)
        SPEED += 0.0001  # ДЗ 5


def show_end_screen():
    end_menu = pygame_menu.Menu('Игра окончена', 300, 400,
                                theme=pygame_menu.themes.THEME_BLUE)
    end_menu.add.label(f'Всего очков: {score}', font_size=30)
    end_menu.add.button('Заново', main)
    end_menu.add.button('Выйти', pygame_menu.events.EXIT)
    end_menu.mainloop(screen)


def show_start_screen():
    menu = pygame_menu.Menu('Flappy Bird', 300, 400, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Начать', main)
    menu.add.button('Выйти', pygame_menu.events.EXIT)
    menu.mainloop(screen)


if __name__ == '__main__':
    show_start_screen()
