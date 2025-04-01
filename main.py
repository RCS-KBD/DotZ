import pygame
import sys
from utils.asset_loader import AssetLoader
from utils.input_handler import InputHandler
from states.game_state import MenuState, PlayState, PauseState
import config

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        # Set up display
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption('PyGame Project')
        self.clock = pygame.time.Clock()
        
        # Initialize systems
        self.assets = AssetLoader()
        self.input_handler = InputHandler()
        
        # Set up game states
        self.states = {
            'menu': MenuState(self),
            'play': PlayState(self),
            'pause': PauseState(self)
        }
        self.current_state = self.states['menu']
        
    def change_state(self, state_name):
        """Change the current game state"""
        if state_name in self.states:
            self.current_state = self.states[state_name]
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            # Calculate delta time
            dt = self.clock.tick(config.FPS) / 1000.0  # Convert to seconds
            
            # Update input handler
            self.input_handler.update()
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.current_state.handle_event(event)
            
            # Update current state
            self.current_state.update(dt)
            
            # Drawing
            self.screen.fill(config.BLACK)
            self.current_state.draw(self.screen)
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()