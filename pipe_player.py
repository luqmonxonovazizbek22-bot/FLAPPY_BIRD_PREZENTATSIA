import pygame


pipe_gap = 200
pipe_frequence = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequence

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__()
        self.image = pygame.image.load("pictures/pipe.png")
        self.rect = self.image.get_rect()
        if position == 1:
            self.rect.topleft = [x, y + pipe_gap//2]
        if position == 0:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect()
            self.rect.bottomleft = [x, y - pipe_gap//2]
        self.speed_y = 3
        self.passed = False

    def update(self, window):
        self.rect.x -= self.speed_y
        if self.rect.x <= -50:
            self.kill()


class Pipe2(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__()
        self.image = pygame.image.load("pictures/pipe_red.png")
        self.image = pygame.transform.scale(self.image, (78, 560))
        self.rect = self.image.get_rect()
        if position == 1:
            self.rect.topleft = [x, y + pipe_gap//2]
        if position == 0:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect()
            self.rect.bottomleft = [x, y - pipe_gap//2]
        self.speed_y = 3
        self.passed = False

    def update(self, window):
        self.rect.x -= self.speed_y
        if self.rect.x <= -50:
            self.kill()