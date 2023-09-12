# import pygame
#
# pygame.init()
#
# W, H = 800, 600
#
# display = pygame.display.set_mode((W, H))
# font = pygame.font.get_default_font()
# font = pygame.font.Font(font, 48)
# render = font.render('Привет, pygame', 1, 'green')
# render_hitbox = render.get_rect(center=(W / 2, H / 2))
#
#
# def main():
#     while True:
#         # 1) Считывание ввода
#         for i in pygame.event.get():
#             if i.type == pygame.QUIT:
#                 return
#         # -----------------
#         # 2) Обновление состояния игры
#
#         # -----------------
#         # 3) Отрисовка обновленного состояния
#         display.blit(render, render_hitbox)
#         pygame.display.update()
#         # -----------------
#
#
# if __name__ == '__main__':
#     main()
import pygame
pygame.init()
W, H = 800, 600
display = pygame.display.set_mode((W, H))
font = pygame.font.get_default_font()
font = pygame.font.Font(font, 48)
render = font.render('Привет, pygame', 1, 'green')
render_hitbox = render.get_rect(center=(W / 2, H / 2))
def main():
    while True:
        pygame.event.get()
        # 3) Отрисовка обновленного состояния
        display.blit(render, render_hitbox)
        pygame.display.update()
        # -----------------


if __name__ == '__main__':
    main()

