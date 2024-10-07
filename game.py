#Game!

import pygame 


#Näytön asentaminen ja näytön koko
screen = pygame.display.set_mode((800, 500))

clock = pygame.time.Clock()

background_colour = (135, 206, 235)

pygame.display.set_caption('Peli')
display = pygame.Surface((800,500))
screen.fill(background_colour)

#Päivittää näytön
pygame.display.flip()

running = True

#Game loop
while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #60 Fps
    clock.tick(60)