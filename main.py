import pygame
import sys  # prevents Segmentation fault 11
from pygame.locals import *


pygame.init()
pygame.mixer.init()  # Initialize music and sounds

# Load Sound and Music
money_collect = pygame.mixer.Sound("money.wav")  # only WAV is supported as Sound
pygame.mixer.music.load("loop1.wav")
# Loop music forever -1
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

pygame.display.set_caption("Hyde's Journey")

window_size = (1280, 720)

screen = pygame.display.set_mode(window_size)  # initiate the window

display = pygame.Surface((320, 192))  # used as the surface for rendering, which is scaled

moving_right = False
moving_left = False
jump = False
vertical_momentum = 0
air_timer = 0
to_left = False
walkCount = 0

money = 0

# Status Bar
# font = pygame.font.SysFont("Helvetica, Arial", 14)
font = pygame.font.Font("vga8.ttf", 16)


# def print_bar(num):
#    return font.render("Cash collected: $" + str(num), True, (0, 0, 0))


# Scrolling x & y for camera
scroll = [0, 0]


def load_map(file_name):
    f = open(file_name, "r")  # "r" means read
    data = f.read()
    f.close()
    data = data.split("\n")
    level_map = []
    for row in data:
        level_map.append(list(row))  # converts the text-line to a list
    return level_map


game_map = load_map("level.txt")


def mirror(img):
    return pygame.transform.flip(img, True, False)


pcb_img = pygame.image.load("pcb.png")
green_img = pygame.image.load("green.png")
green_shadow = pygame.image.load("green_shadow.png")
green_shadow_short = pygame.image.load("green_shadow_short.png")
red_img = pygame.image.load("red.png")
red_shadow = pygame.image.load("red_shadow.png")
red_shadow_short = pygame.image.load("red_shadow_short.png")
# cash = pygame.image.load("cash.png")
doji_green =  pygame.image.load("doji_green.png")
doji_red =  pygame.image.load("doji_red.png")

# Player image load
player_img = pygame.image.load("stand.png")
player_stand = pygame.image.load("stand.png")
player_walk = pygame.image.load("man.png")
player_walk2 = pygame.image.load("man2.png")
player_jump = pygame.image.load("jump.png")

walk_list = [pygame.image.load('man.png'), pygame.image.load('stand.png'), pygame.image.load('man2.png')]

walk_left = []
for i in walk_list:
    walk_left.append(mirror(i))

player_rect = pygame.Rect(32, 290, 16, 32)


