import pygame
from pygame.display import *



screen_size = (1024, 768)

surface = set_mode(screen_size)

def render_frame(surface):
    circle = pygame.draw.circle(surface, (255,255,255), (500,370) , 12 )
    flip()
render_frame(surface)
    
# Initialize Pygame
pygame.init()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
<<<<<<< HEAD
<<<<<<< Updated upstream
GGGGezedzdz
kln
=======
GGGG
>>>>>>> Stashed changes
=======
>>>>>>> ba40145498c0cd1aba807d9ed0b71794d6a4f2e1
