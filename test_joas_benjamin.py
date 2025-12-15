import pygame


screen_size = (1024, 768)

pygame.display.set_mode(screen_size)
# Initialize Pygame
pygame.init()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
GGGG