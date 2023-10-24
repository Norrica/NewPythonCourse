import random

import pygame as pg

pg.init()

W, H = 480, 800
display = pg.display.set_mode((W, H))

GRAVITY = 1
JUMP = -30
PLATFORM_WIDTH = 105
MIN_GAP = 90
MAX_GAP = 180
score = 0
font_name = pg.font.match_font('Comic Sans', True, False)
font = pg.font.Font(font_name, 36)


def draw_text(text: str, x: int, y: int):
    score_text = font.render(text, True, (0, 0, 0))
    display.blit(score_text, (x, y))


class Sprite(pg.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pg.image.load(image_path)
        self.rect = self.image.get_rect(center=(x, y))
        self.dead = False

    def update(self):
        super().update()

    def draw(self):
        display.blit(self.image, self.rect)

    def collide_with_border(self):
        return self.rect.left < 0 or self.rect.right > W or self.rect.top < 0 or self.rect.bottom > H

    def kill(self):
        self.dead = True
        super().kill()


class Player(Sprite):
    def __init__(self):
        super().__init__(W // 2, H // 2, '../img/doodle_left.png')
        self.image_left = self.image
        self.image_right = pg.transform.flip(self.image, True, False)
        self.speed = 0

    def update(self):
        if self.dead:
            return
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.rect.x -= 5
            self.image = self.image_left
        if keys[pg.K_RIGHT]:
            self.rect.x += 5
            self.image = self.image_right

        if self.rect.left > W:
            self.rect.left = 0
        if self.rect.right < 0:
            self.rect.right = W

        self.speed += GRAVITY
        self.rect.y += self.speed
        if self.rect.y > H:
            self.kill()

    def draw(self):
        if self.dead:
            # self.rect.y = H // 2
            draw_text('Game Over', W // 2 - 70, H // 2 - 10)
        else:
            display.blit(self.image, self.rect)


class BaseBonus(Sprite):
    def __init__(self, image_path, plat: 'BasePlatform'):
        img = pg.image.load(image_path)
        w = img.get_width()
        h = img.get_height()
        rect = plat.rect
        x = random.randint(rect.left + w // 2, rect.right - w // 2)
        y = rect.top - h // 2
        super().__init__(x, y, image_path)
        self.platform = plat
        self.dx = self.rect.x - self.platform.rect.x

    def on_collision(self, player):
        global score
        score += 1000
        self.kill()

    def update(self):
        self.rect.x = self.platform.rect.x + self.dx
        if self.platform.dead:
            self.kill()


class Spring(BaseBonus):
    def __init__(self, plat):
        super().__init__('../img/spring.png', plat)

    def on_collision(self, player):
        player.speed = -50
        self.image = pg.image.load('../img/spring_1.png')


class BasePlatform(Sprite):
    def on_collision(self, player):
        player.speed = JUMP

    def update(self):
        super().update()
        if self.rect.top > H:
            self.kill()
            spawn_platform()

    def attach_bonus(self):
        if random.randint(0, 100) > 0:
            Bonus = random.choice([Spring])
            obj = Bonus(self)
            platforms.add(obj)


class NormalPlatform(BasePlatform):
    def __init__(self, x, y):
        super().__init__(x, y, '../img/green.png')


class SpringPlatform(BasePlatform):
    def __init__(self, x, y):
        super().__init__(x, y, '../img/purple.png')

    def on_collision(self, player):
        player.speed = 1.3 * JUMP


class BreakablePlatform(BasePlatform):
    def __init__(self, x, y):
        super().__init__(x, y, '../img/red.png')

    def on_collision(self, player):
        player.speed = JUMP
        # self.animate_break()
        self.kill()


class MovingPlatform(BasePlatform):
    def __init__(self, x, y):
        super().__init__(x, y, '../img/blue.png')
        self.direction = random.choice([-1, 1])  # 1 for right, -1 for left
        self.speed = 3

    def update(self):
        super().update()
        self.rect.x += self.speed * self.direction
        if self.rect.right > W or self.rect.left < 0:
            self.direction *= -1


platforms = pg.sprite.Group()


def spawn_platform():
    platform = platforms.sprites()[-1]
    y = platform.rect.y - random.randint(MIN_GAP, MAX_GAP)
    x = random.randint(0, W - PLATFORM_WIDTH)
    types = [
        MovingPlatform,
        BreakablePlatform,
        SpringPlatform,
        NormalPlatform
    ]
    Plat = random.choice(types)
    platform = Plat(x, y)
    platform.attach_bonus()
    platforms.add(platform)


class BaseEnemy(Sprite):
    def update(self):
        if self.rect.y > H:
            self.kill()

    def on_collision(self, player):
        player.kill()


class Hole(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, '../img/enemy_hole.png')


class LeftRightEnemy(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, '../img/enemy_l_r.png')
        self.image_right = pg.transform.flip(self.image, True, False)
        self.image_left = self.image
        self.x_speed = random.choice([-5, 5])
        self.y_speed = random.choice([-5, 5])
        self.gravity = GRAVITY
        if self.x_speed > 0:
            self.image = self.image_right

    def update(self):
        self.rect.x += self.x_speed
        if self.x_speed > 0:
            self.image = self.image_right
        if self.x_speed < 0:
            self.image = self.image_left

        if self.collide_with_border():
            self.x_speed *= -1

        self.y_speed += self.gravity
        self.rect.y += self.y_speed
        if self.y_speed < -5:
            self.gravity *= -1
        if self.y_speed > 5:
            self.gravity *= -1


class UpDownEnemy(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, '../img/enemy_u_d.png')  # Хороший пример динамичности питона
        self.image_right = pg.transform.flip(self.image, True, False)
        self.image_left = self.image
        self.x_speed = random.choice([-5, 5])
        self.y_speed = random.choice([-5, 5])
        self.gravity = GRAVITY
        if self.y_speed > 0:
            self.image = self.image_right

    def update(self):  ## ДОП -- написать с использованием класса GravityComponent(self.rect)!!!
        self.rect.y += self.y_speed

        if self.collide_with_border():
            self.y_speed *= -1

        self.x_speed += self.gravity
        self.rect.x += self.x_speed
        if self.x_speed < -10:
            self.gravity *= -1
            self.image = self.image_left
        if self.x_speed > 10:
            self.image = self.image_right
            self.gravity *= -1


doodle = Player()
platform = NormalPlatform(W // 2 - PLATFORM_WIDTH // 2, H - 50)
platforms.add(platform)

enemies = pg.sprite.Group()


def spawn_enemy(delay):
    if delay > 5000:
        delay = 0
        Enemy = random.choice([Hole, LeftRightEnemy, UpDownEnemy])
        x = random.randint(0, W - 80)
        e = Enemy(x, -H)
        enemies.add(e)
    return delay


def is_top_collision(player: Player, platform: BasePlatform):
    if player.rect.colliderect(platform.rect):
        if player.speed > 0:
            if player.rect.bottom < platform.rect.bottom:
                platform.on_collision(player)
                return True


def main():
    passed_time = 0
    while True:
        # 1
        for e in pg.event.get():
            if e.type == pg.QUIT:
                return
        # 2
        doodle.update()
        platforms.update()
        enemies.update()
        pg.sprite.spritecollide(doodle, platforms, False, collided=is_top_collision)
        hit_enemy = pg.sprite.spritecollide(doodle, enemies, False)
        if hit_enemy:
            doodle.kill()
        if len(platforms) < 25:
            spawn_platform()
        if doodle.speed < 0 and doodle.rect.bottom < H / 2:
            doodle.rect.y -= doodle.speed

            global score
            score += 1
            for platform in platforms:
                platform.rect.y -= doodle.speed
            for e in enemies:
                e.rect.y -= doodle.speed
        passed_time = spawn_enemy(passed_time)

        # 3
        display.fill('white')
        enemies.draw(display)
        platforms.draw(display)
        doodle.draw()
        draw_text(f'Score:{score}', 10, 10)
        pg.display.update()
        passed_time += pg.time.delay(1000 // 60)


if __name__ == '__main__':
    main()
