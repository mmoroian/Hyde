import pygame

from pygame.locals import *

clock = pygame.time.Clock()

pygame.init()

pygame.display.set_caption("MyGame")  # Title name

window_size = (1280, 720)

background = pygame.image.load("back.png")

screen = pygame.display.set_mode(window_size)

# A new surface to render the tiles
display = pygame.Surface((320, 192))

pcb_img = pygame.image.load("pcb.png")
green_img = pygame.image.load("green.png")
green_shadow = pygame.image.load("green_shadow.png")
red_img = pygame.image.load("red.png")
red_shadow = pygame.image.load("red_shadow.png")

game_map = [[3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 9, 0, 0, 4, 0, 0],
            [6, 0, 0, 0, 0, 9, 0, 0, 4, 0, 0],
            [6, 0, 0, 0, 0, 9, 0, 0, 4, 0, 0],
            [6, 0, 0, 3, 0, 9, 0, 0, 9, 0, 0],
            [6, 0, 0, 3, 0, 9, 0, 0, 9, 0, 0],
            [6, 0, 0, 6, 0, 9, 0, 0, 9, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1]]

player_img = pygame.image.load("man.png")


def set_player(img):
    picture = pygame.image.load(img)
    character = pygame.transform.scale(picture, (picture.get_width() * 4, picture.get_height() * 4))
    return character


def mirror(img):
    picture = pygame.transform.flip(pygame.image.load(img), True, False)
    character = pygame.transform.scale(picture, (picture.get_width() * 4, picture.get_height() * 4))
    return character


# player = pygame.transform.scale(player_img, (player_img.get_width() * 4, player_img.get_height() * 4))

player = set_player("stand.png")

move_right = False
move_left = False
move_jump = False

player_location_x = 64
player_location_y = 64

momentum_y = 0

# RECTangle (Collisions with objects : x, y, height, width)
player_rect = pygame.Rect(player_location_x, player_location_y, player.get_width(), player.get_height())
# object_rect = pygame.Rect(60, 60, 100, 100)

# The Game Loop
running = True
while running:

    # Render the map
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
            x += 1
        y += 1

    if move_right:
        player_location_x += 4
    if move_left:
        player_location_x -= 4
    if move_jump:
        player_location_y -= 10

    player_rect.x = int(player_location_x)
    player_rect.y = int(player_location_y)

    if player_location_y > window_size[1] - player.get_height():
        momentum_y = 0
    else:
        momentum_y += 0.25

    if player_location_x > window_size[0] - player.get_height():
        player_location_x = window_size[0] - player.get_height()
    elif player_location_x < 0:
        player_location_x = 0

    player_location_y += momentum_y

    if player_location_y < player.get_height():
        screen.fill((0, 0, 0))
    else:
        screen.fill((0, 96, 184))

    # Background colour and image
    screen.fill((0, 96, 184))
    screen.blit(background, (0, 0))

    # Collision detection!
    # if player_rect.colliderect(object_rect):
    #     pygame.draw.rect(screen, (255, 0, 0), object_rect)  # if touching => red
    # else:
    #     pygame.draw.rect(screen, (0, 0, 0), object_rect)  # if not touching => black

    def collision_test(rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list


    def move(rect, movement, tiles):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        rect.x += movement[0]
        hit_list = collision_test(rect, tiles)
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True
        rect.y += movement[1]
        hit_list = collision_test(rect, tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
        return rect, collision_types


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key press events & image changes
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                move_right = True
                to_left = False
                player = set_player("man.png")

            if event.key == K_LEFT:
                move_left = True
                to_left = True
                player = mirror("man.png")

            if event.key == K_SPACE:
                move_jump = True
                if to_left:
                    player = mirror("jump.png")
                else:
                    player = set_player("jump.png")

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                move_right = False
                to_left = False
                player = set_player("stand.png")

            if event.key == K_LEFT:
                move_left = False
                to_left = True
                player = mirror("stand.png")

            if event.key == K_SPACE:
                move_jump = False
                if to_left:
                    player = mirror("stand.png")
                else:
                    player = set_player("stand.png")

    screen.blit(player, (int(player_location_x), int(player_location_y)))
    screen.blit(pygame.transform.scale(display, window_size), (0, 0))

    pygame.display.update()
    clock.tick(60)
