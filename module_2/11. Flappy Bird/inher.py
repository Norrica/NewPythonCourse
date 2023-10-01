import pygame

class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.rect = self.image.get_rect(topleft=(x,y))

    def move(self):
        self.rect.y += 1

class FastEnemy(BaseEnemy):
    def __init__(self):
    def move(self):
        self.rect.y += 5

f = FastEnemy(1,2)
print(f.rect)