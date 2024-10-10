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
platform_png = load_img('platform.png')
danger_png = load_img('danger.png')

background_colour = (128, 128, 128)


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
animation_database['walk'] = load_animation('animations/walk',[7,7,7])
animation_database['idle'] = load_animation('animations/idle',[15,15,15,15,15])
animation_database['fall'] = load_animation('animations/fall',[15,15,15,15,15,15,15,15,15])

player_action = 'idle'
player_frame = 0
player_flip = False

scroll = [0,0]

class danger_obj():
    def __init__(self, loc):
        self.loc = loc

    def render(self, surf, scroll):
        surf.blit(danger_png, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))

    def get_rect(self):
        return pygame.Rect(self.loc[0], self.loc[1], tile_size, tile_size)
    
    def collision_test(self, rect):
        danger_rect = self.get_rect()
        return danger_rect.colliderect(rect)

class falling_obj():
    def __init__(self, loc):
        self.original_loc = list(loc)  # Store original position
        self.loc = list(loc)  # Current position
        self.y_momentum = 0  # Initialize vertical momentum
        self.on_ground = False  # Track if the object is on the ground

    def update(self, tiles):
        # Apply gravity
        self.y_momentum += 0.2  # Gravity effect
        if self.y_momentum > 4:
            self.y_momentum = 4  # Terminal velocity

        # Move the object down
        movement = [0, self.y_momentum]
        rect = self.get_rect()
        rect, collisions = move(rect, movement, tiles)

        # Check for collisions with the ground
        if collisions['bottom']:
            self.on_ground = True
            self.y_momentum = 0  # Reset vertical momentum
            self.loc[1] = rect.top  # Ensure it doesn't penetrate the ground
        else:
            self.on_ground = False

        self.loc[0], self.loc[1] = rect.x, rect.y  # Update location

    def render(self, surf, scroll):
        surf.blit(palikka2_png, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))

    def get_rect(self):
        return pygame.Rect(self.loc[0], self.loc[1], tile_size, tile_size)

    def reset_position(self):
        self.loc = self.original_loc.copy()  # Reset position to original
        self.y_momentum = 0  # Reset momentum
    
    def collision_test(self, rect):
        falling_rect = self.get_rect()
        return falling_rect.colliderect(rect)



class border_obj():
    def __init__(self, loc):
        self.loc = loc

    def get_rect(self):
        return pygame.Rect(self.loc[0], self.loc[1], tile_size, tile_size)
    
    def collision_test(self, rect):
        border_rect = self.get_rect()
        return border_rect.colliderect(rect)


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
player_location = [180,180]

player_rect = pygame.Rect(player_location[0], player_location[1],32,32)

danger_objects = []
border_objects = []
falling_objects = []
y = 0
for row in game_map:
    x = 0
    for tile in row:
        if tile == '3':  # If the tile is a danger tile
            danger_objects.append(danger_obj((x * tile_size, y * tile_size)))
        if tile == '4':
            border_objects.append(border_obj((x * tile_size, y * tile_size)))
        if tile == '5':
            falling_objects.append(falling_obj((x * tile_size, y * tile_size)))
        x += 1         
    y += 1

#Game loop
while True:
    scroll[0] += (player_rect.x-scroll[0]-300)/20
    scroll[1] += (player_rect.y-scroll[1]-150)/20

    display.fill(background_colour)

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(palikka_png, (x * tile_size - scroll[0], y * tile_size - scroll[1]))
            if tile == '2':
                display.blit(platform_png, (x * tile_size - scroll[0], y * tile_size - scroll[1])) 
            if tile == '1' or tile == '2':
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
    
    for danger in danger_objects:
        danger.render(display, scroll) 
        if danger.collision_test(player_rect):
            player_rect.topleft = player_location
            player_y_momentum = 0

    for border in border_objects:
        # danger.render(display, scroll) ei renderöidä koska border on näkymätön
        if border.collision_test(player_rect):
            player_rect.topleft = player_location
            player_y_momentum = 0

    for falling in falling_objects:
        falling.update(tile_rects)
        falling.render(display, scroll) 
        if falling.collision_test(player_rect):
            player_rect.topleft = player_location
            player_y_momentum = 0
        if falling.on_ground:
            falling.reset_position()

            
    
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