def collision_test(rect, tiles):
    hit_list = []
    for a_tile in tiles:
        if rect.colliderect(a_tile):
            #print('TOP LEFT {}'.format(a_tile.top))
            #print('heigh {}'.format(a_tile.height))
            #print('COORDS of PERSON are X:{} X2:{} and of TILE are X:{} X2:{}'.format(rect.bottom,rect.top,a_tile.top,a_tile.bottom))
            hit_list.append(a_tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += int(movement[0])
    hit_list = collision_test(rect, tiles)
    for a_tile in hit_list:
        if movement[0] > 0:
            rect.right = a_tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = a_tile.right
            collision_types['left'] = True
    rect.y += int(movement[1])
    hit_list = collision_test(rect, tiles)
    for a_tile in hit_list:
        if movement[1] > 0:
            rect.bottom = a_tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = a_tile.bottom
            collision_types['top'] = True
    return rect, collision_types


def redrawGameWindow():
    global walkCount

    if walkCount + 1 >= 9:
        walkCount = 0

    if moving_right:
        display.blit(walk_list[walkCount // 3], (player_rect.x - int(scroll[0]), player_rect.y - int(scroll[1])))
        walkCount += 1
    elif moving_left:
        display.blit(walk_left[walkCount // 3], (player_rect.x - int(scroll[0]), player_rect.y - int(scroll[1])))
        walkCount += 1
    elif jump:
        if to_left:
            display.blit(mirror(player_jump), (player_rect.x - int(scroll[0]), player_rect.y - int(scroll[1])))
        else:
            display.blit(player_jump, (player_rect.x - int(scroll[0]), player_rect.y - int(scroll[1])))
        walkCount = 0
    else:
        if to_left:
            display.blit(mirror(player_stand), (player_rect.x - int(scroll[0]), player_rect.y - int(scroll[1])))
        else:
            display.blit(player_stand, (player_rect.x - int(scroll[0]), player_rect.y - int(scroll[1])))
        walkCount = 0

    pygame.display.update()


# The game loop
while True:
    display.fill((250, 250, 255))  # clear screen by filling it with blue
    back_img = pygame.image.load("city.png")
    display.blit(back_img, (0, 0))


    # display.blit(text, ((display.get_width() / 2 - text.get_rect().width / 2), (display.get_height() / 2 - 90)))
    # Scroll with lag
    if player_rect.x > 32:
        scroll[0] += (player_rect.x - scroll[0] - 64) / 16

    #if player_rect.y > 1 44:
    if player_rect.y == 272 :
        scroll[1] += (player_rect.y - scroll[1] - 144) / 16  # vertical scrolling
    if player_rect.y < 170  or moving_left:
        #print('Y is {}'.format(player_rect.y))
        scroll[1] += (player_rect.y - scroll[1] - 72) / 36  # vertical scrolling
    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for idx, tile in enumerate(layer):
            if tile == '1':
                display.blit(pcb_img, (x * 16 - int(scroll[0]), y * 16 - int(scroll[1])))
            if tile == '6':
                display.blit(green_img, (x * 16 - int(scroll[0]) , y * 16 - int(scroll[1])))
            if tile == '3':
                display.blit(green_shadow, (x * 16 - int(scroll[0]) + 7, y * 16 - int(scroll[1])))
                tile_rects.append(pygame.Rect(x * 16 + 7, y * 16, 1, 16))
            if tile == '9':
                display.blit(red_img, (x * 16 - int(scroll[0]), y * 16 - int(scroll[1])))
            if tile == '4':
                display.blit(red_shadow, (x * 16 - int(scroll[0]) + 7, y * 16 - int(scroll[1])))
                tile_rects.append(pygame.Rect(x * 16 + 7, y * 16, 1, 16))
            if tile == '5':
                if layer[idx-1] != '0':
                    display.blit(red_shadow_short, (x * 16 - int(scroll[0]) + 7, y * 16 - int(scroll[1]) ))
                    tile_rects.append(pygame.Rect(x * 16 + 7, y * 16 + 8, 1, 8))  
                else:
                    display.blit(red_shadow_short, (x * 16 - int(scroll[0]) + 7, y * 16 - int(scroll[1]) + 8))
                    tile_rects.append(pygame.Rect(x * 16 + 7, y * 16 + 8, 1, 8))  
            if tile == '7':
                if layer[idx-1] != '0':
                    display.blit(green_shadow_short, (x * 16 - int(scroll[0]) + 7, y * 16 - int(scroll[1]) ))
                    tile_rects.append(pygame.Rect(x * 16 + 7, y * 16 + 8, 1, 8))      
                else:
                    display.blit(green_shadow_short, (x * 16 - int(scroll[0]) + 7, y * 16 - int(scroll[1]) + 8))
                    tile_rects.append(pygame.Rect(x * 16 + 7, y * 16 + 8, 1, 8))
            if tile == '8':
                display.blit(doji_red, (x * 16 - int(scroll[0]) , y * 16 - int(scroll[1]) ))
                tile_rects.append(pygame.Rect(x * 16 , y * 16 , 16, 16))
            if tile == '2':
                display.blit(doji_green, (x * 16 - int(scroll[0]) , y * 16 - int(scroll[1]) ))
                tile_rects.append(pygame.Rect(x * 16 , y * 16 , 16, 16))                             
            if tile == '$':
                b = False
                cash = pygame.image.load("money16.png")
                cashRect = cash.get_rect()
                if tile == '$' and not b:
                    cashRect.x = (x * 16)
                    cashRect.y = (y * 16)
                if player_rect.colliderect(cashRect):
                    money += 100
                    money_collect.play()
                    print("Money: " + str(money))
                    # text = print_bar(money)
                    # display.blit(text, ((display.get_width() / 2 - text.get_rect().width / 2), (display.get_height() / 2 - 90)))

                    index = layer.index(tile)
                    layer[index] = '0'
                    b = True
                display.blit(cash, (x * 16 - int(scroll[0]), y * 16 - int(scroll[1])))

            if tile != '0' and tile != '$' and tile != '4' and tile != '3' and tile != '5' and tile != '7' and tile != '8' and tile != '2':
                #if tile == '4':
                #    tile_rects.append(pygame.Rect( x * 16 - int(scroll[0]) + 7, y * 16 - int(scroll[1]), 1, 16))
                #else:
                tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
                    #tile_rects.append(pygame.Rect( x * 16 - int(scroll[0]) + 7, y * 16 - int(scroll[1]), 1, 16))
            x += 1
        y += 1

    text = font.render("BALANCE: $ " + str(money), 0, (0, 0, 0))
    display.blit(text, (200, 10))
    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2

    if moving_left:
        player_movement[0] -= 2

    player_movement[1] += vertical_momentum
    vertical_momentum += 0.25
    if vertical_momentum > 3:
        vertical_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions["bottom"]:
        air_timer = 0
        vertical_momentum = 5
    else:
        air_timer += 1

    # display.blit(player_img, (player_rect.x - int(scroll[0]), player_rect.y - int(scroll[1])))

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()  # prevents Segmentation fault 11

        # Key press events & image changes
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
                to_left = False
                # player_img = player_walk

            if event.key == K_LEFT:
                moving_left = True
                to_left = True
                # player_img = mirror(player_walk)

            if event.key == K_SPACE:
                if air_timer < 6:
                    vertical_momentum = -5.5
                    jump = True
                # if to_left:
                # player_img = mirror(player_jump)
                # else:
                # player_img = player_jump

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
                to_left = False
                # player_img = player_stand
                walkCount = 0

            if event.key == K_LEFT:
                moving_left = False
                to_left = True
                # player_img = mirror(player_stand)
                walkCount = 0

            if event.key == K_SPACE:
                jump = False
                # if to_left:
                #    player_img = mirror(player_stand)
                # else:
                #    player_img = player_stand
                walkCount = 0

    redrawGameWindow()
    screen.blit(pygame.transform.scale(display, window_size), (0, 0))
    pygame.display.update()
    clock.tick(60)
