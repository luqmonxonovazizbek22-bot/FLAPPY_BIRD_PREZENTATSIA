import pygame

pipe_gap = 200
pipe_frequence = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequence

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, width=78, height=560):
        """
        x, y          -> pipe boshlang'ich koordinatalari
        position      -> 1 = pastki pipe, 0 = yuqori pipe
        width, height -> pipe o'lchamlari
        """
        super().__init__()
        self.image = pygame.image.load("../prezent/pictures/pipi.jpg")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()

        if position == 1:  # pastki pipe
            self.rect.topleft = [x, y + pipe_gap//2]
        elif position == 0:  # yuqori pipe
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect()
            self.rect.bottomleft = [x, y - pipe_gap//2]

        self.speed_y = 3
        self.passed = False

    def update(self, window):
        self.rect.x -= self.speed_y  # pipe chapga siljiydi
        if self.rect.right < 0:       # ekran tashqarisiga chiqqanda
            self.kill()
