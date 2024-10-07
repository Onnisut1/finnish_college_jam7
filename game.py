#Game!
import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() 

pygame.display.set_caption('Peli')


#Näytön asentaminen ja näytön koko
window_size = (800,400)

screen = pygame.display.set_mode(window_size,0,32)

#Kuvien lisääminen
player_png = pygame.image.load('Pelaaja.png')

background_colour = (135, 206, 235)


player_location = [50,300]
player_y_momentum = 0


moving_left = False
moving_right = False

player_rect = pygame.Rect(player_location[0],player_location[1],player_png.get_width(),player_png.get_height())


#Game loop

while True:

    screen.fill(background_colour)
    screen.blit(player_png, player_location)


    if moving_right == True:
        player_location[0] += 4
    if moving_left == True:
        player_location[0] -= 4

    if player_location[1] > window_size[1]-player_png.get_height():
        player_y_momentum = -player_y_momentum
    else:
        player_y_momentum += 0.2
    player_location[1] += player_y_momentum

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

    pygame.display.update()
    #60 Fps
    clock.tick(60)