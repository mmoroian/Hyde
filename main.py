import pygame
from pygame.locals import *

clock = pygame.time.Clock()

pygame.init()

pygame.display.set_caption("Platformer")

window_size = (1280, 720)

screen = pygame.display.set_mode(window_size)  # initiate the window

display = pygame.Surface((320, 192))  # used as the surface for rendering, which is scaled

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
to_left = False

game_map = [[3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [3, 0, 0, 0, 0, 9, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [3, 0, 0, 0, 0, 9, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [3, 0, 0, 1, 1, 9, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


def mirror(img):
    return pygame.transform.flip(img, True, False)


pcb_img = pygame.image.load("pcb.png")
green_img = pygame.image.load("green.png")
green_shadow = pygame.image.load("green_shadow.png")
red_img = pygame.image.load("red.png")
red_shadow = pygame.image.load("red_shadow.png")

player_img = pygame.image.load('stand.png')
player_stand = pygame.image.load('stand.png')
player_walk = pygame.image.load('man.png')
player_jump = pygame.image.load('jump.png')

player_rect = pygame.Rect(16, 100, 16, 32)


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += int(movement[0])
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += int(movement[1])
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


while True:  # game loop
    display.fill((0, 96, 184))  # clear screen by filling it with blue

    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == 1:
                display.blit(pcb_img, (x * 16, y * 16))
            if tile == 6:
                display.blit(green_img, (x * 16, y * 16))
            if tile == 3:
                display.blit(green_shadow, (x * 16, y * 16))
            if tile == 9:
                display.blit(red_img, (x * 16, y * 16))
            if tile == 4:
                display.blit(red_shadow, (x * 16, y * 16))
            if tile != 0:
                tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
            x += 1
        y += 1

    player_movement = [0, 0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions["bottom"] == True:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1

    display.blit(player_img, (player_rect.x, player_rect.y))

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:
            pygame.quit()

        # Key press events & image changes
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
                to_left = False
                player_img = player_walk

            if event.key == K_LEFT:
                moving_left = True
                to_left = True
                player_img = mirror(player_walk)

            if event.key == K_SPACE:
                if air_timer < 6:
                    vertical_momentum = -6
                if to_left:
                    player_img = mirror(player_jump)
                else:
                    player_img = player_jump

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
                to_left = False
                player_img = player_stand

            if event.key == K_LEFT:
                moving_left = False
                to_left = True
                player_img = mirror(player_stand)
            if event.key == K_SPACE:
                if to_left:
                    player_img = mirror(player_stand)
                else:
                    player_img = player_stand

    screen.blit(pygame.transform.scale(display, window_size), (0, 0))
    pygame.display.update()
    clock.tick(60)
