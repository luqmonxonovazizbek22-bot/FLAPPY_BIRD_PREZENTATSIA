import pygame

# pipe_gap, pipe_frequence = 200, 1500
# last_pipe = pygame.time.get_ticks() - pipe_frequence

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("pictures/coin.png")
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_y = 3

    def update(self):
        self.rect.x -= self.speed_y
        if self.rect.x < -25:
            self.kill()
