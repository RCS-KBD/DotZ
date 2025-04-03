import pytest
import pygame
from states.game_state import MenuState, PlayState, PauseState

def test_state_transitions(game):
    """Test that state transitions work correctly"""
    # Start in menu state
    assert isinstance(game.current_state, MenuState)
    
    # Transition to play state
    game.change_state('play')
    assert isinstance(game.current_state, PlayState)
    
    # Transition to pause state
    game.change_state('pause')
    assert isinstance(game.current_state, PauseState)
    
    # Transition back to menu
    game.change_state('menu')
    assert isinstance(game.current_state, MenuState)

def test_menu_state_initialization(game):
    """Test that menu state initializes correctly"""
    menu_state = game.states['menu']
    assert menu_state is not None
    assert hasattr(menu_state, 'options')
    assert len(menu_state.options) > 0

def test_play_state_initialization(game):
    """Test that play state initializes correctly"""
    play_state = game.states['play']
    assert play_state is not None
    assert hasattr(play_state, 'player')
    assert hasattr(play_state, 'entities')

def test_pause_state_initialization(game):
    """Test that pause state initializes correctly"""
    pause_state = game.states['pause']
    assert pause_state is not None
    assert hasattr(pause_state, 'options')
    assert len(pause_state.options) > 0

def test_state_event_handling(game, mock_event):
    """Test that states handle events correctly"""
    # Test menu state event handling
    menu_state = game.states['menu']
    menu_state.handle_event(mock_event)
    
    # Test play state event handling
    play_state = game.states['play']
    play_state.handle_event(mock_event)
    
    # Test pause state event handling
    pause_state = game.states['pause']
    pause_state.handle_event(mock_event) 