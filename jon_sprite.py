# life_sprite.py
import pygame
import random

# Life sprite class
class Life(pygame.sprite.Sprite):
    def __init__(self, top_pipe, bottom_pipe):
        super().__init__()
        self.image = pygame.image.load("pictures/hearth.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()

        # Life pipe'larning ortasida paydo bo‘ladi
        self.rect.centerx = top_pipe.rect.centerx
        self.rect.centery = (top_pipe.rect.bottom + bottom_pipe.rect.top) // 2

    def update(self, *args):
        # Life chapga harakat qiladi pipe bilan birga
        self.rect.x -= 3  # ground_speed yoki pipe speed bilan moslashtirish mumkin

        # Agar ekran tashqarisiga chiqsa, o‘chirilsin
        if self.rect.right < 0:
            self.kill()
