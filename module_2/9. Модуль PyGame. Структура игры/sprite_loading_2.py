import pygame as pg

pg.init()

W, H = 800, 600

display = pg.display.set_mode((W, H))

target = pg.image.load('res/target_small.png')
target_hitbox = target.get_rect()
crosshair = pg.image.load('res/crosshair_small.png')
crosshair_hitbox = crosshair.get_rect()


def main():
    while True:
        events = pg.event.get()
        for e in events:
            if e.type == pg.constants.QUIT:
                return

        crosshair_hitbox.center = pg.mouse.get_pos()
        # display.fill('white')
        display.blit(target, target_hitbox)
        display.blit(crosshair, crosshair_hitbox)
        pg.display.update()


if __name__ == '__main__':
    main()
