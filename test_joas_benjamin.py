import pygame
from random import randrange

pygame.init()

#Music
pygame.mixer.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
UI_BAR = 50
BG_SPEED = 300
WAVE_SPEED = 200

#Music 
pygame.mixer.music.load("music_testmap/2.ogg")
pygame.mixer.music.play(-1)

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
waves_mask = pygame.mask.from_surface(waves)
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
icarus_mask = pygame.mask.from_surface(icarus)


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

def check_wave_collision():
    # Y-positie van de waves (zoals je ze tekent)
    wave_y = WINDOW_HEIGHT - 100

    # Eerste wave
    offset_x1 = waves_x - icarus_rect.x
    offset_y1 = wave_y - icarus_rect.y

    if icarus_mask.overlap(waves_mask, (offset_x1, offset_y1)):
        print("💥 Icarus raakt de zee!")
        return True

    # Tweede wave (naadloze herhaling)
    offset_x2 = (waves_x + WINDOW_WIDTH) - icarus_rect.x
    offset_y2 = wave_y - icarus_rect.y

    if icarus_mask.overlap(waves_mask, (offset_x2, offset_y2)):
        print("💥 Icarus raakt de zee!")
        return True

    return False

    
def load_level():
    infinite_background()
    infinite_waves()
    screen.blit(text_surface, text_rect)
    screen.blit(icarus, icarus_rect)
    screen.blit(Ui, (0, 0))
    score_text = score_font.render(f"Score: {int(score)}", True, (255, 255, 255)).convert_alpha()
    score_text_rect = score_text.get_rect(midleft = (0 , UI_BAR/2))
    screen.blit(score_text, score_text_rect)    


heart_image = pygame.image.load('Sprites/heart.png').convert_alpha()
heart_mask = pygame.mask.from_surface(heart_image)

hearts = []

heart_speed = 200
heart_spawn_time = 1
heart_timer = 0

def spawn_heart():
    heart_rect = heart_image.get_rect(
        midleft=(WINDOW_WIDTH + 50, randrange(50, WINDOW_HEIGHT - 200))
    )
    hearts.append(heart_rect)

def update_hearts():
    for heart in hearts[:]:
        heart.x -= heart_speed * dt

        # Verwijder als buiten scherm
        if heart.right < 0:
            hearts.remove(heart)
            continue

        # OFFSET berekenen
        offset_x = heart.x - icarus_rect.x
        offset_y = heart.y - icarus_rect.y

        # Pixel-perfect collision
        if icarus_mask.overlap(heart_mask, (offset_x, offset_y)):
            hearts.remove(heart)
            print("Pixel-perfect heart collected!")
            continue

        screen.blit(heart_image, heart)



def check_heart_collision():
    global score  # tijdelijk voorbeeld

    for heart in hearts[:]:
        if icarus_rect.colliderect(heart):
            hearts.remove(heart)
            print("Heart collected!")
            score += 50  # placeholder




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_keys()
    load_level()
    if check_wave_collision():
        print("Pixel-perfect collision met waves!")
    # hier later: leven -= 1, respawn, game over, etc.

    if WAVE_SPEED <= 600:
        BG_SPEED += 0.002
        WAVE_SPEED += 0.1    
    score += dt*20

    heart_timer += dt
    if heart_timer >= heart_spawn_time:
        spawn_heart()
        heart_timer = 0

    update_hearts()

    if heart_speed < 400:
        heart_speed *= 1.0004
    score += dt*20   

    pygame.display.flip()
    dt = clock.tick(60) / 1000


pygame.quit()

