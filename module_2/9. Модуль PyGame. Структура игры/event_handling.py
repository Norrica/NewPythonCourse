import pygame as pg

pg.init()

W, H = 800, 600

display = pg.display.set_mode((W, H))


def main():
    while True:
        events = pg.event.get()
        for e in events:
            if e.type == pg.constants.QUIT:
                return
        pg.display.update()


if __name__ == '__main__':
    main()
