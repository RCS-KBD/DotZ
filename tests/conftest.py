import pytest
import pygame
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import Game
from config import *

@pytest.fixture
def game():
    """Fixture to create a game instance for testing"""
    pygame.init()
    game = Game()
    yield game
    pygame.quit()

@pytest.fixture
def mock_screen():
    """Fixture to create a mock screen for testing"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    yield screen
    pygame.quit()

@pytest.fixture
def mock_event():
    """Fixture to create a mock pygame event"""
    return pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE}) 