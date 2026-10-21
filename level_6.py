import pygame
import random
import os

from bird_player import Bird
from pipe3_player import Pipe, pipe_frequence
from coin_sprite import Coin

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

screen_width, screen_height = 864, 800
window = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Flappy Bird - Level 6")

winning = pygame.mixer.Sound("winning-218995.mp3")
winning.set_volume(1.0)

back_image = pygame.image.load("../FLAPPY_BIRD_PREZENTATSIA/pictures/img_2.png")
back_image = pygame.transform.smoothscale(back_image, (screen_width, screen_height))

olsh = pygame.mixer.Sound("die.mp3")
olsh.set_volume(1.0)

uchish_vrp = pygame.mixer.Sound("uchish.mp3")
uchish_vrp.set_volume(1.0)

tanga_olish = pygame.mixer.Sound("tanga olish.mp3")
tanga_olish.set_volume(1.0)

ground_image = pygame.image.load("../FLAPPY_BIRD_PREZENTATSIA/pictures/ground.png")
ground_image = pygame.transform.scale(ground_image, (screen_width + 136, 1))

heart_img = pygame.image.load("../FLAPPY_BIRD_PREZENTATSIA/pictures/hearth.png")
heart_img = pygame.transform.scale(heart_img, (40, 40))

next_button = pygame.image.load("../FLAPPY_BIRD_PREZENTATSIA/pictures/img_3.png")
next_button = pygame.transform.scale(next_button, (600, 600))
next_button_rect = next_button.get_rect()

button_image = pygame.image.load("../FLAPPY_BIRD_PREZENTATSIA/pictures/72e6fdf6-a1cf-40fd-9c48-d1bc9a9d6813_removalai_preview.png")
button_image = pygame.transform.scale(button_image, (320, 150))
button_rect = button_image.get_rect()

game_over_image = pygame.image.load("../FLAPPY_BIRD_PREZENTATSIA/pictures/gameover.png")
game_over_image = pygame.transform.scale(game_over_image, (530, 300))
game_over_rect = game_over_image.get_rect()

stone_img = pygame.image.load("../FLAPPY_BIRD_PREZENTATSIA/pictures/tosh.png")
stone_img = pygame.transform.scale(stone_img, (40, 40))

font_score = pygame.font.SysFont("roboto", 50)
font_level = pygame.font.SysFont("roboto", 50)

ground_x = 0
ground_speed = 3

bird = Bird(60, screen_height // 2)
bird_group = pygame.sprite.Group(bird)
pipe_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
life_group = pygame.sprite.Group()

stones = []
stone_timer = pygame.time.get_ticks()
last_pipe = pygame.time.get_ticks()
pipe_counter = 0

flying = False
game_over = False
level_passed = False

score = 0
lives = 4
die_played = False
win_played = False

# ===== FUNCTIONS =====
def remove_4_pipes(group):
    count = 0
    for pipe in group.sprites():
        pipe.kill()
        count += 1
        if count >= 4:
            break

# ===== LIFE SPRITE =====
class Life(pygame.sprite.Sprite):
    def __init__(self, coin_group, pipe_group):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("../FLAPPY_BIRD_PREZENTATSIA/pictures/hearth.png"), (40, 40)
        )
        self.rect = self.image.get_rect()
        placed = False
        while not placed:
            self.rect.center = (random.randint(50, screen_width - 50), random.randint(100, screen_height - 200))
            collision = False
            for coin in coin_group:
                if self.rect.colliderect(coin.rect):
                    collision = True
                    break
            for pipe in pipe_group:
                if self.rect.colliderect(pipe.rect):
                    collision = True
                    break
            if not collision:
                placed = True
        self.velocity_x = -3

    def update(self):
        self.rect.x += self.velocity_x
        if self.rect.right < 0:
            self.kill()

# ===== RAIN (cosmetic) =====
rain_drops = [[random.randint(0, screen_width), random.randint(0, screen_height), random.randint(6, 15)] for _ in range(700)]
def draw_rain():
    for drop in rain_drops:
        drop[1] += drop[2]
        drop[0] -= 1
        if drop[1] > screen_height:
            drop[0] = random.randint(0, screen_width)
            drop[1] = random.randint(-100, -10)
            drop[2] = random.randint(6, 15)
        pygame.draw.line(window, (120, 180, 255), (drop[0], drop[1]), (drop[0], drop[1] + 6))

