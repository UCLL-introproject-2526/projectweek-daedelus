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

LEVEL_X = 450
LEVEL_Y_START = 260
LEVEL_SPACING = 50

BG_SPEED = 300
WAVE_SPEED = 0
PILLAR_SPEED = 300

MAX_LIVES = 3
lives = 3

HIT_COOLDOWN = 1.2
hit_timer = 0

LEVEL_SCORE_LIMIT = None

# Vogel
BIRD_SPEED = 0
BIRD_SPAWN_TIME = 2.0
BIRD_ANIM_SPEED = 0.15

# Sun
SUN_HEIGHT = 100
SUN_DAMAGE_Y = UI_BAR
SUN_TOLERANCE = 25  # hoeveel pixels je mag "indringen" zonder damage

# Booster
INVINCIBILITY_DURATION = 5.0
invincible_timer = 0
SHIELD_WARNING_TIME = 1.0

# Levels

LEVEL_INTRO = {
    "BG_SPEED": 250,
    "PILLAR_SPEED": 250,
    "BIRD_SPAWN": 3.0,
    "PILLAR_SPAWN": 2,
    "POWERUP_SPAWN": 12.0,
    "SCORE_LIMIT": 1000,
    "HEART_SPAWN_TIME": 3,
    "WAVE_SPEED" : 400,
    "BIRD_SPEED" : 400
}

LEVEL_EASY = {
    "BG_SPEED": 400,
    "PILLAR_SPEED": 400,
    "BIRD_SPAWN": 1.3,
    "PILLAR_SPAWN": 1.7,
    "POWERUP_SPAWN": 15.0,
    "SCORE_LIMIT": 2000,
    "HEART_SPAWN_TIME": 10,
    "WAVE_SPEED" : 600,
    "BIRD_SPEED" : 600
}

LEVEL_MEDIUM = {
    "BG_SPEED": 550,
    "PILLAR_SPEED": 550,
    "BIRD_SPAWN": 0.7,
    "PILLAR_SPAWN": 1,
    "POWERUP_SPAWN": 20.0,
    "SCORE_LIMIT": 3000,
    "HEART_SPAWN_TIME": 25,
    "WAVE_SPEED" : 800,
    "BIRD_SPEED" : 800
}

LEVEL_IMPOSSIBLE = {
    "BG_SPEED": 700,
    "PILLAR_SPEED": 700,
    "BIRD_SPAWN": 0.4,
    "PILLAR_SPAWN": 0.7,
    "POWERUP_SPAWN": 20,
    "SCORE_LIMIT": None,
    "HEART_SPAWN_TIME": 15,
    "WAVE_SPEED" : 1000,
    "BIRD_SPEED" : 1000
}

# ========================
# SETUP
# ========================
Level_Shown = None
Game_level1 = "1 - Intro"
Game_level2 = "2 - Easy"
Game_level3 ="3 - Medium"
Game_level4 ="4 - Impossible"
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Flight of Icarus')
clock = pygame.time.Clock()
running = True
dt = 0
score = 0
music_started = False        #muziek begint enkel bij player input in de browser

# ========================
# GAME STATES
# ========================
LEVEL_SELECT = 0
PLAYING = 1
GAME_OVER = 2
LEVEL_COMPLETED = 3

game_over_timer = 0

state = LEVEL_SELECT
current_level = None
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

icarus_corner = pygame.image.load("Sprites/icarus25.png").convert_alpha()
icarus_corner = pygame.transform.scale_by(icarus_corner, 0.2)  # pas schaal aan indien nodig
icarus_corner_rect = icarus_corner.get_rect(
    topleft=(10, 10)
)

heart_image = pygame.image.load('Sprites/heart.png').convert_alpha()
heart_mask = pygame.mask.from_surface(heart_image)

icarus = pygame.image.load('Sprites/icarus_sprite.png').convert_alpha()
icarus_rect = icarus.get_rect(midleft=(0, WINDOW_HEIGHT / 2))
icarus_mask = pygame.mask.from_surface(icarus)

icarus_shielded = pygame.image.load("Sprites/Icarus_shielded.png").convert_alpha()
icarus_shielded = pygame.transform.scale(icarus_shielded, icarus.get_size())

icarus_2hearts = pygame.image.load("Sprites/2_heart_Icarus.png").convert_alpha()
icarus_2hearts_mask = pygame.mask.from_surface(icarus_2hearts)

icarus_1heart = pygame.image.load("Sprites/1_heart_Icarus.png").convert_alpha()
icarus_1heart_mask = pygame.mask.from_surface(icarus_1heart)

icarus_2hearts_shielded = pygame.image.load("Sprites/2_heart_Icarus_shielded.png").convert_alpha()
icarus_2hearts_shielded_mask = pygame.mask.from_surface(icarus_2hearts)

