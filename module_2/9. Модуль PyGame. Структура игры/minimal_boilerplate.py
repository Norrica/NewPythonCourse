import pygame

pygame.init()

W, H = 800, 600

display = pygame.display.set_mode((W, H))

sprite = pygame.image.load('res/crosshair_small.png')
hitbox = sprite.get_rect()
sprite2 = pygame.image.load('res/target_small.png')
hitbox2 = sprite.get_rect()


def is_key_pressed(key):
    return pygame.key.get_pressed()[key]


def where_mouse_pressed(mouse_key):
    buttons = pygame.mouse.get_pressed(num_buttons=5)
    if buttons[mouse_key]:
        return pygame.mouse.get_pos()


def main():
    while True:
        # 1) Считывание ввода
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                return

        if is_key_pressed(pygame.K_w):
            hitbox2.y -= 1
        if is_key_pressed(pygame.K_d):
            hitbox2.x += 1
        if is_key_pressed(pygame.K_s):
            hitbox2.y += 1
        if is_key_pressed(pygame.K_a):
            hitbox2.x -= 1

        hitbox.center = pygame.mouse.get_pos()
        # mouse_pos = where_mouse_pressed(0)
        # if mouse_pos:
        #     hitbox.center = mouse_pos
        # -----------------
        # 2) Обновление состояния игры
        # hitbox.x = 10
        # hitbox.y = 10
        # -----------------
        # 3) Отрисовка обновленного состояния
        display.fill('black')  # можно использовать названия цветов в виде строки, а можно RGB-значения
        # display.fill(pygame.Color(0,0,0))
        display.blit(sprite2, hitbox2)
        display.blit(sprite, hitbox)
        pygame.display.update()
        # -----------------


if __name__ == '__main__':
    main()
