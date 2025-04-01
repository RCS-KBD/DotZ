import pygame
from typing import Union, Tuple

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image: Union[pygame.Surface, str], pos: Tuple[float, float], *groups):
        super().__init__(*groups)
        self.image = image if isinstance(image, pygame.Surface) else pygame.image.load(image)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(0, 0)
    
    def update(self):
        """Update sprite position based on velocity"""
        self.pos += self.velocity
        self.rect.center = self.pos
    
    def collides_with(self, other: 'GameSprite') -> bool:
        """Check collision with another sprite"""
        return self.rect.colliderect(other.rect)

def load_spritesheet(filename: str, sprite_size: Tuple[int, int], colorkey=None) -> list:
    """Load a spritesheet and split it into surfaces"""
    sheet = pygame.image.load(filename)
    sprites = []
    
    sheet_width = sheet.get_width()
    sheet_height = sheet.get_height()
    
    for y in range(0, sheet_height, sprite_size[1]):
        for x in range(0, sheet_width, sprite_size[0]):
            sprite = pygame.Surface(sprite_size)
            sprite.blit(sheet, (0, 0), (x, y, sprite_size[0], sprite_size[1]))
            if colorkey is not None:
                sprite.set_colorkey(colorkey)
            sprites.append(sprite)
    
    return sprites
