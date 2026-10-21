import pygame
import random

class Stone(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.image.load("pictures/tosh.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = -50
        self.speed = random.randint(5, 9)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 800:
            self.kill()
