import pygame
import random
import os
import pygame.mixer

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("간단한 게임")


bg_image = pygame.image.load("C:/Users/ilove/Desktop/Games/hamster's_fire_escape_game/images/back.png")
player_image = pygame.image.load("C:/Users/ilove/Desktop/Games/hamster's_fire_escape_game/images/햄스터.png")
obstacle_image = pygame.image.load("C:/Users/ilove/Desktop/Games/hamster's_fire_escape_game/images/불.png")

backgroundMusic = pygame.mixer.Sound("C:/Users/ilove/Desktop/Games/hamster's_fire_escape_game/music/8-bit-classic-arcade-game-116832.mp3")
backgroundMusic.play(-1)

font = pygame.font.Font(None, 28)

player_x = WINDOW_WIDTH // 2
player_y = WINDOW_HEIGHT - 100
obstacle_x = WINDOW_WIDTH // 2
obstacle_y = 0

score = 0
time_counter = 0
player_life = 3

while True:
    for game_event in pygame.event.get():
        if game_event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 5
    if keys[pygame.K_RIGHT] and player_x < WINDOW_WIDTH - player_image.get_width():
        player_x += 5

    obstacle_y += 5
    if obstacle_y > WINDOW_HEIGHT:
        obstacle_y = 0
        obstacle_x = random.randint(0, WINDOW_WIDTH - obstacle_image.get_width())
        score += 1

    player_rect = pygame.Rect(player_x, player_y, player_image.get_width(), player_image.get_height())
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_image.get_width(), obstacle_image.get_height())
    if player_rect.colliderect(obstacle_rect):
        player_life -= 1
        if player_life == 0:
            print("게임 오버!")
            pygame.quit()
            exit()
        else:
            player_x = WINDOW_WIDTH // 2
            player_y = WINDOW_HEIGHT - 100
            obstacle_x = random.randint(0, WINDOW_WIDTH - obstacle_image.get_width())
            obstacle_y = 0

    time_counter += pygame.time.Clock().tick(60)

    game_window.blit(bg_image, (0, 0))
    game_window.blit(player_image, (player_x, player_y))
    game_window.blit(obstacle_image, (obstacle_x, obstacle_y))


    survived_text = font.render("Survived Time : " + str(int(time_counter / 1000)), True, (255, 255, 255))
    life_text = font.render("Life : " + str(player_life), True, (255, 255, 255))
    game_window.blit(survived_text, (10, 10))
    game_window.blit(life_text, (WINDOW_WIDTH - life_text.get_width() - 10, 10))

    pygame.mixer.music.set_volume(0.5)

    pygame.display.update()
