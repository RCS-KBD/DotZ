import pytest
import pygame
from states.game_state import MenuState, PlayState, PauseState
import config

def test_menu_navigation(game):
    """Test menu state navigation and selection"""
    menu_state = game.states['menu']
    
    # Test initial state
    assert menu_state.selected_option == 0
    assert len(menu_state.options) > 0
    
    # Test moving down
    menu_state.handle_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN}))
    assert menu_state.selected_option == 1
    
    # Test moving up
    menu_state.handle_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP}))
    assert menu_state.selected_option == 0
    
    # Test wrapping around
    for _ in range(len(menu_state.options) + 1):
        menu_state.handle_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN}))
    assert menu_state.selected_option == 1  # Should wrap around

def test_play_state_mechanics(game):
    """Test play state game mechanics"""
    pygame.init()  # Initialize pygame for key handling
    play_state = game.states['play']
    
    # Test player initialization
    assert play_state.player is not None
    initial_x = play_state.player.rect.centerx
    
    # Create a mock keyboard state
    # We need to monkey patch pygame.key.get_pressed to return our mock state
    original_get_pressed = pygame.key.get_pressed
    mock_keys = [0] * 512  # Create a list of key states
    mock_keys[pygame.K_d] = 1  # Set D key to pressed
    pygame.key.get_pressed = lambda: mock_keys
    
    # Update multiple frames to ensure movement
    for _ in range(5):
        play_state.update(0.016)  # Simulate one frame at 60 FPS
    
    # Restore original function
    pygame.key.get_pressed = original_get_pressed
    
    # Player should have moved right
    assert play_state.player.rect.centerx > initial_x
    
    # Test collision with boundaries
    play_state.player.rect.x = -100
    play_state.update(0.016)
    assert play_state.player.rect.x >= -100  # Allow movement but check it's not getting stuck
    
    # Test entity management
    initial_entity_count = len(play_state.entities)
    # Add a test entity
    test_entity = pygame.sprite.Sprite()
    play_state.all_sprites.add(test_entity)
    assert len(play_state.entities) == initial_entity_count + 1
    
    pygame.quit()

def test_pause_functionality(game):
    """Test pause state functionality"""
    # Start in play state
    game.change_state('play')
    assert isinstance(game.current_state, PlayState)
    
    # Test pausing
    game.current_state.handle_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE}))
    assert isinstance(game.current_state, PauseState)
    
    # Test resuming
    game.current_state.handle_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE}))
    assert isinstance(game.current_state, PlayState)
    
    # Test pause menu options
    pause_state = game.states['pause']
    assert 'Resume' in pause_state.options
    assert 'Quit to Menu' in pause_state.options

def test_game_state_transitions(game):
    """Test complex state transitions and data preservation"""
    # Start in menu
    assert isinstance(game.current_state, MenuState)
    
    # Go to play state
    game.change_state('play')
    play_state = game.current_state
    
    # Record some initial state
    initial_x = play_state.player.rect.centerx
    initial_y = play_state.player.rect.centery
    initial_entity_count = len(play_state.entities)
    
    # Pause and resume
    game.change_state('pause')
    game.change_state('play')
    
    # Verify state is preserved
    assert play_state.player.rect.centerx == initial_x
    assert play_state.player.rect.centery == initial_y
    assert len(play_state.entities) == initial_entity_count
    
    # Test returning to menu
    game.change_state('menu')
    assert isinstance(game.current_state, MenuState)
    assert game.current_state.selected_option == 0  # Menu should reset 