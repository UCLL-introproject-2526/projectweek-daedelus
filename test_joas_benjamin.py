import pygame
import random
from random import randrange

pygame.init()
pygame.mixer.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
UI_BAR = 50

BG_SPEED = 300
WAVE_SPEED = 200
<<<<<<< HEAD
PILLAR_SPEED = 300
=======

#Music 
pygame.mixer.music.load("Sound/Music/2.ogg")
pygame.mixer.music.play(-1)
>>>>>>> b8984983bb64ed884dcbae5c8ada6c70561820c1

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("bang bang")
clock = pygame.time.Clock()
running = True
dt = 0
score = 0
<<<<<<< HEAD
=======
score_font = pygame.font.Font("fonts/Cinzel-VariableFont_wght.ttf", 24)
Ui = pygame.image.load("Sprites/UI.png").convert()
background = pygame.image.load("Sprites/background.png").convert()
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT+UI_BAR))
bg_x = 0 
waves = pygame.image.load("Sprites/waves.png").convert_alpha()
waves = pygame.transform.scale(waves, (WINDOW_WIDTH, WINDOW_HEIGHT/ 4))
waves_mask = pygame.mask.from_surface(waves)
waves_x = 0 
>>>>>>> fc16b972507b81eeb078b639c86e44306548c0b2

# Music
pygame.mixer.music.load("music_testmap/2.ogg")
pygame.mixer.music.play(-1)

# Fonts
score_font = pygame.font.Font("fonts/Cinzel-VariableFont_wght.ttf", 24)
font = pygame.font.Font("fonts/Cinzel-VariableFont_wght.ttf", 30)

# Background
Ui = pygame.image.load("Sprites/UI.png").convert_alpha()
background = pygame.image.load("Sprites/background.png").convert()
background = pygame.transform.scale(
    background, (WINDOW_WIDTH, WINDOW_HEIGHT - UI_BAR)
)
bg_x = 0

waves = pygame.image.load("Sprites/waves.png").convert()
waves = pygame.transform.scale(waves, (WINDOW_WIDTH, (WINDOW_HEIGHT - UI_BAR) // 4))
waves_x = 0

# Player
icarus = pygame.image.load("Sprites/icarus_sprite.png").convert_alpha()
icarus_rect = icarus.get_rect(midleft=(80, UI_BAR + (WINDOW_HEIGHT - UI_BAR) // 2))
icarus_mask = pygame.mask.from_surface(icarus)

# Pillars
pillar_img = pygame.image.load("Sprites/zuilen.png").convert_alpha()
pillar_img = pygame.transform.scale(pillar_img, (70, 450))
pillar_img_flipped = pygame.transform.flip(pillar_img, False, True)
PILLAR_WIDTH = pillar_img.get_width()

pillars = []
pillar_timer = 0

# Text
text_surface = font.render(
    "The sea waits below. The sun burns above.",
    True,
    (212, 175, 55)
)
text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, UI_BAR + 40))


def reset_game():
    global score, BG_SPEED, pillar_timer
    score = 0
    BG_SPEED = 300
    pillar_timer = 0
    pillars.clear()
    icarus_rect.midleft = (80, UI_BAR + (WINDOW_HEIGHT - UI_BAR) // 2)


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
    screen.blit(background, (bg_x, UI_BAR))
    screen.blit(background, (bg_x + WINDOW_WIDTH, UI_BAR))


def infinite_waves():
    global waves_x
    waves_x -= WAVE_SPEED * dt
    if waves_x <= -WINDOW_WIDTH:
        waves_x = 0
<<<<<<< HEAD
    y = WINDOW_HEIGHT - waves.get_height()
    screen.blit(waves, (waves_x, y))
    screen.blit(waves, (waves_x + WINDOW_WIDTH, y))
=======
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
>>>>>>> fc16b972507b81eeb078b639c86e44306548c0b2


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


# Hearts
heart_image = pygame.image.load("Sprites/heart.png").convert_alpha()
heart_mask = pygame.mask.from_surface(heart_image)
hearts = []
heart_speed = 200
heart_spawn_time = 0.1
heart_timer = 0


def spawn_heart():
    heart_rect = heart_image.get_rect(
<<<<<<< HEAD
        midleft=(WINDOW_WIDTH + 100, randrange(UI_BAR + 60, WINDOW_HEIGHT - 60))
=======
        midleft=(WINDOW_WIDTH + 50, randrange(50, WINDOW_HEIGHT - 200))
>>>>>>> fc16b972507b81eeb078b639c86e44306548c0b2
    )
    hearts.append(heart_rect)


def update_hearts():
    for heart in hearts[:]:
        heart.x -= heart_speed * dt
        if heart.right < 0:
            hearts.remove(heart)
            continue

        offset = (heart.x - icarus_rect.x, heart.y - icarus_rect.y)
        if icarus_mask.overlap(heart_mask, offset):
            hearts.remove(heart)
            continue

        screen.blit(heart_image, heart)


def load_level():
    infinite_background()
    infinite_waves()

    for pillar in pillars:
        pillar.draw()

    for heart in hearts:
        screen.blit(heart_image, heart)

    screen.blit(text_surface, text_rect)
    screen.blit(icarus, icarus_rect)
    screen.blit(Ui, (0, 0))

    score_text = score_font.render(f"Score: {int(score)}", True, (255, 255, 255))
    screen.blit(score_text, (10, UI_BAR // 2))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000
    handle_keys()
<<<<<<< HEAD

    pillar_timer += dt
    if pillar_timer >= max(1.0, 1.8 - score * 0.01):
        gap = max(95, 180 - score * 0.15)
        pillars.append(PillarPair(WINDOW_WIDTH + 100, gap))
        pillar_timer = 0
=======
    load_level()
    if check_wave_collision():
        print("Pixel-perfect collision met waves!")
    # hier later: leven -= 1, respawn, game over, etc.

    if WAVE_SPEED <= 600:
        BG_SPEED += 0.002
        WAVE_SPEED += 0.1    
    score += dt*20
>>>>>>> fc16b972507b81eeb078b639c86e44306548c0b2

    heart_timer += dt
    if heart_timer >= heart_spawn_time:
        spawn_heart()
        heart_timer = 0

    BG_SPEED *= 1.00015
    score += dt * 20

    for pillar in pillars:
        pillar.update()
        if pillar.collides(icarus_rect):
            reset_game()
            break
        if not pillar.passed and pillar.x + PILLAR_WIDTH < icarus_rect.x:
            pillar.passed = True
            score += 10

    update_hearts()
    pillars[:] = [p for p in pillars if p.x > -PILLAR_WIDTH]

    load_level()
    pygame.display.flip()

pygame.quit()
