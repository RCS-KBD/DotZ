# Game settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
GRAVITY = 9.81  # Standard gravity in m/s²

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  # For hostile NPCs
BROWN = (139, 69, 19)   # For buildings
DARK_BROWN = (101, 67, 33)  # For doors

# Player settings
PLAYER_SPEED = 350       # Slightly faster than before
PLAYER_SIZE = 25
PLAYER_MAX_HEALTH = 100
PLAYER_DAMAGE = 20
PLAYER_ATTACK_COOLDOWN = 0.5

# Shockwave settings
SHOCKWAVE_DAMAGE = 15
SHOCKWAVE_KNOCKBACK = 400
SHOCKWAVE_COOLDOWN = 1.0  # Seconds between shockwaves

# Enemy settings
ZOMBIE_SPEED = 120       # Slower than before
ZOMBIE_SIZE = 25
ZOMBIE_DAMAGE = 5        # Less damage
ZOMBIE_MAX_HEALTH = 50
ZOMBIE_ATTACK_COOLDOWN = 1.5  # Longer cooldown
ZOMBIE_DETECTION_RADIUS = 250  # Shorter detection range

# NPC settings
NPC_SPEED = 150          # Slower than before
NPC_SIZE = 25
NPC_DAMAGE = 8          # Less damage
NPC_MAX_HEALTH = 75
NPC_ATTACK_COOLDOWN = 1.2  # Longer cooldown
NPC_DETECTION_RADIUS = 150
HOSTILE_NPC_CHANCE = 0.4    # Lower chance to be hostile
NPC_FOLLOW_DISTANCE = 100  # Distance friendly NPCs try to maintain from player
NPC_ATTACK_RANGE = 100     # Range at which friendly NPCs attack enemies
NPC_FRIENDLY_DAMAGE = 10   # Damage dealt by friendly NPCs

# Building settings
BUILDING_MIN_SIZE = 100
BUILDING_MAX_SIZE = 300
NUM_BUILDINGS = 5  # Number of buildings to spawn

# Collision settings
COLLISION_DAMAGE = 5
KNOCKBACK_FORCE = 300

# Game states
STATE_MENU = 'menu'
STATE_PLAYING = 'play'
STATE_PAUSED = 'pause'
STATE_GAME_OVER = 'game_over'

# Asset settings
ASSETS_DIR = 'assets'  # Changed from ASSET_DIR to match test expectations
IMAGES_DIR = f'{ASSETS_DIR}/images'  # Changed from IMAGE_DIR
SOUNDS_DIR = f'{ASSETS_DIR}/sounds'  # Changed from SOUND_DIR
FONTS_DIR = f'{ASSETS_DIR}/fonts'    # Changed from FONT_DIR
