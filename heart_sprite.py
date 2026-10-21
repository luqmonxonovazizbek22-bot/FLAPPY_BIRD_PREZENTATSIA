# heart_sprite.py
import pygame

class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("pictures/hearth.png"), (35, 35)
        )
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.kill()
