import pygame as pg
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

pg.init()
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pg.display.set_caption("Имя игры")

font_xl = pg.font.Font(None, 96)


class BasicSprite(pg.sprite.Sprite):
    def __init__(self, color, x, y, width, height):
        super().__init__()
        self.image = pg.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))


class Scene():
    sprites = pg.sprite.Group()

    def process_input(self, events):
        pass

    def update(self):
        self.sprites.update()

    def render(self, message):
        screen.fill('black')
        text = font_xl.render(message, 1, 'white')
        screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        self.sprites.draw(screen)


class Level1(Scene):
    def __init__(self):
        self.sprites = pg.sprite.Group()
        for _ in range(5):
            sprite = BasicSprite('red', random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50), 50,
                                 50)
            self.sprites.add(sprite)

    def process_input(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_SPACE:
                    return Level2()
        return self

    def render(self):
        super().render("Level1")


class Level2(Scene):
    def __init__(self):
        self.sprites = pg.sprite.Group()
        for _ in range(10):
            sprite = BasicSprite('blue', random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50),
                                 50, 50)
            self.sprites.add(sprite)

    def process_input(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_SPACE:
                    return Level3()
        return self

    def render(self):
        super().render("Level2")


class Level3(Scene):
    def __init__(self):
        self.sprites = pg.sprite.Group()
        for _ in range(15):
            sprite = BasicSprite('green', random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50),
                                 50, 50)
            self.sprites.add(sprite)

    def process_input(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_SPACE:
                    return Level1()
        return self

    def render(self):
        super().render("Level3")


def main():
    current_scene = Level1()
    while current_scene:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                return

        next_scene = current_scene.process_input(events)
        if next_scene:
            current_scene = next_scene
        current_scene.update()
        current_scene.render()
        pg.display.update()
        pg.time.delay(1000 // FPS)


if __name__ == "__main__":
    main()
    pg.quit()
