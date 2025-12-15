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
def flying():
    keys =pygame.key.get_pressed()
    if keys[pygame.K_d]:
        sprite_coord[0] += 1
    if keys[pygame.K_a]:
        sprite_coord[0] -= 1
    if keys[pygame.K_w]:
        sprite_coord[1] -= 1
    if keys[pygame.K_s]:
        sprite_coord[1] += 1
pygame.init()

run = True
while run:
    render_frame(surface, coord)
    surface.blit(icarus, sprite_coord)
    flying()
    clear_surface(surface)
    surface.blit(icarus, sprite_coord)
    
        
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

pygame.quit()
