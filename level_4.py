import pygame
import random
import os

from bird_player import Bird
from pipe_player import Pipe, pipe_frequence
from coin_sprite import Coin

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# ===== SCREEN =====
window = pygame.display.set_mode((864, 800), pygame.RESIZABLE)
pygame.display.set_caption("Flappy Bird - Level 4")

# ===== IMAGES =====
back_image = pygame.transform.scale(
    pygame.image.load("pictures/8b375140-6bda-4b68-b202-961ffd841def.png"), (864, 800)
)
ground_image = pygame.transform.scale(
    pygame.image.load("pictures/ground.png"), (1000, 100)
)
heart_img = pygame.transform.scale(
    pygame.image.load("pictures/hearth.png"), (40, 40)
)

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

# ===== SOUNDS =====
olsh = pygame.mixer.Sound("die.mp3")
uchish_vrp = pygame.mixer.Sound("uchish.mp3")
tanga_olish = pygame.mixer.Sound("tanga olish.mp3")

# ===== FONTS =====
font_score = pygame.font.SysFont("roboto", 50)
font_level = pygame.font.SysFont("roboto", 50)
konstruksiya = pygame.font.SysFont("roboto", 30)

# ===== VARIABLES =====
bird = Bird(60, 380)
bird_group = pygame.sprite.Group(bird)

pipe_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
life_group = pygame.sprite.Group()

ground_x = 0
ground_speed = 3

flying = False
game_over = False
level_passed = False

score = 0
lives = 4
bird_speed_x = 0

last_pipe = pygame.time.get_ticks()
pipe_counter = 0

# ===== LIFE SPRITE =====
class Life(pygame.sprite.Sprite):
    def __init__(self, coin_group, pipe_group):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("pictures/hearth.png"), (40, 40)
        )
        self.rect = self.image.get_rect()
        placed = False
        while not placed:
            self.rect.center = (random.randint(50, 800), random.randint(100, 600))
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

# ===== FUNCTIONS =====
def remove_4_pipes(group):
    count = 0
    for pipe in group.sprites():
        pipe.kill()
        count += 1
        if count >= 4:
            break

# ===== MAIN LOOP =====
running = True
while running:
    clock.tick(60)
    window.blit(back_image, (0, 0))

    # ===== EVENTS =====
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and not level_passed:
                uchish_vrp.play()
                flying = True
                bird.velocity = -8
            if event.key == pygame.K_a:
                bird_speed_x = -2
            if event.key == pygame.K_d:
                bird_speed_x = 2
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_d):
                bird_speed_x = 0

    # ===== GROUND =====
    ground_x -= ground_speed
    if ground_x < -100:
        ground_x = 0
    window.blit(ground_image, (ground_x, 765))

    # ===== BIRD MOVEMENT =====
    bird.rect.x += bird_speed_x
    bird.rect.left = max(0, bird.rect.left)
    bird.rect.right = min(window.get_width(), bird.rect.right)

    # ===== DRAW GROUPS =====
    bird_group.draw(window)
    pipe_group.draw(window)
    coin_group.draw(window)
    life_group.draw(window)

    # ===== HUD =====
    window.blit(font_level.render("LEVEL 4", True, "yellow"), (10, 10))
    window.blit(konstruksiya.render("D -> Oldinga   A -> Orqaga", True, "green"), (370, 10))
    window.blit(font_score.render(f"{score} / 15", True, "white"), (430, 40))
    for i in range(lives):
        window.blit(heart_img, (10 + i * 50, 60))

    # ===== COLLISION WITH SCREEN =====
    if flying and not game_over:
        if bird.rect.bottom >= 765 or bird.rect.top <= 0:
            lives -= 1
            bird.rect.center = (60, 380)
            flying = False
            if lives <= 0:
                game_over = True

    # ===== GAME LOGIC =====
    if flying and not game_over and not level_passed:
        now = pygame.time.get_ticks()

        # ---- PIPE + COIN SPAWN ----
        if now - last_pipe > pipe_frequence:
            offset = random.randint(-100, 100)
            top_pipe = Pipe(window.get_width(), window.get_height() // 2 + offset, 1)
            bottom_pipe = Pipe(window.get_width(), window.get_height() // 2 + offset, 0)
            pipe_group.add(top_pipe, bottom_pipe)

            # coin
            coin_group.add(
                Coin(window.get_width() + 30, window.get_height() // 2 + random.randint(-50, 50))
            )

            # life every 3 pipes
            pipe_counter += 1
            if pipe_counter % 3 == 0:
                life_group.add(Life(coin_group, pipe_group))

            last_pipe = now

        # ---- UPDATE GROUPS ----
        bird_group.update(window, flying, game_over)
        pipe_group.update(window)
        coin_group.update()
        life_group.update()

        # ---- COLLISIONS ----
        for pipe in pipe_group:
            if pygame.sprite.collide_mask(pipe, bird):
                lives -= 1
                remove_4_pipes(pipe_group)
                coin_group.empty()
                life_group.empty()
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
                score += 2
                coin.kill()

        for life in life_group:
            if pygame.sprite.collide_mask(life, bird):
                if lives < 4:
                    lives += 1
                life.kill()

        if score >= 15:
            level_passed = True
            flying = False

    # ===== NEXT LEVEL =====
    if level_passed:
        next_button_rect.center = (window.get_width() // 2, window.get_height() // 2)
        window.blit(next_button, next_button_rect)
        if pygame.mouse.get_pressed()[0] and next_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.quit()
            os.system("python level_5.py")
            exit()

    # ===== GAME OVER =====
    if game_over:
        game_over_rect.center = (window.get_width() // 2, window.get_height() // 3)
        window.blit(game_over_img, game_over_rect)

        restart_rect.center = (window.get_width() // 2, window.get_height() // 1.8)
        window.blit(restart_button, restart_rect)

        if pygame.mouse.get_pressed()[0] and restart_rect.collidepoint(pygame.mouse.get_pos()):
            game_over = False
            flying = False
            score = 0
            lives = 4
            bird.rect.center = (60, 380)
            pipe_group.empty()
            coin_group.empty()
            life_group.empty()
            last_pipe = pygame.time.get_ticks()
            pipe_counter = 0

    pygame.display.update()

pygame.quit()
