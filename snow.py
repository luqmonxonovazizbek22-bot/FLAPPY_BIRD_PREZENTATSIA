import random
import pygame

# Qor zarrachalari uchun ro'yxat
snow_particles = []

# Qor parchasini yaratish
def create_snow(window):
    for _ in range(50):  # Bir vaqtda 50 ta parcha hosil qilish
        x = random.randint(0, window.get_width())
        y = random.randint(-100, window.get_height())
        size = random.randint(2, 4)  # Parcha o'lchami
        speed = random.randint(1, 3)  # Parcha tushish tezligi
        snow_particles.append([x, y, size, speed])

# Qorni chizish va harakatlantirish
def update_snow(window):
    for particle in snow_particles:
        particle[1] += particle[3]  # Pastga harakat
        pygame.draw.circle(window, "white", (particle[0], particle[1]), particle[2])
        if particle[1] > window.get_height():  # Ekrandan chiqib ketsa
            particle[1] = random.randint(-20, -5)  # Yangi parcha uchun boshlang'ich nuqta
            particle[0] = random.randint(0, window.get_width())


# Asosiy loopda yangilash
# create_snow()  # Qorni o'yinni boshlashda yaratish
# while running:
#     update_snow()  # Qorni har bir kadrlarda yangilash