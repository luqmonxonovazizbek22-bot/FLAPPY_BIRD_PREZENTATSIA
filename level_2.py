import pygame
import random
import os

from bird_player import Bird
from pipe_player import Pipe, pipe_frequence
from coin_sprite import Coin

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((864, 800), pygame.RESIZABLE)

olsh = pygame.mixer.Sound("die.mp3")
olsh.set_volume(1.0)

tanga_olish = pygame.mixer.Sound("tanga olish.mp3")
tanga_olish.set_volume(1.0)

uchish_vrp = pygame.mixer.Sound("uchish.mp3")
uchish_vrp.set_volume(1.0)

back_image = pygame.transform.scale(
    pygame.image.load("pictures/background.png"), (864, 800)
)
ground_image = pygame.transform.scale(
    pygame.image.load("pictures/ground.png"), (1000, 100)
)
heart_img = pygame.transform.scale(
    pygame.image.load("pictures/hearth.png"), (40, 40)
)

font_score = pygame.font.SysFont("roboto", 50)
yana = pygame.font.SysFont("roboto", 50)

bird = Bird(60, 380)
bird_group = pygame.sprite.Group(bird)

pipe_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

ground_x = 0
ground_speed = 3

flying = False
game_over = False
level_passed = False

score = 0
lives = 3

game_over_sound_played = False

last_pipe = pygame.time.get_ticks()

next_button = pygame.transform.scale(
    pygame.image.load("pictures/e16d3ed1-c8be-4ca3-aadb-1d34bc2f6ded_removalai_preview.png"),
    (500, 300)
)
next_button_rect = next_button.get_rect()

button_image = pygame.transform.scale(
    pygame.image.load("pictures/72e6fdf6-a1cf-40fd-9c48-d1bc9a9d6813_removalai_preview.png"),
    (320, 150)
)
button_rect = button_image.get_rect()

game_over_button = pygame.transform.scale(
    pygame.image.load("pictures/gameover.png"),
    (500, 300)
)
game_over_rect = game_over_button.get_rect()

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

    window.blit(ground_image, (ground_x, 765))
    bird_group.draw(window)
    pipe_group.draw(window)
    coin_group.draw(window)

    window.blit(yana.render("LEVEL 2", True, "yellow"), (10, 10))
    window.blit(font_score.render(f"{score} / 5", True, "white"), (430, 40))

    for i in range(lives):
        window.blit(heart_img, (10 + i * 50, 60))

    if flying and not game_over:
        if bird.rect.bottom >= 765 or bird.rect.top <= 0:
            lives -= 1
            bird.rect.center = (60, 380)
            flying = False
            if lives <= 0:
                game_over = True

    if flying and not game_over and not level_passed:
        now = pygame.time.get_ticks()

        if now - last_pipe > pipe_frequence:
            offset = random.randint(-100, 100)
            pipe_group.add(
                Pipe(window.get_width(), window.get_height() // 2 + offset, 1),
                Pipe(window.get_width(), window.get_height() // 2 + offset, 0)
            )
            coin_group.add(
                Coin(
                    window.get_width() + 30,
                    window.get_height() // 2 + random.randint(-50, 50)
                )
            )
            last_pipe = now

        ground_x -= ground_speed
        if ground_x < -100:
            ground_x = 0

        bird_group.update(window, flying, game_over)
        pipe_group.update(window)
        coin_group.update()

        for pipe in pipe_group:
            if pygame.sprite.collide_mask(pipe, bird):
                lives -= 1
                bird.rect.center = (60, 380)
                flying = False
                if lives <= 0:
                    game_over = True

            if pipe.rect.right < bird.rect.left and not pipe.passed and pipe.rect.y > 0:
                pipe.passed = True
                score += 1

        for coin in coin_group:
            if pygame.sprite.collide_mask(coin, bird):
                tanga_olish.play()
                score += 1
                coin.kill()

        if score >= 5:
            level_passed = True
            flying = False

    if level_passed:
        next_button_rect.center = (window.get_width() // 2, window.get_height() // 2)
        window.blit(next_button, next_button_rect)
        if pygame.mouse.get_pressed()[0] and next_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.quit()
            os.system("python level_3.py")
            exit()

    if game_over:
        if not game_over_sound_played:
            olsh.play()
            game_over_sound_played = True

        game_over_rect.center = (window.get_width() // 2, window.get_height() // 3)
        window.blit(game_over_button, game_over_rect)

        button_rect.center = (window.get_width() // 2, window.get_height() // 1.9)
        window.blit(button_image, button_rect)

        if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(pygame.mouse.get_pos()):
            game_over = False
            level_passed = False
            pipe_group.empty()
            coin_group.empty()
            bird.rect.center = (60, 380)
            score = 0
            lives = 3
            flying = False
            last_pipe = pygame.time.get_ticks()
            game_over_sound_played = False

    pygame.display.update()

pygame.quit()
