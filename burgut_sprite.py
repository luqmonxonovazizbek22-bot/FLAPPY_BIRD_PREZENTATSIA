import pygame
import random

class EnemyBird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("pictures/burgut.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 45))
        self.rect = self.image.get_rect(midleft=(x, y))
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