icarus_1heart_shielded = pygame.image.load("Sprites/1_heart_Icarus_shielded.png").convert_alpha()
icarus_1heart_shielded_mask = pygame.mask.from_surface(icarus_1heart)

game_over_img = pygame.image.load("Sprites/game_over3.png").convert_alpha()
game_over_img = pygame.transform.scale(game_over_img, (600, 200))

sun_surface = pygame.Surface((WINDOW_WIDTH, SUN_HEIGHT), pygame.SRCALPHA)
sun_surface.fill((255, 200, 0, 180))  # zelfde kleur als glow
sun_mask = pygame.mask.from_surface(sun_surface)

powerup_image = pygame.image.load("Sprites/Shield.png").convert_alpha()
powerup_mask = pygame.mask.from_surface(powerup_image)

SCALE = 0.5  # kleiner = 0.6, groter = 0.8

level_intro_img = pygame.transform.scale_by(
    pygame.image.load("Sprites/intro1.png").convert_alpha(), SCALE
)
level_easy_img = pygame.transform.scale_by(
    pygame.image.load("Sprites/easy2.png").convert_alpha(), SCALE
)
level_medium_img = pygame.transform.scale_by(
    pygame.image.load("Sprites/meduim3.png").convert_alpha(), SCALE
)
level_impossible_img = pygame.transform.scale_by(
    pygame.image.load("Sprites/impossible4.png").convert_alpha(), SCALE
)

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

powerups = []
powerup_speed = 200
powerup_spawn_time = 15
powerup_timer = 0
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
    if lives <= 0:
        game_over()

    return False

def check_sun_collision():
    penetration = (UI_BAR + SUN_HEIGHT) - icarus_rect.top
    if lives <= 0:
                    game_over()
    return penetration > SUN_TOLERANCE
    


def spawn_heart():
    heart_rect = heart_image.get_rect(
        midleft=(WINDOW_WIDTH + 50, randrange(75, WINDOW_HEIGHT - 100))
    )
    hearts.append(heart_rect)

class SoundLibrary:
    def __init__(self):
        heart_sound = pygame.mixer.Sound("Sound/Soundeffect/Heart.ogg")
        heart_sound.set_volume(1.0)
        
        splash_sound = pygame.mixer.Sound("Sound/Soundeffect/Splash.ogg")
        splash_sound.set_volume(1.0)

        oof_sound = pygame.mixer.Sound("Sound/Soundeffect/Oof.ogg")
        oof_sound.set_volume(0.4)

        hit_sound = pygame.mixer.Sound("Sound\Soundeffect\Hit.ogg")
        hit_sound.set_volume(1.0)

        bird_sound = pygame.mixer.Sound("Sound/Soundeffect/Bird.ogg")
        bird_sound.set_volume(1.0)

        powerup_sound = pygame.mixer.Sound("Sound/Soundeffect/Powerup.ogg")
        powerup_sound.set_volume(1.0)

        sun_sound = pygame.mixer.Sound("Sound\Soundeffect\Sun_damage.ogg")
        sun_sound.set_volume(0.3)


        self.sounds = {
            "heart": heart_sound,
            "splash": splash_sound,
            "oof": oof_sound, 
            "hit": hit_sound,
            "bird": bird_sound,
            "powerup": powerup_sound,
            "sun": sun_sound
            
            
        }
        
    def play(self, sound_id):
        if sound_id in self.sounds:
            self.sounds[sound_id].play()

sound_library = SoundLibrary()

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

def spawn_powerup():
    rect = powerup_image.get_rect(
        midleft=(WINDOW_WIDTH + 50, randrange(UI_BAR + 60, WINDOW_HEIGHT - 120))
    )
    powerups.append(rect)

def update_powerups():
    global invincible_timer

    for p in powerups[:]:
        p.x -= powerup_speed * dt

        if p.right < 0:
            powerups.remove(p)
            continue

        offset_x = p.x - icarus_rect.x
        offset_y = p.y - icarus_rect.y

        if icarus_mask.overlap(powerup_mask, (offset_x, offset_y)):
            sound_library.play("powerup")
            invincible_timer = INVINCIBILITY_DURATION
            powerups.remove(p)
            continue

        screen.blit(powerup_image, p)

