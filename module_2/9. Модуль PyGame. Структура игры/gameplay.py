import random

import pygame as pg

pg.init()

W, H = 800, 600

display = pg.display.set_mode((W, H))

target = pg.image.load('res/target_small.png')
target_hitbox = target.get_rect()
crosshair = pg.image.load('res/crosshair_small.png')
crosshair_hitbox = crosshair.get_rect()
crosshair_hitbox.center = W / 2, H / 2


def main():
    flag = True
    while True:
        events = pg.event.get()
        for e in events:
            if e.type == pg.constants.QUIT:
                return

        crosshair_hitbox.center = pg.mouse.get_pos()

        is_LMB_pressed = pg.mouse.get_pressed(3)[0]

        if is_LMB_pressed and flag:
            if target_hitbox.collidepoint(crosshair_hitbox.center):
                target_hitbox.x = random.randint(0, W - target_hitbox.width)
                target_hitbox.y = random.randint(0, H - target_hitbox.height)
                flag = False
        elif not is_LMB_pressed:
            flag = True

        display.fill('white')
        display.blit(target, target_hitbox)
        display.blit(crosshair, crosshair_hitbox)
        pg.display.update()


if __name__ == '__main__':
    main()