# ===== GAME LOOP =====
running = True
while running:
    clock.tick(60)
    window.blit(back_image, (0, 0))

    if flying:
        draw_rain()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and not level_passed:
                uchish_vrp.play()
                flying = True
            if event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        bird.rect.x -= 5
    if keys[pygame.K_d]:
        bird.rect.x += 5

    bird.rect.left = max(0, bird.rect.left)
    bird.rect.right = min(screen_width, bird.rect.right)

    window.blit(ground_image, (ground_x, screen_height - 100))
    ground_x -= ground_speed
    if ground_x <= -screen_width:
        ground_x = 0

    bird_group.draw(window)
    pipe_group.draw(window)
    coin_group.draw(window)
    life_group.draw(window)

    for stone in stones:
        window.blit(stone_img, stone)

    # HUD
    window.blit(font_level.render("LEVEL 6", True, "yellow"), (15, 15))
    for i in range(lives):
        window.blit(heart_img, (10 + i * 50, 60))
    window.blit(font_score.render(f"{score} / 25", True, "white"), (screen_width // 2 - 50, 40))

    if flying and not game_over and not level_passed:
        now = pygame.time.get_ticks()

        # ----- CREATE PIPES & COINS -----
        if now - last_pipe > pipe_frequence:
            pipe_height = random.randint(-100, 100)
            pipe_group.add(Pipe(screen_width, screen_height // 2 + pipe_height, 1),
                           Pipe(screen_width, screen_height // 2 + pipe_height, 0))
            coin_group.add(Coin(screen_width + 30, screen_height // 2 + random.randint(-30, 50)))

            pipe_counter += 1
            if pipe_counter % 3 == 0:  # Life every 3 pipes
                life_group.add(Life(coin_group, pipe_group))

            last_pipe = now

        # ----- CREATE STONES -----
        if now - stone_timer > 1200:
            stones.append(pygame.Rect(random.randint(0, screen_width - 40), -40, 40, 40))
            stone_timer = now

        for stone in stones[:]:
            stone.y += 6
            if stone.y > screen_height:
                stones.remove(stone)

        bird_group.update(window, flying, game_over)
        pipe_group.update(window)
        coin_group.update()
        life_group.update()

        # ----- COLLISION CHECK -----
        hit = False  # only 1 life per frame
        for pipe in pipe_group:
            if pygame.sprite.collide_mask(pipe, bird):
                hit = True
                break
        for stone in stones[:]:
            if stone.colliderect(bird.rect):
                hit = True
                break

        if hit:
            lives -= 1
            stones.clear()
            remove_4_pipes(pipe_group)
            coin_group.empty()
            life_group.empty()
            bird.rect.center = (60, screen_height // 2)
            flying = False
            if lives <= 0:
                game_over = True

        # Passed pipes → score
        for pipe in pipe_group:
            if pipe.rect.right < bird.rect.left and not pipe.passed and pipe.rect.y > 0:
                pipe.passed = True
                score += 1

        # Coin collision
        for coin in coin_group:
            if pygame.sprite.collide_mask(coin, bird):
                tanga_olish.play()
                score += 1
                coin.kill()

        # Life collision
        for life in life_group:
            if pygame.sprite.collide_mask(life, bird):
                if lives < 4:
                    lives += 1
                life.kill()

        if score >= 25:
            level_passed = True
            flying = False

    # NEXT LEVEL BUTTON
    if level_passed:
        next_button_rect.center = (screen_width // 2, screen_height // 2)
        window.blit(next_button, next_button_rect)
        if not win_played:
            winning.play()
            win_played = True

    # GAME OVER
    if game_over:
        if not die_played:
            olsh.play()
            die_played = True

        game_over_rect.center = (screen_width // 2, screen_height // 3)
        window.blit(game_over_image, game_over_rect)

        button_rect.center = (screen_width // 2, screen_height // 1.9)
        window.blit(button_image, button_rect)

        if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(pygame.mouse.get_pos()):
            game_over = False
            level_passed = False
            die_played = False
            win_played = False
            pipe_group.empty()
            coin_group.empty()
            life_group.empty()
            stones.clear()
            bird.rect.center = (60, screen_height // 2)
            score = 0
            lives = 4
            flying = False
            last_pipe = pygame.time.get_ticks()
            pipe_counter = 0

    pygame.display.update()

pygame.quit()
