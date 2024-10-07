#Game!
import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() 

pygame.display.set_caption('Peli')


#Näytön asentaminen ja näytön koko
window_size = (800,500)

screen = pygame.display.set_mode(window_size,0,32)

display = pygame.Surface((800, 500))

load_img = pygame.image.load
#Kuvien lisääminen
player_png = load_img('Pelaaja.png')
player_png.set_colorkey((255,255,255))
palikka_png = load_img('Multa.png')
palikka2_png = load_img('Ruoho.png')

background_colour = (135, 206, 235)


def load_map(path):

    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

game_map = load_map('map1')
tile_size = 32

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

player_y_momentum = 0


moving_left = False
moving_right = False

player_rect = pygame.Rect(50,50,player_png.get_width(),player_png.get_height())


#Game loop

while True:

    display.fill(background_colour)

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(palikka_png, (x * tile_size, y * tile_size))
            if tile == '2':
                display.blit(palikka2_png, (x * tile_size, y * tile_size)) 
            if tile != '0':
                tile_rects.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
            x += 1         
        y += 1


    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3
    

    
    player_rect, collisions = move(player_rect, player_movement, tile_rects) 
    display.blit(player_png, (player_rect.x, player_rect.y))
   
    # if moving_right == True:
    #     player_location[0] += 4
    # if moving_left == True:
    #     player_location[0] -= 4
    
    # player_rect.x = player_location[0]
    # player_rect.y = player_location[1]
    
    #Bouncy screen bottom
    # if player_location[1] > window_size[1]-player_png.get_height():
    #     player_y_momentum = -player_y_momentum
    # else:
    #     player_y_momentum += 0.2
    # player_location[1] += player_y_momentum

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_SPACE:
                    player_y_momentum = -5
        if event.type == pygame.KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False


    surf = pygame.transform.scale(display, window_size)
    screen.blit(surf, (0,0))
    pygame.display.update()
    #60 Fps
    clock.tick(60)