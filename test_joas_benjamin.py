import pygame
import random

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("bang bang")
clock = pygame.time.Clock()
running = True
dt = 0
score = 0

BG_SPEED = 300
WAVE_SPEED = 200
PILLAR_SPEED = 300

score_font = pygame.font.Font("fonts/Cinzel-VariableFont_wght.ttf", 24)
font = pygame.font.Font("fonts/Cinzel-VariableFont_wght.ttf", 30)

background = pygame.image.load("Sprites/background.png").convert()
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
bg_x = 0

waves = pygame.image.load("Sprites/waves.png").convert()
waves = pygame.transform.scale(waves, (WINDOW_WIDTH, WINDOW_HEIGHT // 4))
waves_x = 0

pillar_img = pygame.image.load("Sprites/zuilen.png").convert_alpha()
pillar_img = pygame.transform.scale(pillar_img, (70, 450))
pillar_img_flipped = pygame.transform.flip(pillar_img, False, True)
PILLAR_WIDTH = pillar_img.get_width()

icarus = pygame.image.load("Sprites/icarus_sprite.png").convert_alpha()
icarus_rect = icarus.get_rect(midleft=(80, WINDOW_HEIGHT // 2))

text_surface = font.render(
    "The sea waits below. The sun burns above.",
    True,
    (212, 175, 55)
)
text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 100))

pillars = []
pillar_timer = 0


def reset_game():
    global score, BG_SPEED, pillar_timer
    score = 0
    BG_SPEED = 300
    pillar_timer = 0
    pillars.clear()
    icarus_rect.midleft = (80, WINDOW_HEIGHT // 2)


def handle_keys():
    keys = pygame.key.get_pressed()
    speed = 300 * dt

    if keys[pygame.K_UP] and icarus_rect.top > 0:
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


class PillarPair:
    def __init__(self, x, gap_height):
        self.x = x
        self.gap_y = random.randint(120, WINDOW_HEIGHT - 200)
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


def load_level():
    infinite_background()
    infinite_waves()

    for pillar in pillars:
        pillar.draw()

    screen.blit(text_surface, text_rect)
    screen.blit(icarus, icarus_rect)

    score_text = score_font.render(f"Score: {int(score)}", True, (0, 0, 0))
    screen.blit(score_text, (20, 20))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000
    handle_keys()

    pillar_timer += dt
    spawn_time = max(1.0, 1.8 - score * 0.01)
    if pillar_timer >= spawn_time:
        gap = max(95, 180 - score * 0.15)
        pillars.append(PillarPair(WINDOW_WIDTH + 100, gap))
        pillar_timer = 0

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

    pillars[:] = [p for p in pillars if p.x > -PILLAR_WIDTH]

    load_level()
    pygame.display.flip()

pygame.quit()
