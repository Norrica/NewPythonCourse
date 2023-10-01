import pygame as pg
import random

pg.init()

# Определение констант
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


class Bird(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([BIRD_WIDTH, BIRD_HEIGHT])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(
            center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        )
        self.gravity = 1
        self.lift = -10
        self.velocity = 0

    def update(self):
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
        if type == self.TOP:
            self.image = pg.Surface([PIPE_WIDTH, gap_start])
            self.rect = self.image.get_rect(topleft=(SCREEN_WIDTH, 0))
        elif type == self.BOTTOM:
            height = SCREEN_HEIGHT - gap_start - PIPE_GAP
            self.image = pg.Surface([PIPE_WIDTH, height])
            self.rect = self.image.get_rect(topleft=(SCREEN_WIDTH, gap_start + PIPE_GAP))
        self.image.fill(GREEN)

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


make_pipes()

clock = pg.time.Clock()


def main():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    bird.jump()
                global SPEED
                if event.key == pg.K_RIGHT:
                    SPEED +=10
                if event.key == pg.K_LEFT:
                    SPEED -=10

        pipes.update()
        if pipes.sprites()[-1].rect.x <= SCREEN_WIDTH / 2:
            make_pipes()

        bird.update()

        # collisions = pg.sprite.spritecollide(bird, pipes, False)
        # if collisions:
        #     return

        screen.fill(WHITE)
        screen.blit(bird.image, bird.rect)
        pipes.draw(screen)
        pg.display.update()
        clock.tick(30)


if __name__ == '__main__':
    main()
