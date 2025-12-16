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
# GAME STATES (NIEUW)
# ========================
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAMEOVER = "gameover"

game_state = STATE_MENU

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
icarus_rect = icarus.get_rect(midleft=(80, WINDOW_HEIGHT / 2))
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

# ========================
# PILLARS
# ========================
pillar_img = pygame.image.load("Sprites/zuilen.png").convert_alpha()
pillar_img = pygame.transform.scale(pillar_img, (70, 450))
pillar_img_flipped = pygame.transform.flip(pillar_img, False, True)
PILLAR_WIDTH = pillar_img.get_width()

pillars = []
pillar_timer = 0

# ========================
# FUNCTIES (ONGEWJZIGD)
# ========================
def handle_keys():
    keys = pygame.key.get_pressed()
    speed = 300 * dt

    if keys[pygame.K_UP] and icarus_rect.top > UI_BAR:
        icarus_rect.y -= speed
    if keys[pygame.K_DOWN] and icarus_rect.bottom < WINDOW_HEIGHT - 100:
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
    offset_x = waves_x - icarus_rect.x
    offset_y = wave_y - icarus_rect.y
    return icarus_mask.overlap(waves_mask, (offset_x, offset_y))


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

        self.hitbox_top = pygame.Rect(self.top_rect.inflate(-20, -80))
        self.hitbox_bottom = pygame.Rect(self.bottom_rect.inflate(-20, -80))

    def update(self):
        self.x -= PILLAR_SPEED * dt
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
        self.hitbox_top.x = self.x
        self.hitbox_bottom.x = self.x

    def draw(self):
        screen.blit(pillar_img_flipped, self.top_rect)
        screen.blit(pillar_img, self.bottom_rect)

    def collides(self, rect):
        return self.hitbox_top.colliderect(rect) or self.hitbox_bottom.colliderect(rect)


def reset_game():
    global score, lives, hit_timer, pillar_timer, game_state
    score = 0
    lives = MAX_LIVES
    hit_timer = 0
    pillar_timer = 0
    pillars.clear()
    hearts.clear()
    icarus_rect.midleft = (80, WINDOW_HEIGHT // 2)
    game_state = STATE_PLAYING


# ========================
# START & END SCREENS (NIEUW)
# ========================
def draw_start_screen():
    screen.blit(background, (0, 0))
    title = font.render("ICARUS", True, (212, 175, 55))
    screen.blit(title, title.get_rect(center=(WINDOW_WIDTH // 2, 160)))
    info = score_font.render("Press SPACE to start", True, (255, 255, 255))
    screen.blit(info, info.get_rect(center=(WINDOW_WIDTH // 2, 260)))


def draw_game_over_screen():
    screen.blit(background, (0, 0))
    over = font.render("GAME OVER", True, (200, 50, 50))
    screen.blit(over, over.get_rect(center=(WINDOW_WIDTH // 2, 160)))
    final = score_font.render(f"Final Score: {int(score)}", True, (255, 255, 255))
    screen.blit(final, final.get_rect(center=(WINDOW_WIDTH // 2, 230)))
    retry = score_font.render("Press R to restart", True, (255, 255, 255))
    screen.blit(retry, retry.get_rect(center=(WINDOW_WIDTH // 2, 300)))


# ========================
# MAIN LOOP
# ========================
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == STATE_MENU:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game()

        elif game_state == STATE_GAMEOVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()

    if game_state == STATE_MENU:
        draw_start_screen()

    elif game_state == STATE_PLAYING:
        handle_keys()

        pillar_timer += dt
        if pillar_timer >= max(1.0, 1.8 - score * 0.01):
            gap = max(95, 180 - score * 0.15)
            pillars.append(PillarPair(WINDOW_WIDTH + 100, gap))
            pillar_timer = 0

        for pillar in pillars:
            pillar.update()
            if pillar.collides(icarus_rect):
                game_state = STATE_GAMEOVER

            if not pillar.passed and pillar.x + PILLAR_WIDTH < icarus_rect.x:
                pillar.passed = True
                score += 10

        pillars[:] = [p for p in pillars if p.x > -PILLAR_WIDTH]

        load_level()

        if hit_timer > 0:
            hit_timer -= dt

        if check_wave_collision() and hit_timer <= 0:
            lives -= 1
            hit_timer = HIT_COOLDOWN
            if lives <= 0:
                game_state = STATE_GAMEOVER

        score += dt * 20

        heart_timer += dt
        if heart_timer >= heart_spawn_time:
            spawn_heart()
            heart_timer = 0

        update_hearts()

    elif game_state == STATE_GAMEOVER:
        draw_game_over_screen()

    pygame.display.flip()

pygame.quit()
