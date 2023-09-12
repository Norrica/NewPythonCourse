import pygame as pg

pg.init()

W, H = 800, 600

display = pg.display.set_mode((W, H))

target = pg.image.load('res/target_small.png')
target_hitbox = target.get_rect()


# Сделать самому загрузку crosshair.png

def main():
    while True:
        # 1) Считывание ввода
        events = pg.event.get()
        for e in events:
            if e.type == pg.constants.QUIT:
                return
        # -----------------
        # 2) Обновление состояния игры
        # -----------------
        # 3) Отрисовка обновленного состояния
        display.blit(target, target_hitbox)
        pg.display.update()
        # -----------------



if __name__ == '__main__':
    main()
