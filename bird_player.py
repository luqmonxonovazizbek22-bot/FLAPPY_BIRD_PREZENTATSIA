import pygame


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = []
        for n in range(3):
            photo = pygame.image.load(f"pictures/bird{n + 1}.png")
            self.images.append(photo)
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed_y = 0
        self.clicked = False

    def update(self, window, flying, game_over):
        if flying == True:
            self.speed_y += 0.5
            if self.speed_y > 3:
                self.speed_y = 3
            if self.rect.bottom < 768:
                self.rect.y += int(self.speed_y)

        if game_over == False:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.clicked == False:
                self.clicked = True
                self.speed_y = -10
            if not key[pygame.K_SPACE]:
                self.clicked = False

            self.counter += 1
            if self.counter > 5:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0

            self.image = self.images[self.index]
            # rotate and flip
            self.image = pygame.transform.rotate(self.images[self.index], self.speed_y * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], 270)
