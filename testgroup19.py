import pygame
from random import randrange

pygame.init()
pygame.mixer.init()

# ========================
# CONSTANTEN
# ========================
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
UI_BAR = 50

BG_SPEED = 300
WAVE_SPEED = 200

MAX_LIVES = 3
lives = 3

HIT_COOLDOWN = 1.2
hit_timer = 0

# Vogel
BIRD_SPEED = 250
BIRD_SPAWN_TIME = 2.0
BIRD_ANIM_SPEED = 0.15

# ========================
# SETUP
# ========================
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("bang bang")
clock = pygame.time.Clock()
running = True
dt = 0
score = 0

# ========================
# MUSIC
# ========================
pygame.mixer.music.load("Sound/Music/2.ogg")
pygame.mixer.music.play(-1)

# ========================
# FONTS & IMAGES
# ========================
score_font = pygame.font.Font("fonts/Cinzel-VariableFont_wght.ttf", 24)
font = pygame.font.Font("fonts/Cinzel-VariableFont_wght.ttf", 30)

Ui = pygame.image.load("Sprites/UI.png").convert_alpha()
background = pygame.image.load("Sprites/background.png").convert()
background = pygame.transform.scale(
    background, (WINDOW_WIDTH, WINDOW_HEIGHT + UI_BAR)
)

waves = pygame.image.load("Sprites/waves.png").convert_alpha()
waves = pygame.transform.scale(waves, (WINDOW_WIDTH, WINDOW_HEIGHT // 4))
waves_mask = pygame.mask.from_surface(waves)

heart_image = pygame.image.load("Sprites/heart.png").convert_alpha()

icarus = pygame.image.load("Sprites/icarus_sprite.png").convert_alpha()
icarus_rect = icarus.get_rect(midleft=(50, WINDOW_HEIGHT // 2))
icarus_mask = pygame.mask.from_surface(icarus)

# ========================
# VOGEL FRAMES (GESCHAALD)
# ========================
bird_frames = []
for img in [
    "Sprites/game158.png",
    "Sprites/Schermafbeelding 2025-12-16 141211game.png",
]:
    image = pygame.image.load(img).convert_alpha()
    image = pygame.transform.scale(
        image, (image.get_width() // 2, image.get_height() // 2)
    )
    bird_frames.append(image)

bird_masks = [pygame.mask.from_surface(f) for f in bird_frames]

birds = []
bird_spawn_timer = 0
bird_anim_timer = 0
bird_frame_index = 0

# ========================
# TEKST
# ========================
text_surface = font.render(
    "The sea waits below. The sun burns above.",
    True,
    (212, 175, 55),
)
text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 100))

# ========================
# BACKGROUND VARS
# ========================
bg_x = 0
waves_x = 0

# ========================
# FUNCTIES
# ========================
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
    screen.blit(waves, (waves_x, WINDOW_HEIGHT - 100))
    screen.blit(waves, (waves_x + WINDOW_WIDTH, WINDOW_HEIGHT - 100))


def spawn_bird():
    y = randrange(60, WINDOW_HEIGHT - 180)  # nooit in zee
    rect = bird_frames[0].get_rect(midleft=(WINDOW_WIDTH + 50, y))
    birds.append(rect)


def update_birds():
    global lives, hit_timer

    for bird in birds[:]:
        bird.x -= BIRD_SPEED * dt

        if bird.right < 0:
            birds.remove(bird)
            continue

        offset_x = bird.x - icarus_rect.x
        offset_y = bird.y - icarus_rect.y

        if hit_timer <= 0:
            if icarus_mask.overlap(
                bird_masks[bird_frame_index], (offset_x, offset_y)
            ):
                lives -= 1
                hit_timer = HIT_COOLDOWN
                birds.remove(bird)

        screen.blit(bird_frames[bird_frame_index], bird)


def draw_lives():
    for i in range(lives):
        screen.blit(heart_image, (20 + i * 40, 10))


def load_level():
    infinite_background()
    infinite_waves()

    screen.blit(text_surface, text_rect)

    # knipperen bij hit
    if hit_timer <= 0 or int(hit_timer * 10) % 2 == 0:
        screen.blit(icarus, icarus_rect)

    screen.blit(Ui, (0, 0))
    draw_lives()

    score_text = score_font.render(
        f"Score: {int(score)}", True, (255, 255, 255)
    )
    screen.blit(score_text, (10, 40))


# ========================
# MAIN LOOP
# ========================
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_keys()

    if hit_timer > 0:
        hit_timer -= dt

    bird_spawn_timer += dt
    if bird_spawn_timer >= BIRD_SPAWN_TIME:
        spawn_bird()
        bird_spawn_timer = 0

    bird_anim_timer += dt
    if bird_anim_timer >= BIRD_ANIM_SPEED:
        bird_anim_timer = 0
        bird_frame_index = (bird_frame_index + 1) % len(bird_frames)

    load_level()
    update_birds()

    score += dt * 20

    if lives <= 0:
        running = False

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
