import pygame
import math
import random
from typing import Tuple, Optional, List
import config

class Camera:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.offset_x = 0
        self.offset_y = 0
        
    def follow(self, target):
        """Center the camera on the target"""
        self.offset_x = target.rect.centerx - self.width // 2
        self.offset_y = target.rect.centery - self.height // 2
    
    def apply(self, entity) -> pygame.Rect:
        """Return the entity's position relative to the camera"""
        return pygame.Rect(
            entity.rect.x - self.offset_x,
            entity.rect.y - self.offset_y,
            entity.rect.width,
            entity.rect.height
        )

class Building(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # Door properties
        self.door_width = 30
        self.door_height = 30
        self.door_pos = self._calculate_door_position(width, height)
        
        self.draw_building()
    
    def _calculate_door_position(self, width, height):
        """Calculate door position - randomly on one of the walls"""
        side = random.choice(['top', 'right', 'bottom', 'left'])
        if side == 'top':
            return (random.randint(self.door_width, width - self.door_width), 0)
        elif side == 'right':
            return (width - self.door_width, random.randint(self.door_height, height - self.door_height))
        elif side == 'bottom':
            return (random.randint(self.door_width, width - self.door_width), height - self.door_height)
        else:  # left
            return (0, random.randint(self.door_height, height - self.door_height))
    
    def draw_building(self):
        # Draw main building
        pygame.draw.rect(self.image, config.BROWN, (0, 0, self.rect.width, self.rect.height))
        
        # Draw door (by erasing the area)
        pygame.draw.rect(self.image, (0, 0, 0, 0), 
                        (self.door_pos[0], self.door_pos[1], 
                         self.door_width, self.door_height))
    
    def collides_with_point(self, x, y):
        """Check if a point collides with the building, excluding the door"""
        if not self.rect.collidepoint(x, y):
            return False
            
        # Convert point to building's local coordinates
        local_x = x - self.rect.x
        local_y = y - self.rect.y
        
        # Check if point is in door
        in_door = (self.door_pos[0] <= local_x <= self.door_pos[0] + self.door_width and
                  self.door_pos[1] <= local_y <= self.door_pos[1] + self.door_height)
        
        return not in_door  # Return True if point collides with building but not door

class Shockwave(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.radius = 10
        self.max_radius = 100
        self.growth_rate = 300  # pixels per second
        self.damage = config.SHOCKWAVE_DAMAGE
        self.knockback = config.SHOCKWAVE_KNOCKBACK
        
        # Create surface
        self.image = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.center_x = x
        self.center_y = y
        
    def update(self, dt: float) -> bool:
        """Update shockwave size. Returns True if shockwave should be removed."""
        self.radius += self.growth_rate * dt
        
        # Clear previous frame
        self.image.fill((0, 0, 0, 0))
        
        # Draw new circle
        pygame.draw.circle(self.image, (*config.BLUE, 128), 
                         (self.max_radius, self.max_radius), 
                         int(self.radius))
        
        # Remove if too large
        return self.radius >= self.max_radius

class Entity(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, radius: int, color: Tuple[int, int, int], max_health: int):
        super().__init__()
        
        # Create circular surface
        self.radius = radius
        self.color = color
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        
        # Set up rect and position
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Movement and collision
        self.speed = 0
        self.knockback_dx = 0
        self.knockback_dy = 0
        
        # Combat stats
        self.max_health = max_health
        self.health = max_health
        self.is_hostile = False
        self.attack_cooldown = 0
        self.is_dead = False
        self.draw_entity()
        
    def draw_entity(self):
        self.image.fill((0, 0, 0, 0))  # Clear with transparency
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        if self.is_dead:
            # Draw X mark when dead
            pygame.draw.line(self.image, (0, 0, 0), (5, 5), 
                           (self.radius * 2 - 5, self.radius * 2 - 5), 3)
            pygame.draw.line(self.image, (0, 0, 0), (5, self.radius * 2 - 5),
                           (self.radius * 2 - 5, 5), 3)

    def move(self, dx, dy, all_sprites):
        if self.is_dead:
            return False

        # Store original position
        original_x = self.rect.x
        original_y = self.rect.y
        
        # Apply movement
        self.rect.x += dx
        self.rect.y += dy
        
        # Check collisions with buildings
        collision = False
        for sprite in all_sprites:
            if isinstance(sprite, Building) and sprite != self:
                # Check each corner of the entity
                corners = [
                    (self.rect.left, self.rect.top),
                    (self.rect.right, self.rect.top),
                    (self.rect.left, self.rect.bottom),
                    (self.rect.right, self.rect.bottom)
                ]
                
                for corner_x, corner_y in corners:
                    if sprite.collides_with_point(corner_x, corner_y):
                        collision = True
                        break
                
                if collision:
                    break
        
        # If collision occurred, revert movement
        if collision:
            self.rect.x = original_x
            self.rect.y = original_y
            return True
        
        return False

    def take_damage(self, amount: int, knockback_x: float = 0, knockback_y: float = 0):
        """Take damage and knockback"""
        if not self.is_dead:
            self.health = max(0, self.health - amount)
            self.knockback_dx += knockback_x
            self.knockback_dy += knockback_y
            if self.health <= 0:
                self.is_dead = True
                self.draw_entity()
            return self.health <= 0

    def get_distance_to(self, other: 'Entity') -> float:
        """Get distance to another entity"""
        dx = other.rect.centerx - self.rect.centerx
        dy = other.rect.centery - self.rect.centery
        return math.sqrt(dx * dx + dy * dy)

class Player(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, radius=config.PLAYER_SIZE, color=config.BLUE, max_health=config.PLAYER_MAX_HEALTH)
        self.speed = config.PLAYER_SPEED
        self.attack_cooldown = 0
        self.shockwave_cooldown = 0
        self.followers: List[NPC] = []
    
    def update(self, dt: float, sprites: pygame.sprite.Group) -> Optional[Shockwave]:
        if self.is_dead:
            return None
        
        # Update cooldowns
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        self.shockwave_cooldown = max(0, self.shockwave_cooldown - dt)
        
        # Get keyboard input
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] - keys[pygame.K_a]) * self.speed * dt
        dy = (keys[pygame.K_s] - keys[pygame.K_w]) * self.speed * dt
        
        # Move with collision detection
        self.move(dx, dy, sprites)
        
        # Create shockwave on space press if cooldown is ready
        if keys[pygame.K_SPACE] and self.shockwave_cooldown <= 0:
            self.shockwave_cooldown = config.SHOCKWAVE_COOLDOWN
            return Shockwave(self.rect.centerx, self.rect.centery)
        
        return None

