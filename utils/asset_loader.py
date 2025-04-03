import os
import pygame

class AssetLoader:
    def __init__(self):
        self.base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
        self.images = {}
        self.sounds = {}
        self.fonts = {}
    
    def load_image(self, name, filename):
        """Load an image asset."""
        path = os.path.join(self.base_path, 'images', filename)
        try:
            if os.path.exists(path):
                self.images[name] = pygame.image.load(path).convert_alpha()
                return self.images[name]
            return None
        except (pygame.error, FileNotFoundError) as e:
            print(f'Could not load image {filename}: {e}')
            return None
    
    def load_sound(self, name, filename):
        """Load a sound asset."""
        path = os.path.join(self.base_path, 'sounds', filename)
        try:
            if os.path.exists(path):
                self.sounds[name] = pygame.mixer.Sound(path)
                return self.sounds[name]
            return None
        except (pygame.error, FileNotFoundError) as e:
            print(f'Could not load sound {filename}: {e}')
            return None
    
    def load_font(self, name, filename, size):
        """Load a font asset."""
        path = os.path.join(self.base_path, 'fonts', filename)
        try:
            if os.path.exists(path):
                self.fonts[name] = pygame.font.Font(path, size)
                return self.fonts[name]
            return pygame.font.Font(None, size)  # Fallback to default font
        except (pygame.error, FileNotFoundError) as e:
            print(f'Could not load font {filename}: {e}')
            return pygame.font.Font(None, size)  # Fallback to default font
