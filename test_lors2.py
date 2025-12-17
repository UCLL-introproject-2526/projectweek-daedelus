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

# Vogel
BIRD_SPEED = 500
BIRD_SPAWN_TIME = 2.0
BIRD_ANIM_SPEED = 0.15

SUN_HEIGHT = 100
SUN_DAMAGE_Y = UI_BAR
SUN_TOLERANCE = 25  # hoeveel pixels je mag "indringen" zonder damage


# ========================
# SETUP
# ========================
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Flight of Icarus')
clock = pygame.time.Clock()
running = True
dt = 0
score = 0

# ========================
# GAME STATES
# ========================
START = 0
PLAYING = 1
GAME_OVER = 2

state = START
record = 0

# ========================
# MUSIC
# ========================
pygame.mixer.music.load("Sound/Music/2.ogg")
pygame.mixer.music.set_volume(0.3)
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

sun_surface = pygame.Surface((WINDOW_WIDTH, SUN_HEIGHT), pygame.SRCALPHA)
sun_surface.fill((255, 200, 0, 180))  # zelfde kleur als glow
sun_mask = pygame.mask.from_surface(sun_surface)


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
# TEKST 2
# ========================
title_text = font.render("BANG BANG", True, (212, 175, 55))
start_text = font.render("Druk op SPACE om te starten", True, (255, 255, 255))

game_over_text = font.render("GAME OVER", True, (200, 50, 50))
restart_text = font.render("SPACE = opnieuw spelen", True, (255, 255, 255))

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
heart_spawn_time = 5
heart_timer = 0

# Pillars
pillar_img = pygame.image.load("Sprites/zuilen.png").convert_alpha()
pillar_img = pygame.transform.scale(pillar_img, (70, 450))
pillar_img_flipped = pygame.transform.flip(pillar_img, False, True)
PILLAR_WIDTH = pillar_img.get_width()

pillars = []
pillar_timer = 0