class Zombie(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, radius=config.ZOMBIE_SIZE, color=config.RED, max_health=config.ZOMBIE_MAX_HEALTH)
        self.speed = config.ZOMBIE_SPEED
        self.attack_cooldown = 0
        self.is_hostile = True
    
    def update(self, dt: float, player: Player, sprites: pygame.sprite.Group):
        if self.is_dead:
            return
        
        # Update attack cooldown
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        
        # Get direction to player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Move towards player if in detection range
        if distance <= config.ZOMBIE_DETECTION_RADIUS:
            if distance > 0:
                dx = dx / distance * self.speed * dt
                dy = dy / distance * self.speed * dt
                collision = self.move(dx, dy, sprites)
                
                # Deal damage on collision if attack is ready
                if collision and self.attack_cooldown <= 0:
                    player.take_damage(config.ZOMBIE_DAMAGE, dx * 2, dy * 2)
                    self.attack_cooldown = config.ZOMBIE_ATTACK_COOLDOWN

class NPC(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, radius=config.NPC_SIZE, color=config.WHITE, max_health=config.NPC_MAX_HEALTH)
        self.speed = config.NPC_SPEED
        self.attack_cooldown = 0
        self.revealed = False
        self.is_hostile = random.random() < config.HOSTILE_NPC_CHANCE
        self.following_player = False
        self.attack_range = config.NPC_ATTACK_RANGE
    
    def update(self, dt: float, player: Player, sprites: pygame.sprite.Group):
        if self.is_dead:
            return
        
        # Update attack cooldown
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        
        # Get distance to player
        distance = self.get_distance_to(player)
        
        # Reveal true nature when player gets close
        if not self.revealed and distance <= config.NPC_DETECTION_RADIUS:
            self.revealed = True
            if self.is_hostile:
                self.image.fill((0, 0, 0, 0))
                pygame.draw.circle(self.image, config.YELLOW, (self.radius, self.radius), self.radius)
            else:
                # Start following player if friendly
                self.following_player = True
                if self not in player.followers:
                    player.followers.append(self)
        
        if self.revealed:
            if self.is_hostile:
                # Hostile behavior
                if distance > 0:
                    dx = player.rect.centerx - self.rect.centerx
                    dy = player.rect.centery - self.rect.centery
                    dx = dx / distance * self.speed * dt
                    dy = dy / distance * self.speed * dt
                    collision = self.move(dx, dy, sprites)
                    
                    # Deal damage on collision if attack is ready
                    if collision and self.attack_cooldown <= 0:
                        player.take_damage(config.NPC_DAMAGE, dx * 2, dy * 2)
                        self.attack_cooldown = config.NPC_ATTACK_COOLDOWN
            
            elif self.following_player:
                # Friendly behavior - follow player but maintain distance
                if distance > config.NPC_FOLLOW_DISTANCE:
                    dx = player.rect.centerx - self.rect.centerx
                    dy = player.rect.centery - self.rect.centery
                    dx = dx / distance * self.speed * dt
                    dy = dy / distance * self.speed * dt
                    self.move(dx, dy, sprites)
                
                # Attack nearby enemies
                for sprite in sprites:
                    if isinstance(sprite, (Zombie, NPC)) and sprite.is_hostile:
                        enemy_distance = self.get_distance_to(sprite)
                        if enemy_distance <= self.attack_range and self.attack_cooldown <= 0:
                            dx = sprite.rect.centerx - self.rect.centerx
                            dy = sprite.rect.centery - self.rect.centery
                            sprite.take_damage(config.NPC_FRIENDLY_DAMAGE, dx, dy)
                            self.attack_cooldown = config.NPC_ATTACK_COOLDOWN 