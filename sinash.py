import pygame
import random
import sys

pygame.init()

# Oyna sozlamalari
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# Ranglar
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (135, 206, 235)
RED = (255, 0, 0)

# Qush
bird_x = 80
bird_y = HEIGHT // 2
bird_radius = 15
gravity = 0.5
bird_movement = 0
jump = -8

# Trubalar
pipe_width = 60
pipe_gap = 150
pipe_speed = 3
pipes = []

def create_pipe():
    height = random.randint(100, 400)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(
        WIDTH, height + pipe_gap, pipe_width, HEIGHT
    )
    return top_pipe, bottom_pipe

pipes.extend(create_pipe())

score = 0
game_over = False

# O‘yin sikli
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_movement = jump
            if event.key == pygame.K_SPACE and game_over:
                # Qayta boshlash
                bird_y = HEIGHT // 2
                bird_movement = 0
                pipes.clear()
                pipes.extend(create_pipe())
                score = 0
                game_over = False

    screen.fill(BLUE)

    if not game_over:
        # Qush harakati
        bird_movement += gravity
        bird_y += bird_movement

        # Trubalar
        for pipe in pipes:
            pipe.x -= pipe_speed

        # Yangi truba
        if pipes[0].x < -pipe_width:
            pipes.pop(0)
            pipes.pop(0)
            pipes.extend(create_pipe())
            score += 1

        # To‘qnashuv
        bird_rect = pygame.Rect(
            bird_x - bird_radius,
            bird_y - bird_radius,
            bird_radius * 2,
            bird_radius * 2
        )

        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                game_over = True

        if bird_y < 0 or bird_y > HEIGHT:
            game_over = True

    # Chizish
    pygame.draw.circle(screen, RED, (bird_x, int(bird_y)), bird_radius)

    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if game_over:
        over_text = font.render("GAME OVER", True, WHITE)
        restart_text = font.render("SPACE - qayta boshlash", True, WHITE)
        screen.blit(over_text, (100, 250))
        screen.blit(restart_text, (40, 300))

    pygame.display.update()
    clock.tick(60)
