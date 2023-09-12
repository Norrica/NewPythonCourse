import pygame

pygame.init()

W, H = 800, 600

display = pygame.display.set_mode((W, H))


class Crosshair():
    def __init__(self):
        self.sprite = pygame.image.load('res/crosshair_small.png')
        self.hitbox = self.sprite.get_rect()

    def draw(self):
        display.blit(self.sprite, self.hitbox)

    def move(self):
        self.hitbox.center = pygame.mouse.get_pos()


class Target():
    def __init__(self):
        # \ разделяет строку кода если она  слишком длинная
        self.sprite = \
        pygame.image.load('res/target_small.png')
        self.hitbox = self.sprite.get_rect()


    def draw(self):
        display.blit(self.sprite, self.hitbox)
    def move(self):
        if is_key_pressed(pygame.K_w):
            self.hitbox.y -= 1
        if is_key_pressed(pygame.K_d):
            self.hitbox.x += 1
        if is_key_pressed(pygame.K_s):
            self.hitbox.y += 1
        if is_key_pressed(pygame.K_a):
            self.hitbox.x -= 1


def draw(self):
    display.blit(self.sprite, self.hitbox)


def is_key_pressed(key):
    return pygame.key.get_pressed()[key]


def where_mouse_pressed(mouse_key):
    buttons = pygame.mouse.get_pressed(num_buttons=5)
    if buttons[mouse_key]:
        return pygame.mouse.get_pos()


...
crosshair = Crosshair()
target = Target()

def main():
    while True:
        # 1) Считывание ввода
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                return



        # mouse_pos = where_mouse_pressed(0)
        # if mouse_pos:
        #     hitbox.center = mouse_pos
        # -----------------
        # 2) Обновление состояния игры
        crosshair.move()
        target.move()
        # hitbox.x = 10
        # hitbox.y = 10
        # -----------------
        # 3) Отрисовка обновленного состояния
        display.fill('black')  # можно использовать названия цветов в виде строки, а можно RGB-значения
        # display.fill(pygame.Color(0,0,0))
        target.draw()
        crosshair.draw()
        pygame.display.update()
        # -----------------


if __name__ == '__main__':
    main()
