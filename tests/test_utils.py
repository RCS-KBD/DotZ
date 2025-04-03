import pytest
import pygame
from utils.asset_loader import AssetLoader
from utils.input_handler import InputHandler
from utils.sprite_utils import GameSprite

def test_asset_loader():
    """Test that assets are loaded correctly"""
    pygame.init()  # Initialize pygame for image loading
    loader = AssetLoader()
    assert loader is not None
    
    # Test image loading with non-existent file
    test_image = loader.load_image('test', 'nonexistent.png')
    assert test_image is None
    
    # Test sound loading with non-existent file
    test_sound = loader.load_sound('test', 'nonexistent.wav')
    assert test_sound is None
    
    # Test font loading with non-existent file
    test_font = loader.load_font('test', 'nonexistent.ttf', 24)
    assert test_font is not None  # Should return default font
    
    pygame.quit()

def test_input_handler():
    """Test input handling functionality"""
    pygame.init()
    handler = InputHandler()
    assert handler is not None
    
    # Test key state tracking
    assert not handler.is_key_pressed(pygame.K_SPACE)
    assert not handler.is_mouse_button_pressed()
    assert not handler.is_mouse_button_just_pressed()
    
    # Test movement vector
    movement = handler.get_movement_vector()
    assert isinstance(movement, tuple)
    assert len(movement) == 2
    
    # Test update
    handler.update()
    assert handler.pressed_keys is not None
    assert handler.mouse_pos is not None
    assert handler.mouse_buttons is not None
    
    pygame.quit()

def test_sprite_utils(mock_screen):
    """Test sprite functionality"""
    # Create a test surface
    test_surface = pygame.Surface((32, 32))
    test_surface.fill((255, 0, 0))  # Red square
    
    # Create a sprite
    sprite = GameSprite(test_surface, (100, 100))
    assert sprite is not None
    assert sprite.rect.centerx == 100
    assert sprite.rect.centery == 100
    
    # Test sprite movement
    sprite.velocity = pygame.math.Vector2(10, 10)
    sprite.update()
    assert sprite.rect.centerx == 110
    assert sprite.rect.centery == 110
    
    # Test sprite drawing
    mock_screen.blit(sprite.image, sprite.rect)  # Use pygame's blit instead of draw
    
    # Test collision detection
    other_sprite = GameSprite(test_surface, (100, 100))
    assert sprite.collides_with(other_sprite)
    
    other_sprite.rect.x = 200
    assert not sprite.collides_with(other_sprite) 