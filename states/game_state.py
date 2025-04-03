import pygame
import sys
import random
import math
from abc import ABC, abstractmethod
from utils.entities import Player, Zombie, NPC, Camera, Building, Shockwave
import config

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
        # Clear screen
        screen.fill(config.BLACK)
        
        # Draw menu options
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
                    # Create a fresh PlayState instead of reusing the old one
                    self.game.states['play'] = PlayState(self.game)
                    self.game.change_state('play')
                elif self.options[self.selected_option] == 'Quit':
                    pygame.quit()
                    sys.exit()

class PlayState(GameState):
    def __init__(self, game):
        super().__init__(game)
        
        # Initialize sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.buildings = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.shockwaves = pygame.sprite.Group()
        
        # Initialize camera
        self.camera = Camera(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        
        # Create buildings first
        self.spawn_buildings()
        
        # Create player in center
        self.player = Player(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2)
        self.all_sprites.add(self.player)
        
        # Add entities
        self.entities = self.all_sprites
        self.spawn_test_entities()
    
    def spawn_buildings(self):
        """Spawn random buildings around the map"""
        for _ in range(config.NUM_BUILDINGS):
            # Generate random size
            width = random.randint(config.BUILDING_MIN_SIZE, config.BUILDING_MAX_SIZE)
            height = random.randint(config.BUILDING_MIN_SIZE, config.BUILDING_MAX_SIZE)
            
            # Try to find a valid position (not overlapping other buildings)
            max_attempts = 50
            for _ in range(max_attempts):
                x = random.randint(50, config.WINDOW_WIDTH - width - 50)
                y = random.randint(50, config.WINDOW_HEIGHT - height - 50)
                
                # Create temporary rect to check overlap
                test_rect = pygame.Rect(x, y, width, height)
                padding = 50  # Space between buildings
                
                # Check if too close to center (player spawn)
                center_dist = math.sqrt(
                    (x + width/2 - config.WINDOW_WIDTH/2)**2 +
                    (y + height/2 - config.WINDOW_HEIGHT/2)**2
                )
                if center_dist < 200:  # Keep buildings away from spawn
                    continue
                
                # Check overlap with other buildings
                overlap = False
                for building in self.buildings:
                    expanded_rect = building.rect.inflate(padding, padding)
                    if expanded_rect.colliderect(test_rect):
                        overlap = True
                        break
                
                if not overlap:
                    building = Building(x, y, width, height)
                    self.buildings.add(building)
                    self.all_sprites.add(building)
                    break
    
    def get_random_spawn_position(self, min_distance=300, max_distance=500):
        """Get a random position that's between min and max distance from player"""
        for _ in range(50):  # Maximum attempts
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(min_distance, max_distance)
            
            x = self.player.rect.centerx + distance * math.cos(angle)
            y = self.player.rect.centery + distance * math.sin(angle)
            
            # Create test rect
            test_rect = pygame.Rect(x - 25, y - 25, 50, 50)
            
            # Check if position is valid (not inside buildings)
            valid = True
            for building in self.buildings:
                if building.rect.colliderect(test_rect):
                    valid = False
                    break
            
            if valid and 0 <= x <= config.WINDOW_WIDTH and 0 <= y <= config.WINDOW_HEIGHT:
                return x, y
        
        # If no valid position found, return a position near the edge
        return random.randint(50, config.WINDOW_WIDTH-50), random.randint(50, config.WINDOW_HEIGHT-50)
    
    def spawn_test_entities(self):
        # Spawn zombies at random positions
        for _ in range(5):
            x, y = self.get_random_spawn_position()
            zombie = Zombie(x, y)
            self.all_sprites.add(zombie)
            self.enemies.add(zombie)
        
        # Spawn NPCs at random positions
        for _ in range(3):
            x, y = self.get_random_spawn_position()
            npc = NPC(x, y)
            self.all_sprites.add(npc)
            self.npcs.add(npc)
            if npc.is_hostile:
                self.enemies.add(npc)
    
    def update(self, dt):
        # Update player and check for shockwave creation
        shockwave = self.player.update(dt, self.all_sprites)
        if shockwave:
            self.shockwaves.add(shockwave)
            self.all_sprites.add(shockwave)
        
        # Update shockwaves and check for collisions
        for shockwave in list(self.shockwaves):
            if shockwave.update(dt):
                shockwave.kill()
            else:
                # Check for entities in shockwave radius
                for sprite in self.all_sprites:
                    if isinstance(sprite, (Zombie, NPC)) and sprite.is_hostile:
                        dx = sprite.rect.centerx - shockwave.center_x
                        dy = sprite.rect.centery - shockwave.center_y
                        distance = math.sqrt(dx * dx + dy * dy)
                        
                        if distance <= shockwave.radius:
                            # Calculate knockback direction
                            if distance > 0:
                                knockback_x = (dx / distance) * shockwave.knockback * dt
                                knockback_y = (dy / distance) * shockwave.knockback * dt
                                sprite.take_damage(shockwave.damage, knockback_x, knockback_y)
        
        # Update enemies and NPCs
        for sprite in self.all_sprites:
            if isinstance(sprite, (Zombie, NPC)) and sprite != self.player:
                sprite.update(dt, self.player, self.all_sprites)
        
        # Update camera to follow player
        self.camera.follow(self.player)
        
        # Check player death
        if self.player.health <= 0:
            self.game.change_state('menu')
    
    def draw(self, screen):
        # Clear screen
        screen.fill(config.BLACK)
        
        # Draw all sprites with camera offset
        for sprite in self.all_sprites:
            screen_pos = self.camera.apply(sprite)
            screen.blit(sprite.image, screen_pos)
            
            # Draw health bars for entities
            if isinstance(sprite, (Player, Zombie, NPC)):
                health_pct = sprite.health / sprite.max_health
                bar_width = sprite.rect.width
                bar_height = 5
                
                # Background (red)
                bar_pos = pygame.Rect(
                    screen_pos.x,
                    screen_pos.y - 10,
                    bar_width,
                    bar_height
                )
                pygame.draw.rect(screen, config.RED, bar_pos)
                
                # Foreground (green)
                bar_pos.width *= health_pct
                pygame.draw.rect(screen, config.GREEN, bar_pos)
        
        # Draw UI
        self.draw_ui(screen)
    
    def draw_ui(self, screen):
        # Draw player health bar
        bar_width = 200
        bar_height = 20
        x = 10
        y = 10
        
        # Background (red)
        pygame.draw.rect(screen, config.RED, (x, y, bar_width, bar_height))
        
        # Foreground (green)
        health_width = (self.player.health / self.player.max_health) * bar_width
        pygame.draw.rect(screen, config.GREEN, (x, y, health_width, bar_height))
        
        # Draw health text
        font = pygame.font.Font(None, 24)
        health_text = f"Health: {int(self.player.health)}/{self.player.max_health}"
        text_surface = font.render(health_text, True, config.WHITE)
        screen.blit(text_surface, (x + 10, y + 25))
        
        # Draw shockwave cooldown
        if self.player.shockwave_cooldown > 0:
            cooldown_text = f"Shockwave: {self.player.shockwave_cooldown:.1f}s"
        else:
            cooldown_text = "Shockwave: Ready!"
        cooldown_surface = font.render(cooldown_text, True, config.WHITE)
        screen.blit(cooldown_surface, (x + 10, y + 45))
        
        # Draw follower count
        follower_text = f"Followers: {len(self.player.followers)}"
        follower_surface = font.render(follower_text, True, config.WHITE)
        screen.blit(follower_surface, (x + 10, y + 65))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.change_state('pause')

class PauseState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.options = ['Resume', 'Restart', 'Quit to Menu']
    
    def update(self, dt):
        pass
    
    def draw(self, screen):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # Draw pause menu options
        font = pygame.font.Font(None, 36)
        for i, option in enumerate(self.options):
            text = font.render(option, True, (255, 255, 255))
            rect = text.get_rect(center=(screen.get_width() // 2, 200 + i * 50))
            screen.blit(text, rect)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_state('play')
