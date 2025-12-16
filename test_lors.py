import pygame

pygame.init()
pygame.mixer.init()



WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500


BG_SPEED = 250

pygame.mixer.music.load("Sound/Music/2.ogg")
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('bang bang')
clock = pygame.time.Clock()
running = True
dt = 0


background = pygame.image.load("Sprites/background.png").convert()
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
bg_x = 0 


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

    if keys[pygame.K_UP] and icarus_rect.top > 0:
        icarus_rect.y -= speed
    if keys[pygame.K_DOWN] and icarus_rect.bottom < WINDOW_HEIGHT:
        icarus_rect.y += speed
    if keys[pygame.K_LEFT] and icarus_rect.left > 0:
        icarus_rect.x -= speed
    if keys[pygame.K_RIGHT] and icarus_rect.right < WINDOW_WIDTH:
        icarus_rect.x += speed


def load_level():
    global bg_x  


    bg_x -= BG_SPEED * dt
    if bg_x <= -WINDOW_WIDTH:
        bg_x = 0

    screen.blit(background, (bg_x, 0))
    screen.blit(background, (bg_x + WINDOW_WIDTH, 0))


    screen.blit(text_surface, text_rect)
    screen.blit(icarus, icarus_rect)
# ------------------------------ HIT_SOUND ---------------------------------
class Sound:
    def __init__(self, file_path, volume=1.0):
        self.sound = pygame.mixer.Sound(file_path)
        self.sound.set_volume(volume)

    def play(self, loops=0):
        self.sound.play(loops=loops)

    def stop(self):
        self.sound.stop()

hit_sound = Sound("Sound/Soundeffect/Oof.ogg", volume=0.7)

''' Example: Player gets hit randomly for demonstration
    if randint(0, 100) < 2:  # 2% chance per frame
        player_health -= 1
        print(f"Player hit! Health: {player_health}")
        hit_sound.play()  # Play the hit sound'''

# ------------------------------ HIT_SOUND ---------------------------------

# Simple Sound wrapper class
class Sound:
    def __init__(self, file_path, volume=1.0):
        self.sound = pygame.mixer.Sound(file_path)
        self.sound.set_volume(volume)

    def play(self, loops=0):
        self.sound.play(loops=loops)

# SoundLibrary class
class SoundLibrary:
    def __init__(self):
        """
        Initialize the library and load all sounds.
        """
        # Dictionary mapping sound IDs to Sound objects
        self.sounds = {
            'explosion': Sound('oof.ogg', volume=0.7)
            # You can add more sounds here like:
            # 'laser': Sound('laser.ogg', volume=0.5)
        }

    def play(self, sound_id):
        """
        Play a sound by its ID.
        """
        if sound_id in self.sounds:
            self.sounds[sound_id].play()
        else:
            print(f"Warning: Sound '{sound_id}' not found!")

# Example usage
if __name__ == "__main__":
    # Create the sound library
    sound_library = SoundLibrary()

    # Example: Play the explosion sound
    sound_library.play('explosion')

# ------------------------------ HIT_SOUND ---------------------------------


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_keys()
    load_level()
    BG_SPEED *= 1.0002

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
