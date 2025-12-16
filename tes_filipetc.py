import pygame

pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('bang bang')
clock = pygame.time.Clock()
running = True

dt = 0
#player_pos = pygame.Vector2(screen.get_width() /2, screen.get_height() /2)

downloaded_font = pygame.font.Font('fonts/Cinzel-VariableFont_wght.ttf', 30)
downloaded_font = downloaded_font.render('The sea waits below. The sun burns above.', True, (212, 175, 55), 'silver')
downloaded_font_rect = downloaded_font.get_rect()
downloaded_font_rect.center = (WINDOW_WIDTH/2, 100)
icarus = pygame.image.load('Sprites/icarus_sprite.png')
icarus_rect = icarus.get_rect()

icarus_rect.midleft = (0, WINDOW_HEIGHT / 2)
def keys():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and icarus_rect.y > 0:
        icarus_rect.y -= 300 * dt

    if keys[pygame.K_DOWN] and  icarus_rect.y < WINDOW_HEIGHT - 50:
        icarus_rect.y += 300 * dt

    if keys[pygame.K_LEFT] and icarus_rect.x > 0:
        icarus_rect.x -= 300 * dt

    if keys[pygame.K_RIGHT] and icarus_rect.x < WINDOW_WIDTH - 75:
        icarus_rect.x += 300 * dt
def load_level():
    screen.fill('silver')

    #pygame.draw.circle(screen, 'blue', player_pos, 40)

    screen.blit(downloaded_font, downloaded_font_rect)

    screen.blit(icarus, icarus_rect)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    load_level()
    keys()


    '''if pygame.mouse.get_pressed()[0]:
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            player_pos.x = pos[0]
            player_pos.y = pos[1]
    '''

    pygame.display.flip()

    dt = clock.tick(60) / 1000


    class Background:
        def __init__(self):
            self.__set_create_image()
            
        def __set_create_image(self):
            background = pygame.image.load('Sprites/background.png')
            screen.blit(background)
