import pygame

class InputHandler:
    def __init__(self):
        self.pressed_keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_buttons = pygame.mouse.get_pressed()
        self._prev_mouse_buttons = self.mouse_buttons
    
    def update(self):
        """Update input states"""
        self.pressed_keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self._prev_mouse_buttons = self.mouse_buttons
        self.mouse_buttons = pygame.mouse.get_pressed()
    
    def is_key_pressed(self, key):
        """Check if a key is currently pressed"""
        return self.pressed_keys[key]
    
    def is_mouse_button_pressed(self, button=0):
        """Check if a mouse button is currently pressed"""
        return self.mouse_buttons[button]
    
    def is_mouse_button_just_pressed(self, button=0):
        """Check if a mouse button was just pressed this frame"""
        return self.mouse_buttons[button] and not self._prev_mouse_buttons[button]
    
    def get_movement_vector(self):
        """Get normalized movement vector from WASD/Arrow keys"""
        x = self.pressed_keys[pygame.K_d] - self.pressed_keys[pygame.K_a] or \
            self.pressed_keys[pygame.K_RIGHT] - self.pressed_keys[pygame.K_LEFT]
        y = self.pressed_keys[pygame.K_s] - self.pressed_keys[pygame.K_w] or \
            self.pressed_keys[pygame.K_DOWN] - self.pressed_keys[pygame.K_UP]
        return (x, y)