def load_level():
    infinite_background()
    infinite_waves()

    draw_sun_glow()

    update_powerups()

    for pillar in pillars:
        pillar.draw()

    # Bepaal welke Icarus sprite getoond moet worden
    if invincible_timer > 0:
        # Laatste seconde → flikkeren
        if invincible_timer <= SHIELD_WARNING_TIME:
            if int(invincible_timer * 10) % 2 == 0:
                if lives == 2:
                    screen.blit(icarus_2hearts_shielded, icarus_rect)
                elif lives == 1:
                    screen.blit(icarus_1heart_shielded, icarus_rect)
                else:
                    screen.blit(icarus_shielded, icarus_rect)
        else:
            if lives == 2:
                screen.blit(icarus_2hearts_shielded, icarus_rect)
            elif lives == 1:
                screen.blit(icarus_1heart_shielded, icarus_rect)
            else:
                screen.blit(icarus_shielded, icarus_rect)
    else:
        # normale hit-knipper
        if hit_timer <= 0 or int(hit_timer * 10) % 2 == 0:
            if lives == 2:
                screen.blit(icarus_2hearts, icarus_rect)
            elif lives == 1:
                screen.blit(icarus_1heart, icarus_rect)
            else:
                screen.blit(icarus, icarus_rect)




    screen.blit(Ui, (0, 0))
    Level_Ui = font.render(Level_Shown, True, (255,255,255), )

    score_text = score_font.render(f"Score: {int(score)}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(Level_Ui, (WINDOW_WIDTH/2 - 100, 10))


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
    global bird_spawn_timer, bird_anim_timer, bird_frame_index, heart_timer, score, pillar_timer, powerup_timer, invincible_timer
    bird_spawn_timer = 0
    bird_anim_timer = 0
    bird_frame_index = 0
    heart_timer = 0
    score = 0
    BG_SPEED = 300
    pillar_timer = 0
    invincible_timer = 0
    powerup_timer = 0

    pillars.clear()
    hearts.clear() #toegevoegd
    birds.clear() #toegevoegd
    powerups.clear()
    icarus_rect.midleft = (80, UI_BAR + (WINDOW_HEIGHT - UI_BAR) // 2)

def spawn_bird():
    y = randrange(60, WINDOW_HEIGHT - 120)  # nooit in zee
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

        if hit_timer <= 0 and invincible_timer <= 0:
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


def draw_game_over():
    global game_over_timer
    game_over_timer += dt

    # achtergrond
    infinite_background()
    infinite_waves()

    # fade overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    alpha = min(180, int(game_over_timer * 120))
    overlay.set_alpha(alpha)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    center_x = WINDOW_WIDTH // 2

    # 🟥 GAME OVER komt van boven
    if game_over_timer > 0.4:
        t = min(1, (game_over_timer - 0.4) / 0.8)
        y = -200 + t * 320
        go_rect = game_over_img.get_rect(center=(center_x, y))
        screen.blit(game_over_img, go_rect)

    # 🟨 Score
    if game_over_timer > 1.5:
        score_surf = font.render(f"Score: {int(score)}", True, (255, 255, 255))
        screen.blit(score_surf, (center_x - score_surf.get_width() // 2, 260))

    # 🟨 Record
    if game_over_timer > 2.0:
        record_surf = font.render(f"Record: {record}", True, (255, 215, 0))
        screen.blit(record_surf, (center_x - record_surf.get_width() // 2, 300))

    # 🟩 Knipperende instructie (arcade-style)
    if game_over_timer > 2.6:
        if int(game_over_timer * 2) % 2 == 0:
            info = font.render(
                "Press SPACE to Retry or ESC to Exit",
                True,
                (200, 200, 200)
            )
            screen.blit(info, (center_x - info.get_width() // 2, 360))

def game_over():
    global state, record, game_over_timer
    if score > record:
        record = int(score)
    game_over_timer = 0
    state = GAME_OVER

def draw_level_select():
    infinite_background()
    infinite_waves()

    screen.blit(font.render("Flight of Icarus", True, (212, 175, 55)),(LEVEL_X, LEVEL_Y_START - 100))
    screen.blit(font.render("Kies een level:", True, (255,255,255)), (LEVEL_X, LEVEL_Y_START - 50))
    screen.blit(level_intro_img, (LEVEL_X, LEVEL_Y_START))
    screen.blit(level_easy_img, (LEVEL_X, LEVEL_Y_START + LEVEL_SPACING))
    screen.blit(level_medium_img, (LEVEL_X, LEVEL_Y_START + LEVEL_SPACING * 2))
    screen.blit(level_impossible_img, (LEVEL_X, LEVEL_Y_START + LEVEL_SPACING * 3))
    
    screen.blit(icarus_corner, icarus_corner_rect)

def draw_level_completed():
    infinite_background()
    infinite_waves()
    screen.blit(
        font.render("Level Completed!", True, (212, 175, 55)),
        (WINDOW_WIDTH // 2 - 120, 180)
    )
    screen.blit(
        font.render(f"Score: {int(score)}", True, (255, 255, 255)),
        (WINDOW_WIDTH // 2 - 80, 240)
    )
    screen.blit(
        font.render("Press ESC for Exit or SPACE for Next Level", True, (255, 255, 255)),
        (50, 300)
    )

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


        if state == LEVEL_SELECT and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_level = LEVEL_INTRO
                Level_Shown = Game_level1

            if event.key == pygame.K_2:
                current_level = LEVEL_EASY
                Level_Shown = Game_level2

            if event.key == pygame.K_3:
                current_level = LEVEL_MEDIUM
                Level_Shown = Game_level3

            if event.key == pygame.K_4:
                current_level = LEVEL_IMPOSSIBLE
                Level_Shown = Game_level4

            if current_level:
                BG_SPEED = current_level["BG_SPEED"]
                PILLAR_SPEED = current_level["PILLAR_SPEED"]
                BIRD_SPAWN_TIME = current_level["BIRD_SPAWN"]
                PILLAR_SPAWN_TIME = current_level["PILLAR_SPAWN"]
                powerup_spawn_time = current_level["POWERUP_SPAWN"]
                LEVEL_SCORE_LIMIT = current_level["SCORE_LIMIT"]
                heart_spawn_time = current_level["HEART_SPAWN_TIME"]
                BIRD_SPEED = current_level["BIRD_SPEED"]
                WAVE_SPEED = current_level["WAVE_SPEED"]

                lives = MAX_LIVES
                score = 0
                reset_game()
                #heart_timer = powerup_spawn_time / 2 - 5
                #powerup_timer = powerup_spawn_time / 2
                state = PLAYING

        if state == LEVEL_COMPLETED and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Exit
                state = LEVEL_SELECT
                current_level = None
            if event.key == pygame.K_SPACE:  # Next level
                if Level_Shown == Game_level1:
                    current_level = LEVEL_EASY
                    Level_Shown = Game_level2
                elif Level_Shown == Game_level2:
                    current_level = LEVEL_MEDIUM
                    Level_Shown = Game_level3
                elif Level_Shown == Game_level3:
                    current_level = LEVEL_IMPOSSIBLE
                    Level_Shown = Game_level4
                else:
                    state = LEVEL_SELECT
                    current_level = None
                if current_level:
                    BG_SPEED = current_level["BG_SPEED"]
                    PILLAR_SPEED = current_level["PILLAR_SPEED"]
                    BIRD_SPAWN_TIME = current_level["BIRD_SPAWN"]
                    PILLAR_SPAWN_TIME = current_level["PILLAR_SPAWN"]
                    powerup_spawn_time = current_level["POWERUP_SPAWN"]
                    LEVEL_SCORE_LIMIT = current_level["SCORE_LIMIT"]
                    BIRD_SPEED = current_level["BIRD_SPEED"]
                    WAVE_SPEED = current_level["WAVE_SPEED"]
                    lives = MAX_LIVES
                    reset_game()
                    state = PLAYING


        if state == GAME_OVER and event.type == pygame.KEYDOWN and game_over_timer > 2.6:
            if event.key == pygame.K_SPACE:
                reset_game()
                lives = MAX_LIVES
                state = PLAYING
            if event.key == pygame.K_ESCAPE:
                state = LEVEL_SELECT
                current_level = None


    if state == LEVEL_SELECT:
        draw_level_select()
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        continue

    if state == GAME_OVER:
        draw_game_over()
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        continue

    if state == LEVEL_COMPLETED:
        draw_level_completed()
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        continue


    handle_keys()

    powerup_timer += dt
    if powerup_timer >= powerup_spawn_time:
        spawn_powerup()
        powerup_timer = 0
    
    pillar_timer += dt
    if pillar_timer >= PILLAR_SPAWN_TIME:
        gap = max(95, 180 - score * 0.15)
        pillars.append(PillarPair(WINDOW_WIDTH + 100, gap))
        pillar_timer = 0

    # ⬇️ ELKE FRAME
    for pillar in pillars:
        pillar.update()

        if pillar.collides(icarus_rect) and hit_timer <= 0 and invincible_timer <= 0:
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

    if check_sun_collision() and hit_timer <= 0 and invincible_timer <= 0:

        lives -= 1
        hit_timer = HIT_COOLDOWN 
        sound_library.play("oof")
        sound_library.play("sun")

    # zee raakt → 1 leven verliezen
    if check_wave_collision() and hit_timer <= 0 and invincible_timer <= 0:
        lives -= 1
        hit_timer = HIT_COOLDOWN
        sound_library.play("splash")
        sound_library.play("oof")

        if lives <= 0:
            # update record als nodig
            if score > record:
                game_over()

    score += dt * 20
    if LEVEL_SCORE_LIMIT is not None and score >= LEVEL_SCORE_LIMIT:
        state = LEVEL_COMPLETED

    heart_timer += dt
    if heart_timer >= heart_spawn_time:
        spawn_heart()
        heart_timer = 0

    update_hearts()

    if invincible_timer > 0:
        invincible_timer -= dt

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()