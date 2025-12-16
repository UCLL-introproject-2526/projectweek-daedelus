import pygame
import random
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
PILLAR_SPEED = 300

MAX_LIVES = 3
lives = 3

HIT_COOLDOWN = 1.2
hit_timer = 0

# ========================
# SETUP
# ========================
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('bang bang')
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
font = pygame.font.Font('fonts/Cinzel-VariableFont_wght.ttf', 30)

Ui = pygame.image.load("Sprites/UI.png").convert_alpha()
background = pygame.image.load("Sprites/background.png").convert()
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT + UI_BAR))

waves = pygame.image.load("Sprites/waves.png").convert_alpha()
waves = pygame.transform.scale(waves, (WINDOW_WIDTH, WINDOW_HEIGHT // 4))
waves_mask = pygame.mask.from_surface(waves)

heart_image = pygame.image.load('Sprites/heart.png').convert_alpha()
heart_mask = pygame.mask.from_surface(heart_image)

icarus = pygame.image.load('Sprites/icarus_sprite.png').convert_alpha()
icarus_rect = icarus.get_rect(midleft=(0, WINDOW_HEIGHT / 2))
icarus_mask = pygame.mask.from_surface(icarus)

# ========================
# TEKST
# ========================
text_surface = font.render(
    'The sea waits below. The sun burns above.',
    True,
    (212, 175, 55)
)
text_rect = text_surface.get_rect(center=(WINDOW_WIDTH / 2, 100))

# ========================
# BACKGROUND VARS
# ========================
bg_x = 0
waves_x = 0

# ========================
# HEART PICKUPS
# ========================
hearts = []
heart_speed = 200
heart_spawn_time = 2.5
heart_timer = 0

# Pillars
pillar_img = pygame.image.load("Sprites/zuilen.png").convert_alpha()
pillar_img = pygame.transform.scale(pillar_img, (70, 450))
pillar_img_flipped = pygame.transform.flip(pillar_img, False, True)
PILLAR_WIDTH = pillar_img.get_width()

pillars = []
pillar_timer = 0

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


def check_wave_collision():
    wave_y = WINDOW_HEIGHT - 100

    offset_x1 = waves_x - icarus_rect.x
    offset_y1 = wave_y - icarus_rect.y
    if icarus_mask.overlap(waves_mask, (offset_x1, offset_y1)):
        return True

    offset_x2 = (waves_x + WINDOW_WIDTH) - icarus_rect.x
    offset_y2 = wave_y - icarus_rect.y
    if icarus_mask.overlap(waves_mask, (offset_x2, offset_y2)):
        return True

    return False


def spawn_heart():
    heart_rect = heart_image.get_rect(
        midleft=(WINDOW_WIDTH + 50, randrange(50, WINDOW_HEIGHT - 200))
    )
    hearts.append(heart_rect)


def update_hearts():
    global lives

    for heart in hearts[:]:
        heart.x -= heart_speed * dt

        if heart.right < 0:
            hearts.remove(heart)
            continue

        offset_x = heart.x - icarus_rect.x
        offset_y = heart.y - icarus_rect.y

        if icarus_mask.overlap(heart_mask, (offset_x, offset_y)):
            hearts.remove(heart)

            if lives < MAX_LIVES:
                lives += 1

            continue

        screen.blit(heart_image, heart)


def draw_lives():
    for i in range(lives):
        screen.blit(heart_image, (WINDOW_WIDTH - 50 * (i + 1), 0))


def load_level():
    infinite_background()
    infinite_waves()
    screen.blit(text_surface, text_rect)

    for pillar in pillars:
        pillar.draw()

    # knipperen tijdens invincibility
    if hit_timer <= 0 or int(hit_timer * 10) % 2 == 0:
        screen.blit(icarus, icarus_rect)

    screen.blit(Ui, (0, 0))

    score_text = score_font.render(f"Score: {int(score)}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    draw_lives()

class PillarPair:
    def __init__(self, x, gap_height):
        self.x = x
        self.gap_y = random.randint(UI_BAR + 80, WINDOW_HEIGHT - 160)
        self.passed = False

        self.top_rect = pillar_img.get_rect(bottomleft=(x, self.gap_y))
        self.bottom_rect = pillar_img.get_rect(topleft=(x, self.gap_y + gap_height))

        self.SIDE_MARGIN = 18
        self.STONE_TOP = 40
        self.STONE_BOTTOM = 40

        self.top_hitbox = pygame.Rect(
            self.top_rect.x + self.SIDE_MARGIN,
            self.top_rect.y + self.STONE_TOP,
            self.top_rect.width - self.SIDE_MARGIN * 2,
            self.top_rect.height - self.STONE_TOP - self.STONE_BOTTOM
        )

        self.bottom_hitbox = pygame.Rect(
            self.bottom_rect.x + self.SIDE_MARGIN,
            self.bottom_rect.y + self.STONE_TOP,
            self.bottom_rect.width - self.SIDE_MARGIN * 2,
            self.bottom_rect.height - self.STONE_TOP - self.STONE_BOTTOM
        )

    def update(self):
        self.x -= PILLAR_SPEED * dt
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
        self.top_hitbox.x = self.x + self.SIDE_MARGIN
        self.bottom_hitbox.x = self.x + self.SIDE_MARGIN

    def draw(self):
        screen.blit(pillar_img_flipped, self.top_rect)
        screen.blit(pillar_img, self.bottom_rect)

    def collides(self, player_rect):
        return (
            self.top_hitbox.colliderect(player_rect)
            or self.bottom_hitbox.colliderect(player_rect)
        )
def reset_game():
    global score, BG_SPEED, pillar_timer
    score = 0
    BG_SPEED = 300
    pillar_timer = 1
    pillars.clear()
    icarus_rect.midleft = (80, UI_BAR + (WINDOW_HEIGHT - UI_BAR) // 2)

<<<<<<< Updated upstream
=======
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
                if lives <= 0: 
                 reset_game()
                hit_timer = HIT_COOLDOWN
                birds.remove(bird)

        screen.blit(bird_frames[bird_frame_index], bird)

>>>>>>> Stashed changes
# ========================
# MAIN LOOP
# ========================
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_keys()

    pillar_timer += dt
    if pillar_timer >= max(1.0, 1.8 - score * 0.01):
        gap = max(95, 180 - score * 0.15)
        pillars.append(PillarPair(WINDOW_WIDTH + 100, gap))
        pillar_timer = 0

    # ⬇️ ELKE FRAME
    for pillar in pillars:
        pillar.update()

        if pillar.collides(icarus_rect):
            reset_game()
            break

        if not pillar.passed and pillar.x + PILLAR_WIDTH < icarus_rect.x:
            pillar.passed = True
            score += 10


    pillars[:] = [p for p in pillars if p.x > -PILLAR_WIDTH]

    load_level()
    # hit cooldown
    if hit_timer > 0:
        hit_timer -= dt

    # zee raakt → 1 leven verliezen
    if check_wave_collision() and hit_timer <= 0:
        lives -= 1
        hit_timer = HIT_COOLDOWN

        if lives <= 0:
           reset_game()

    score += dt * 20

    heart_timer += dt
    if heart_timer >= heart_spawn_time:
        spawn_heart()
        heart_timer = 0

    update_hearts()

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
