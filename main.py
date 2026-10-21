import pygame
from bird_sprite import Bird
from pipe_sprite import Pipe, last_pipe, pipe_frequence
import random
from coin_sprite import Coin
from snow import create_snow, update_snow

pygame.init()
window = pygame.display.set_mode([864, 790], pygame.RESIZABLE)

back = pygame.image.load("pictures/background.png")
back = pygame.transform.scale(back, (864, 790))

ground = pygame.image.load("pictures/ground.png")
ground = pygame.transform.scale(ground, (1200, 150))
ground_x = 0

bird = Bird(50, 350)
bird_group = pygame.sprite.Group()
bird_group.add(bird)
flying = False
game_over = False

pipe_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
score = 0

create_snow(window)

running = True
while running:
    window.blit(back, (0, 0))
    window.blit(ground, (ground_x, 750))
    bird_group.draw(window)
    bird_group.update(flying, window, game_over)

    pipe_group.draw(window)
    coin_group.draw(window)
    update_snow(window)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and flying == False and game_over == False:
            flying = True

    if game_over == False and flying == True:
        ground_x -= 5
        if ground_x <= -50:
            ground_x = 0
        if bird.rect.y >= window.get_height() - 80:
            game_over = True
            flying = False
        if bird.rect.y <= 0:
            game_over = True

        pipe_group.update()
        coin_group.update()
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe > pipe_frequence:
            random_pipe_y = random.randint(-100, 100)
            top_pipe = Pipe(window.get_width(), int(window.get_height()/2) + random_pipe_y, 1)
            bottom_pipe = Pipe(window.get_width(), int(window.get_height()/2) + random_pipe_y, 0)
            pipe_group.add(top_pipe)
            pipe_group.add(bottom_pipe)

            random_coin_y = random.randint(-50, 50)
            coin = Coin(window.get_width()+30, window.get_height()//2 + random_coin_y)
            coin_group.add(coin)

            last_pipe = current_time

        for pipe in pipe_group:
            if pipe.rect.right < bird.rect.left and pipe.passed == False:
                if pipe.rect.y > 0:
                    score += 1
                    print(score)
                    pipe.passed = True

    pygame.time.delay(15)
    pygame.display.update()

pygame.quit()
