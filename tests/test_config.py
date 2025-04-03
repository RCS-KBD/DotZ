import pytest
import config

def test_window_configuration():
    """Test that window configuration values are valid"""
    assert config.WINDOW_WIDTH > 0
    assert config.WINDOW_HEIGHT > 0
    assert isinstance(config.WINDOW_WIDTH, int)
    assert isinstance(config.WINDOW_HEIGHT, int)

def test_game_configuration():
    """Test that game configuration values are valid"""
    assert config.FPS > 0
    assert isinstance(config.FPS, int)
    assert config.GRAVITY >= 0
    assert isinstance(config.GRAVITY, float)

def test_color_configuration():
    """Test that color configuration values are valid"""
    assert isinstance(config.BLACK, tuple)
    assert len(config.BLACK) == 3
    assert all(0 <= x <= 255 for x in config.BLACK)
    
    assert isinstance(config.WHITE, tuple)
    assert len(config.WHITE) == 3
    assert all(0 <= x <= 255 for x in config.WHITE)

def test_asset_paths():
    """Test that asset paths are valid"""
    assert isinstance(config.ASSETS_DIR, str)
    assert isinstance(config.IMAGES_DIR, str)
    assert isinstance(config.SOUNDS_DIR, str)
    assert isinstance(config.FONTS_DIR, str) 