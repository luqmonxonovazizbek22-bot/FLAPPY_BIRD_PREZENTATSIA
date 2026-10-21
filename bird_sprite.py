import pygame


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = []
        self.index = 0
        self.counter = 0
        for number in range(1, 4):
            photo = pygame.image.load(f"pictures/bird{number}.png")
            self.images.append(photo)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_y = 0
        self.clicked = False

    def update(self, flying, window, game_over):

        if flying == True:
            self.speed_y += 0.5
            if self.speed_y >= 5:
                self.speed_y = 5
            if self.rect.y < window.get_height():
                self.rect.y += self.speed_y

        if game_over == False:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] == True and self.clicked == False:
                self.clicked = True
                self.speed_y = -10
            if key[pygame.K_SPACE] == False:
                self.clicked = False


            self.counter += 1
            if self.counter == 5:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0

            self.image = self.images[self.index]
            self.image = pygame.transform.rotate(self.images[self.index],
                                                 self.speed_y * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)