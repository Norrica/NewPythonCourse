import pygame as pg
import random

W, H = 800, 600
FPS = 60

pg.init()
SCREEN = pg.display.set_mode([W, H])
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
        SCREEN.fill('black')
        text = font_xl.render(message, 1, 'white')
        SCREEN.blit(text, text.get_rect(
          center=(W // 2, H // 2)))
        self.sprites.draw(SCREEN)


class Level1(Scene):
    def __init__(self):
        self.sprites = pg.sprite.Group()
        for _ in range(5):
            sprite = BasicSprite('red', random.randint(0, W - 50), random.randint(0, H - 50), 50, 50)
            self.sprites.add(sprite)
    def process_input(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_SPACE:
                    return Level2()
        return self
    def render(self):
        super().render("Level1")



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