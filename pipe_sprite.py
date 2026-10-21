import pygame

pipe_gap, pipe_frequence = 200, 1500
last_pipe = pygame.time.get_ticks() - pipe_frequence

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__()
        self.image = pygame.image.load("pictures/pipe.png")
        self.rect = self.image.get_rect()
        if position == 1:
            self.rect.topleft = (x, y + int(pipe_gap/2))
        if position == 0:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect.bottomleft = (x, y - int(pipe_gap / 2))
        self.speed_y = 5
        self.passed = False

    def update(self):
        self.rect.x -= self.speed_y
        if self.rect.x < -80:
            self.kill()
