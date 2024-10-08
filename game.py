#Game!
import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() 

pygame.display.set_caption('Peli')


window_size = (800,500)
screen = pygame.display.set_mode(window_size,0,32)
display = pygame.Surface((800, 500))

load_img = pygame.image.load
#Kuvien lisääminen
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

global animation_frames
animation_frames = {}

def load_animation(path, frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0 
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        aniamtion_image = pygame.image.load(img_loc).convert()
        aniamtion_image.set_colorkey((0,0,0))
        animation_frames[animation_frame_id] = aniamtion_image.copy()
        for i in range (frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data


def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0 
    return action_var, frame

animation_database = {}
#Load animations
animation_database['walk'] = load_animation('animations/walk',[7,7,7,7,7])
animation_database['idle'] = load_animation('animations/idle',[15,15])

player_action = 'idle'
player_frame = 0
player_flip = False

scroll = [0,0]

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
jump_counter = 0

moving_left = False
moving_right = False

player_rect = pygame.Rect(50,50,32,32)

#Game loop

while True:
    scroll[0] += (player_rect.x-scroll[0]-300)/20
    scroll[1] += (player_rect.y-scroll[1]-250)/20

    display.fill(background_colour)

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(palikka_png, (x * tile_size - scroll[0], y * tile_size - scroll[1]))
            if tile == '2':
                display.blit(palikka2_png, (x * tile_size - scroll[0], y * tile_size - scroll[1])) 
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
    if player_y_momentum > 4:
        player_y_momentum = 4

    if player_movement[0] > 0:
        player_action,player_frame = change_action(player_action, player_frame, 'walk')
        player_flip = False
    if player_movement[0] == 0:
        player_action,player_frame = change_action(player_action, player_frame, 'idle')        
    if player_movement[0] < 0:
        player_action,player_frame = change_action(player_action, player_frame, 'walk')
        player_flip = True
    
    
    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_image = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_image,player_flip,False), (player_rect.x-scroll[0], player_rect.y-scroll[1]))

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        jump_counter = 0

    if collisions['top']:
        player_y_momentum = 0

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
                if jump_counter < 2:
                    player_y_momentum = -5
                    jump_counter += 1
 
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