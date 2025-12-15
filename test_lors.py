import pygame


screen_size = (1024, 768)

screen = pygame.display.set_mode(screen_size)

pygame.display.set_caption("keys")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            print("A key was pressed")

    screen.fill(BLACK)

    pygame.draw.circle(
        screen,
        WHITE,
        (512, 384), 
        100,        
        3            
    )

    pygame.display.flip()

pygame.quit()