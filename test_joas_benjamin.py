import pygame

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
UI_BAR = 50
BG_SPEED = 300
WAVE_SPEED = 200


screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('bang bang')
clock = pygame.time.Clock()
running = True
dt = 0
score = 0
score_font = pygame.font.Font("fonts/Cinzel-VariableFont_wght.ttf", 24)
Ui = pygame.image.load("Sprites/UI.png").convert()
background = pygame.image.load("Sprites/background.png").convert()
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT+UI_BAR))
bg_x = 0 
waves = pygame.image.load("Sprites/waves.png").convert()
waves = pygame.transform.scale(waves, (WINDOW_WIDTH, WINDOW_HEIGHT/ 4))
waves_x = 0 

font = pygame.font.Font('fonts/Cinzel-VariableFont_wght.ttf', 30)
text_surface = font.render(
    'The sea waits below. The sun burns above.',
    True,
    (212, 175, 55)
)
text_rect = text_surface.get_rect(center=(WINDOW_WIDTH / 2, 100))


icarus = pygame.image.load('Sprites/icarus_sprite.png').convert_alpha()
icarus_rect = icarus.get_rect(midleft=(0, WINDOW_HEIGHT / 2))


def handle_keys():
    keys = pygame.key.get_pressed()
    speed = 300 * dt

    if keys[pygame.K_UP] and icarus_rect.top > UI_BAR:
        icarus_rect.y -= speed
    if keys[pygame.K_DOWN] and icarus_rect.bottom < WINDOW_HEIGHT:
        icarus_rect.y += speed
    if keys[pygame.K_LEFT] and icarus_rect.left > 0:
        icarus_rect.x -= speed
    if keys[pygame.K_RIGHT] and icarus_rect.right < WINDOW_WIDTH:
        icarus_rect.x += speed

def infinite_background():
    global bg_x  
    bg_x -= BG_SPEED * dt
    if bg_x <= -WINDOW_WIDTH:
        bg_x = 0
    screen.blit(background, (bg_x, 0))
    screen.blit(background, (bg_x + WINDOW_WIDTH, 0))
    
def infinite_waves():
    global waves_x  


    waves_x -= WAVE_SPEED * dt

    if waves_x <= -WINDOW_WIDTH:
        waves_x = 0
    screen.blit(waves, (waves_x, WINDOW_HEIGHT-100))
    screen.blit(waves, (waves_x + WINDOW_WIDTH, WINDOW_HEIGHT-100))
    
def load_level():
    infinite_background()
    infinite_waves()
    screen.blit(text_surface, text_rect)
    screen.blit(icarus, icarus_rect)
    screen.blit(Ui, (0, 0))
    score_text = score_font.render(f"Score: {int(score)}", True, (255, 255, 255)).convert_alpha()
    score_text_rect = score_text.get_rect(midleft = (0 , UI_BAR/2))
    screen.blit(score_text, score_text_rect)    


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_keys()
    load_level()
    if WAVE_SPEED <= 600:
        BG_SPEED += 0.2
        WAVE_SPEED += 0.1
    score += dt*20

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
