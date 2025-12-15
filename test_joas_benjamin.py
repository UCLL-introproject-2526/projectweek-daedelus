import pygame
from pygame.display import *

whipe = (0,0,0)
screen_size = (1024, 768)
circle_speed = 0.3
surface = set_mode(screen_size)
coord = [50 , 150]
sprite_coord = [50 , 150]
icarus = pygame.image.load('icarus_sprite.png')

def render_sprite():
    icarus = pygame.image.load('icarus_sprite.png').convert_alpha()
    flip()
    
def render_frame(surface, coord):
    #circle = pygame.draw.circle(surface, (255,255,0), coord , 120 )
    flip()
def clear_surface(surface):
    surface.fill(whipe)
# Initialize Pygame
pygame.init()

run = True
while run:
    render_frame(surface, coord)
    clear_surface(surface)
    surface.blit(icarus, sprite_coord)
    if(pygame.key.get_focused('d'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
