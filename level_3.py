import pygame
import random
import os

from bird_player import Bird
from pipe_player import Pipe, pipe_frequence
from coin_sprite import Coin
from stone_sprite import Stone

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((864, 800), pygame.RESIZABLE)

back_image = pygame.transform.scale(
    pygame.image.load("pictures/background.png"), (864, 800)
)
ground_image = pygame.transform.scale(
    pygame.image.load("pictures/ground.png"), (1000, 100)
)
heart_img = pygame.transform.scale(
    pygame.image.load("pictures/hearth.png"), (40, 40)
)

konstruksiya = pygame.font.SysFont("roboto", 30)
font_score = pygame.font.SysFont("roboto", 50)
font_level = pygame.font.SysFont("roboto", 50)

olsh = pygame.mixer.Sound("die.mp3")
tanga_olish = pygame.mixer.Sound("tanga olish.mp3")
uchish_vrp = pygame.mixer.Sound("uchish.mp3")

bird = Bird(60, 380)
bird_group = pygame.sprite.Group(bird)

pipe_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
stone_group = pygame.sprite.Group()

ground_x = 0
ground_speed = 3

flying = False
game_over = False
level_passed = False

score = 0
lives = 3

bird_speed_x = 0
game_over_sound_played = False

last_pipe = pygame.time.get_ticks()
last_stone = pygame.time.get_ticks()
stone_delay = 1500

next_button = pygame.transform.scale(
    pygame.image.load("pictures/e16d3ed1-c8be-4ca3-aadb-1d34bc2f6ded_removalai_preview.png"),
    (500, 300)
)
next_button_rect = next_button.get_rect()

restart_button = pygame.transform.scale(
    pygame.image.load("pictures/72e6fdf6-a1cf-40fd-9c48-d1bc9a9d6813_removalai_preview.png"),
    (320, 150)
)
restart_rect = restart_button.get_rect()

game_over_img = pygame.transform.scale(
    pygame.image.load("pictures/gameover.png"), (500, 300)
)
game_over_rect = game_over_img.get_rect()


# ===== 4 ta pipe o‘chirish funksiyasi =====
def remove_4_pipes(group):
    count = 0
    for pipe in group.sprites():
        pipe.kill()
        count += 1
        if count >= 4:
            break


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
            if event.key == pygame.K_a:
                bird_speed_x = -5
            if event.key == pygame.K_d:
                bird_speed_x = 5

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_d):
                bird_speed_x = 0

    window.blit(ground_image, (ground_x, 765))

    bird_group.draw(window)
    pipe_group.draw(window)
    coin_group.draw(window)
    stone_group.draw(window)

    window.blit(font_level.render("LEVEL 3", True, "yellow"), (10, 10))
    window.blit(konstruksiya.render("D -> Oldinga   A -> Orqaga", True, "white"), (370, 10))
    window.blit(font_score.render(f"{score} / 10", True, "white"), (430, 40))

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
                Coin(window.get_width() + 30,
                     window.get_height() // 2 + random.randint(-50, 50))
            )
            last_pipe = now

        if now - last_stone > stone_delay:
            stone_group.add(Stone(random.randint(40, window.get_width() - 40)))
            last_stone = now

        ground_x -= ground_speed
        if ground_x < -100:
            ground_x = 0

        bird.rect.x += bird_speed_x
        bird.rect.left = max(0, bird.rect.left)
        bird.rect.right = min(window.get_width(), bird.rect.right)

        bird_group.update(window, flying, game_over)
        pipe_group.update(window)
        coin_group.update()
        stone_group.update()

        # ---- PIPE ----
        for pipe in pipe_group:
            if pygame.sprite.collide_mask(pipe, bird):
                lives -= 1
                remove_4_pipes(pipe_group)
                bird.rect.center = (60, 380)
                flying = False
                if lives <= 0:
                    game_over = True

            if pipe.rect.right < bird.rect.left and not pipe.passed and pipe.rect.y > 0:
                pipe.passed = True
                score += 1

        # ---- COIN (PIPE O‘ZGARMAYDI) ----
        for coin in coin_group:
            if pygame.sprite.collide_mask(coin, bird):
                tanga_olish.play()
                score += 2
                coin.kill()

        # ---- STONE ----
        for stone in stone_group:
            if pygame.sprite.collide_mask(stone, bird):
                lives -= 1
                remove_4_pipes(pipe_group)
                stone.kill()
                bird.rect.center = (60, 380)
                flying = False
                if lives <= 0:
                    game_over = True

        if score >= 10:
            level_passed = True
            flying = False

    if level_passed:
        next_button_rect.center = (window.get_width() // 2, window.get_height() // 2)
        window.blit(next_button, next_button_rect)
        if pygame.mouse.get_pressed()[0] and next_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.quit()
            os.system("python level_4.py")
            exit()

    if game_over:
        if not game_over_sound_played:
            olsh.play()
            game_over_sound_played = True

        game_over_rect.center = (window.get_width() // 2, window.get_height() // 3)
        window.blit(game_over_img, game_over_rect)

        restart_rect.center = (window.get_width() // 2, window.get_height() // 1.8)
        window.blit(restart_button, restart_rect)

        if pygame.mouse.get_pressed()[0] and restart_rect.collidepoint(pygame.mouse.get_pos()):
            game_over = False
            level_passed = False
            flying = False
            score = 0
            lives = 3
            bird.rect.center = (60, 380)
            pipe_group.empty()
            coin_group.empty()
            stone_group.empty()
            last_pipe = pygame.time.get_ticks()
            last_stone = pygame.time.get_ticks()
            game_over_sound_played = False

    pygame.display.update()

pygame.quit()
