import pygame
import random
import sys

from pygame import Surface, SurfaceType

pygame.init()

WIDTH = 1540
HEIGHT = 816

RED = (0, 0, 255)
green = (255, 0, 0)
YELLOW = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255, 255)

player_size = 50
player_pos = [WIDTH / 2, HEIGHT - 1.5 * player_size]

enemy_size = 50
enemy_pos = [0, 0]
enemy_list = [enemy_pos]

speed1 = 10
game_over = False
score = 1

clock = pygame.time.Clock()
myFont = pygame.font.SysFont("times new roman", 44)
screen: Surface | SurfaceType = pygame.display.set_mode((WIDTH, HEIGHT))


def set_level(score, speed1):

    if score < 20:
        speed1 = 5
    elif score < 40 and speed1 < 8:
        speed1 = 8
    elif score < 60:
        speed1 = 12
    else:
        speed1 = 15
    return speed1


def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, WIDTH - enemy_size)
        y_pos = 1
        enemy_list.append([x_pos, y_pos])


def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.circle(screen, green, enemy_pos, 25, 0)


def update_enemy_positions(enemy_list, score) -> object:
    for idx, enemy_pos in enumerate(enemy_list):
        if 0 <= enemy_pos[1] < HEIGHT:
            enemy_pos[1] += speed1
        else:
            enemy_list.pop(idx)
            score += 1
    return score


def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False


def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (p_x <= e_x < (p_x + player_size)) or (e_x <= p_x < (e_x + enemy_size)):
        if (p_y <= e_y < (p_y + player_size)) or (e_y <= p_y < (e_y + enemy_size)):
            return True
    return False


while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            x = player_pos[0]
            y = player_pos[1]



            if event.key == pygame.K_LEFT:
                x -= player_size
            elif event.key == pygame.K_RIGHT:
                x += player_size
            elif event.key == pygame.K_UP:
                y -= player_size
            elif event.key == pygame.K_DOWN:
                y += player_size

            player_pos = [x, y]

    screen.fill(BACKGROUND_COLOR)

    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list, score)
    speed1 = set_level(score, 10)

    text = "Score:" + str(score)
    label = myFont.render(text, False, YELLOW)
    screen.blit(label, (WIDTH - 200, 20))

    if collision_check(enemy_list, player_pos):
        game_over = True
        break

    draw_enemies(enemy_list)

    pygame.draw.circle(screen, RED, (player_pos[0], player_pos[1]), 25, 25)

    clock.tick(45)

    pygame.display.update()
