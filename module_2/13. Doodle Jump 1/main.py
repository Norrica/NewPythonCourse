import pygame as pg
import random

PLATFORM_WIDTH = 105

pg.init()

W, H = 480, 800
GRAVITY = 1
JUMP = -30
display = pg.display.set_mode((W, H))

MIN_GAP = 90
MAX_GAP = 180
score = 0
font = pg.font.Font(None, 36)  # Шрифт для отображения очков


def draw_text(text: str, pos: (int, int)):
    score_text = font.render(text, True, (0, 0, 0))
    display.blit(score_text, pos)


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_left = pg.image.load('img/doodle_left.png')
        self.image = self.image_left
        self.image_right = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=(W // 2, H // 2))
        self.speed = 0
        self.is_using_jetpack = False
        self.jetpack_counter = 0

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.rect.x -= 5
            self.image = self.image_left
        if keys[pg.K_RIGHT]:
            self.rect.x += 5
            self.image = self.image_right

        if self.rect.right > W:
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.right = W

        if self.is_using_jetpack and self.jetpack_counter > 0:
            self.speed = -5
            self.jetpack_counter -= 5
        else:
            self.is_using_jetpack = False
            self.speed += GRAVITY

        self.rect.y += self.speed

    def draw(self):
        if self.rect.y > H:
            # self.rect.y = H // 2
            draw_text('Game Over', (W // 2 - 30, H // 2 - 10))
            # self.kill()
        else:
            display.blit(self.image, self.rect)


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, sprite):
        super().__init__()
        # self.image = pg.Surface([PLATFORM_WIDTH, 31])
        # self.image.fill('black')
        self.image = pg.image.load(sprite)
        self.rect = self.image.get_rect(topleft=(x, y))

    def collide_with(self, player):
        player.speed = JUMP

    def is_on_screen(self):
        return self.rect.bottom > 0

    def update(self):
        pass


class NormalPlatform(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, 'img/green.png')


class SpringPlatform(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, 'img/purple.png')

    def collide_with(self, player):
        player.speed = 1.5 * JUMP


class BreakablePlatform(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, 'img/red.png')

    def collide_with(self, player):
        player.speed = JUMP
        # self.animate_break()
        self.kill()


class MovingPlatform(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, 'img/blue.png')
        self.direction = random.choice([-1, 1])  # 1 for right, -1 for left
        self.speed = 3

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right > W or self.rect.left < 0:
            self.direction *= -1


def spawn_platform():
    try:
        platform = platforms.sprites()[-1]
    except:
        y = H - 50
        platform = NormalPlatform(W // 2 - PLATFORM_WIDTH // 2, y)
        platforms.add(platform)
    y = platform.rect.y - random.randint(MIN_GAP, MAX_GAP)
    x = random.randint(0, W - PLATFORM_WIDTH)
    types = [MovingPlatform, BreakablePlatform, SpringPlatform, NormalPlatform]
    Plat = random.choice(types)
    platform = Plat(x, y)
    platforms.add(platform)


def is_top_collision(player: Player, platform: Platform):
    if player.rect.colliderect(platform.rect) and player.speed > 0 and platform.is_on_screen():
        if player.rect.bottom < platform.rect.bottom:
            platform.collide_with(player)
            return True


player = Player()
platforms = pg.sprite.Group()

spawn_platform()


def main():
    global player
    while True:
        events = pg.event.get()
        for e in events:
            if e.type == pg.QUIT:
                return

        player.update()
        platforms.update()
        hits = pg.sprite.spritecollide(player, platforms, False, collided=is_top_collision)
        # if hits:
        #     hits[0].collide_with(player)

        if player.speed < 0 and player.rect.bottom < H / 2:  # Only move platforms up if player is moving up
            player.rect.y -= player.speed
            global score
            score += 1
            for platform in platforms:
                platform.rect.y -= player.speed

        # Remove off-screen platforms and spawn new ones
        off_screen_platforms = [p for p in platforms if p.rect.y > H]
        for p in off_screen_platforms:
            p.kill()
            spawn_platform()
        if len(platforms) < 25:
            spawn_platform()

        display.fill('white')
        player.draw()
        platforms.draw(display)
        draw_text(f'Score:{score}', (10, 10))
        pg.display.update()
        pg.time.delay(1000 // 60)


if __name__ == '__main__':
    main()
