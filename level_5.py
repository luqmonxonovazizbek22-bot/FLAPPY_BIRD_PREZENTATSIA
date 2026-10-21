import pygame
import random
import os

from bird_player import Bird
from pipi_player2 import Pipe, pipe_frequence
from coin_sprite import Coin

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((864, 800), pygame.RESIZABLE)
pygame.display.set_caption("Flappy Bird - Level 5")

# ===== IMAGES & SOUNDS =====
back_image = pygame.image.load("pictures/img_4.png")
back_image = pygame.transform.smoothscale(back_image, window.get_size())

ground_image = pygame.image.load("pictures/ground.png")
ground_image = pygame.transform.scale(ground_image, (1000, 1))

heart_img = pygame.image.load("pictures/hearth.png")
heart_img = pygame.transform.scale(heart_img, (40, 40))

stone_img = pygame.image.load("pictures/tosh.png")
stone_img = pygame.transform.scale(stone_img, (40, 40))

game_over_image = pygame.image.load("pictures/gameover.png")
game_over_image = pygame.transform.scale(game_over_image, (500, 300))
game_over_rect = game_over_image.get_rect()

next_button = pygame.image.load("pictures/e16d3ed1-c8be-4ca3-aadb-1d34bc2f6ded_removalai_preview.png")
next_button = pygame.transform.scale(next_button, (500, 300))
next_button_rect = next_button.get_rect()

button_image = pygame.image.load("pictures/72e6fdf6-a1cf-40fd-9c48-d1bc9a9d6813_removalai_preview.png")
button_image = pygame.transform.scale(button_image, (320, 150))
button_rect = button_image.get_rect()

uchish_vrp = pygame.mixer.Sound("uchish.mp3")
uchish_vrp.set_volume(1.0)
tanga_olish = pygame.mixer.Sound("tanga olish.mp3")
tanga_olish.set_volume(1.0)
olsh = pygame.mixer.Sound("die.mp3")
olsh.set_volume(1.0)

font_score = pygame.font.SysFont("roboto", 50)
font_level = pygame.font.SysFont("roboto", 50)

# ===== GAME VARIABLES =====
ground_x = 0
ground_speed = 3

bird = Bird(60, 380)
bird_group = pygame.sprite.Group(bird)
pipe_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

stones = []
stone_timer = pygame.time.get_ticks()
last_pipe = pygame.time.get_ticks()

flying = False
game_over = False
level_passed = False
die_played = False
score = 0
lives = 4

# ===== FUNCTIONS =====
def remove_4_pipes(group):
    count = 0
    for pipe in group.sprites():
        pipe.kill()
        count += 1
        if count >= 4:
            break

# ===== GAME LOOP =====
running = True
while running:
    clock.tick(60)
    window.blit(back_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and not level_passed:
                uchish_vrp.play()
                flying = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        bird.rect.x -= 5
    if keys[pygame.K_d]:
        bird.rect.x += 5

    bird.rect.left = max(0, bird.rect.left)
    bird.rect.right = min(window.get_width(), bird.rect.right)

    window.blit(ground_image, (ground_x, 700))
    bird_group.draw(window)
    pipe_group.draw(window)
    coin_group.draw(window)

    for stone in stones:
        window.blit(stone_img, stone)

    window.blit(font_level.render("LEVEL 5", True, "yellow"), (15, 15))
    for i in range(lives):
        window.blit(heart_img, (10 + i * 50, 60))
    window.blit(font_score.render(f"{score} / 20", True, "white"), (430, 40))

    if flying and not game_over and not level_passed:
        now = pygame.time.get_ticks()

        # ----- CREATE PIPES & COINS -----
        if now - last_pipe > pipe_frequence:
            h = random.randint(-100, 100)
            pipe_group.add(
                Pipe(window.get_width(), window.get_height() // 2 + h, 1),
                Pipe(window.get_width(), window.get_height() // 2 + h, 0)
            )
            coin_group.add(
                Coin(window.get_width() + 30,
                     window.get_height() // 2 + random.randint(-30, 50))
            )
            last_pipe = now

        # ----- CREATE STONES -----
        if now - stone_timer > 1200:
            stones.append(pygame.Rect(random.randint(0, window.get_width() - 40), -40, 40, 40))
            stone_timer = now

        for stone in stones[:]:
            stone.y += 6
            if stone.y > 800:
                stones.remove(stone)

        ground_x -= ground_speed
        if ground_x <= -864:
            ground_x = 0

        bird_group.update(window, flying, game_over)
        pipe_group.update(window)
        coin_group.update()

        # ----- COLLISION CHECK -----
        hit = False  # collision flag

        # Pipe collision
        for pipe in pipe_group:
            if pygame.sprite.collide_mask(pipe, bird):
                hit = True
                break

        # Stone collision
        for stone in stones[:]:
            if stone.colliderect(bird.rect):
                hit = True
                break

        # If hit by pipe or stone, only one life lost
        if hit:
            lives -= 1
            stones.clear()
            remove_4_pipes(pipe_group)
            coin_group.empty()
            bird.rect.center = (60, 380)
            flying = False
            if lives <= 0:
                game_over = True

        # Passed pipes increase score
        for pipe in pipe_group:
            if pipe.rect.right < bird.rect.left and not pipe.passed and pipe.rect.y > 0:
                pipe.passed = True
                score += 1

        # Coin collision
        for coin in coin_group:
            if pygame.sprite.collide_mask(coin, bird):
                tanga_olish.play()
                score += 2
                coin.kill()

        if score >= 20:
            level_passed = True
            flying = False

    # ----- NEXT LEVEL BUTTON -----
    if level_passed:
        next_button_rect.center = (window.get_width() // 2, window.get_height() // 2)
        window.blit(next_button, next_button_rect)
        if pygame.mouse.get_pressed()[0] and next_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.quit()
            os.system("python level_6.py")
            exit()

    # ----- GAME OVER -----
    if game_over:
        if not die_played:
            olsh.play()
            die_played = True

        game_over_rect.center = (window.get_width() // 2, window.get_height() // 3)
        window.blit(game_over_image, game_over_rect)

        button_rect.center = (window.get_width() // 2, window.get_height() // 1.9)
        window.blit(button_image, button_rect)

        if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(pygame.mouse.get_pos()):
            game_over = False
            level_passed = False
            die_played = False
            pipe_group.empty()
            coin_group.empty()
            stones.clear()
            bird.rect.center = (60, 380)
            score = 0
            lives = 4
            flying = False
            last_pipe = pygame.time.get_ticks()

    pygame.display.update()

pygame.quit()
