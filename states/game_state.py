from abc import ABC, abstractmethod

class GameState(ABC):
    def __init__(self, game):
        self.game = game
    
    @abstractmethod
    def update(self, dt):
        """Update game state"""
        pass
    
    @abstractmethod
    def draw(self, screen):
        """Draw game state"""
        pass
    
    @abstractmethod
    def handle_event(self, event):
        """Handle pygame events"""
        pass

class MenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.selected_option = 0
        self.options = ['Start Game', 'Options', 'Quit']
    
    def update(self, dt):
        pass
    
    def draw(self, screen):
        # Example menu drawing
        font = pygame.font.Font(None, 36)
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = font.render(option, True, color)
            rect = text.get_rect(center=(screen.get_width() // 2, 200 + i * 50))
            screen.blit(text, rect)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.options[self.selected_option] == 'Start Game':
                    self.game.change_state('play')
                elif self.options[self.selected_option] == 'Quit':
                    pygame.quit()
                    sys.exit()

class PlayState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.sprites = pygame.sprite.Group()
        # Initialize game objects here
    
    def update(self, dt):
        self.sprites.update()
    
    def draw(self, screen):
        self.sprites.draw(screen)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.change_state('pause')

class PauseState(GameState):
    def __init__(self, game):
        super().__init__(game)
    
    def update(self, dt):
        pass
    
    def draw(self, screen):
        # Draw semi-transparent overlay
        overlay = pygame.Surface(screen.get_size())
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # Draw pause text
        font = pygame.font.Font(None, 48)
        text = font.render('PAUSED', True, (255, 255, 255))
        rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, rect)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.change_state('play')
