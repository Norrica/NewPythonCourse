import pygame as pg

pg.init()

W, H = 800, 600

display = pg.display.set_mode((W, H))

def main():
    while True:
        #1
        events = pg.event.get()
        for e in events:
            if e.type == pg.QUIT:
                return
        #2
        #3
        display.fill('white')
        pg.display.update()


if __name__ == '__main__':
    main()