# ========================
# VOGEL FRAMES (GESCHAALD)
# ========================
bird_frames = []
for img in [
    "Sprites/bird1.png",
    "Sprites/bird2.png",
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

def check_sun_collision():
    penetration = (UI_BAR + SUN_HEIGHT) - icarus_rect.top
    return penetration > SUN_TOLERANCE


def spawn_heart():
    heart_rect = heart_image.get_rect(
        midleft=(WINDOW_WIDTH + 50, randrange(75, WINDOW_HEIGHT - 100))
    )
    hearts.append(heart_rect)

    #------------------------------TEST SOUNDLIBRARY------------------------#

class SoundLibrary:
    def __init__(self):
        heart_sound = pygame.mixer.Sound("Sound/Soundeffect/Heart.ogg")
        heart_sound.set_volume(1.0)
        
        splash_sound = pygame.mixer.Sound("Sound/Soundeffect/Splash.ogg")
        splash_sound.set_volume(1.0)

        oof_sound = pygame.mixer.Sound("Sound/Soundeffect/Oof.ogg")
        oof_sound.set_volume(0.5)

        hit_sound = pygame.mixer.Sound("Sound\Soundeffect\Hit.ogg")
        hit_sound.set_volume(1.0)

        bird_sound = pygame.mixer.Sound("Sound/Soundeffect/Bird.ogg")
        bird_sound.set_volume(1.0)

        self.sounds = {
            "heart": heart_sound,
            "splash": splash_sound,
            "oof": oof_sound, 
            "hit": hit_sound,
            "bird": bird_sound
            
            
        }
        
    def play(self, sound_id):
        if sound_id in self.sounds:
            self.sounds[sound_id].play()

sound_library = SoundLibrary()


#------------------------------TEST SOUNDLIBRARY------------------------#



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

            sound_library.play("heart")

            if lives < MAX_LIVES:
                lives += 1

            continue

        screen.blit(heart_image, heart)

def draw_sun_glow():
    for y in range(SUN_HEIGHT):
        alpha = int(180 * (1 - y / SUN_HEIGHT))  # sterk bovenaan, zwakker naar beneden
        color = (255, 170, 0, alpha)  # oranje/geel
        glow_line = pygame.Surface((WINDOW_WIDTH, 1), pygame.SRCALPHA)
        glow_line.fill(color)
        screen.blit(glow_line, (0, SUN_DAMAGE_Y + y))

def draw_lives():
    for i in range(lives):
        screen.blit(heart_image, (WINDOW_WIDTH - 50 * (i + 1), 0))


def load_level():
    infinite_background()
    infinite_waves()

    draw_sun_glow()

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
    global bird_spawn_timer, bird_anim_timer, bird_frame_index, heart_timer
    bird_spawn_timer = 0
    bird_anim_timer = 0
    bird_frame_index = 0
    heart_timer = 0
    score = 0
    BG_SPEED = 300
    pillar_timer = 0
    pillars.clear()
    hearts.clear() #toegevoegd
    birds.clear() #toegevoegd
    icarus_rect.midleft = (80, UI_BAR + (WINDOW_HEIGHT - UI_BAR) // 2)

def spawn_bird():
    y = randrange(60, WINDOW_HEIGHT - 180)  # nooit in zee
    rect = bird_frames[0].get_rect(midleft=(WINDOW_WIDTH + 50, y))
    birds.append(rect)


def update_birds():
    global lives, hit_timer, state, record

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
                sound_library.play("bird")
                sound_library.play("oof")
                lives -= 1
                hit_timer = HIT_COOLDOWN
                birds.remove(bird)

                # 🛑 Check voor game over
                if lives <= 0:
                    game_over()

        screen.blit(bird_frames[bird_frame_index], bird)


def draw_start():
    infinite_background()
    infinite_waves()
    screen.blit(title_text, title_text.get_rect(center=(WINDOW_WIDTH // 2, 220)))
    screen.blit(start_text, start_text.get_rect(center=(WINDOW_WIDTH // 2, 270)))


def draw_game_over():
    infinite_background()
    infinite_waves()
    screen.blit(game_over_text, game_over_text.get_rect(center=(WINDOW_WIDTH // 2, 200)))
    screen.blit(
        font.render(f"Score: {int(score)}", True, (255, 255, 255)),
        (WINDOW_WIDTH // 2 - 80, 260),
    )
    screen.blit(
        font.render(f"Record: {record}", True, (255, 215, 0)),
        (WINDOW_WIDTH // 2 - 80, 300),
    )
    screen.blit(restart_text, restart_text.get_rect(center=(WINDOW_WIDTH // 2, 360)))

def game_over():
    global state, record
    if score > record:
        record = int(score)
    state = GAME_OVER


# ========================
# MAIN LOOP
# ========================
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not music_started: #|
            pygame.mixer.music.play(-1)                        #| start muziek pas na de input op browser ?
            music_started = True                               #|

        if state == START and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            reset_game()
            lives = MAX_LIVES
            state = PLAYING

        if state == GAME_OVER and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            reset_game()
            lives = MAX_LIVES
            state = PLAYING

    if state == START:
        draw_start()
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        continue

    if state == GAME_OVER:
        draw_game_over()
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        continue

    handle_keys()

    pillar_timer += dt
    if pillar_timer >= max(2, 1.8 - score * 0.01):
        gap = max(95, 180 - score * 0.15)
        pillars.append(PillarPair(WINDOW_WIDTH + 100, gap))
        pillar_timer = 0

    # ⬇️ ELKE FRAME
    for pillar in pillars:
        pillar.update()

        if pillar.collides(icarus_rect) and hit_timer <= 0:
            lives -= 1
            hit_timer = HIT_COOLDOWN
            sound_library.play("oof"),
            sound_library.play("hit")

            if lives <= 0:
                if score > record:
                    game_over()
            break

        if not pillar.passed and pillar.x + PILLAR_WIDTH < icarus_rect.x:
            pillar.passed = True
            score += 10


    pillars[:] = [p for p in pillars if p.x > -PILLAR_WIDTH]

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
    # hit cooldown
    if hit_timer > 0:
        hit_timer -= dt

    if check_sun_collision() and hit_timer <= 0:
        lives -= 1
        sound_library.play("oof")
        hit_timer = HIT_COOLDOWN 

    # zee raakt → 1 leven verliezen
    if check_wave_collision() and hit_timer <= 0:
        lives -= 1
        hit_timer = HIT_COOLDOWN
        sound_library.play("splash")
        sound_library.play("oof")

        if lives <= 0:
            # update record als nodig
            if score > record:
                game_over()


    score += dt * 20

    heart_timer += dt
    if heart_timer >= heart_spawn_time:
        spawn_heart()
        heart_timer = 0

    update_hearts()

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()