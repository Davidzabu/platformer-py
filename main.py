import pygame
import random
import sys
from typing import List, Tuple

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 440
ACCELERATION = 0.5
FRICTION = -0.12
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -15
COIN_VALUE = 5

# Initialize Pygame
pygame.init()
Vector2 = pygame.math.Vector2

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()

# Load and scale background
try:
    background = pygame.image.load("background.png")
    background = pygame.transform.scale(background, (860, 480))
except pygame.error as e:
    print(f"Error loading background image: {e}")
    sys.exit()

class Player(pygame.sprite.Sprite):
    """Represents the player character."""
    
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.transform.scale(pygame.image.load("player.png"), (40, 40))
        except pygame.error as e:
            print(f"Error loading player image: {e}")
            sys.exit()
        self.rect = self.image.get_rect(center=(10, 420))
        
        self.pos = Vector2(10, 385)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        
        self.jumping = False
        self.score = 0

    def move(self):
        """Handles player movement based on key presses."""
        self.acc = Vector2(0, GRAVITY)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -ACCELERATION
        if keys[pygame.K_RIGHT]:
            self.acc.x = ACCELERATION
        
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        # Wrap around the screen
        if self.pos.x > SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH
        
        self.rect.midbottom = self.pos

    def update(self, platforms: pygame.sprite.Group):
        """Updates the player's state, including collision detection."""
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and self.vel.y > 0:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0
            self.jumping = False

    def jump(self, platforms: pygame.sprite.Group):
        """Makes the player jump if on a platform."""
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = JUMP_STRENGTH

    def cancel_jump(self):
        """Cancels the jump if the player is ascending."""
        if self.jumping and self.vel.y < -3:
            self.vel.y = -3

class Platform(pygame.sprite.Sprite):
    """Represents a platform that the player can jump on."""
    
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.transform.scale(pygame.image.load("platform.png"), (random.randint(50, 120), 18))
        except pygame.error as e:
            print(f"Error loading platform image: {e}")
            sys.exit()
        self.rect = self.image.get_rect(center=(random.randint(0, SCREEN_WIDTH - 10), random.randint(0, SCREEN_HEIGHT - 10)))
        self.speed = random.randint(-1, 1)
        self.moving = True

    def move(self):
        """Moves the platform and handles collision with the player."""
        if self.moving:
            self.rect.move_ip(self.speed, 0)
            if self.rect.colliderect(player.rect):
                player.pos += (self.speed, 0)
            if self.speed > 0 and self.rect.left > SCREEN_WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.left < 0:
                self.rect.left = SCREEN_WIDTH

    def generate_coin(self):
        """Generates a coin on the platform if it's not moving."""
        if self.speed == 0:
            coins.add(Coin((self.rect.centerx, self.rect.centery - 30)))

class Coin(pygame.sprite.Sprite):
    """Represents a coin that the player can collect."""
    
    def __init__(self, pos: Tuple[int, int]):
        super().__init__()
        try:
            self.image = pygame.transform.scale(pygame.image.load("coin.png"), (20, 20))
        except pygame.error as e:
            print(f"Error loading coin image: {e}")
            sys.exit()
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        """Checks if the player has collected the coin."""
        if self.rect.colliderect(player.rect):
            player.score += COIN_VALUE
            self.kill()

def platform_generator(platforms: pygame.sprite.Group, all_sprites: pygame.sprite.Group):
    """Generates new platforms and ensures they don't overlap."""
    while len(platforms) < 7:
        width = random.randrange(50, 100)
        platform = Platform()
        while check_collision(platform, platforms):
            platform = Platform()
            platform.rect.center = (random.randrange(0, SCREEN_WIDTH - width), random.randrange(-50, 0))
        platform.generate_coin()
        platforms.add(platform)
        all_sprites.add(platform)

def check_collision(platform: Platform, group: pygame.sprite.Group) -> bool:
    """Checks if a platform collides with any other platform in the group."""
    if pygame.sprite.spritecollideany(platform, group):
        return True
    for other_platform in group:
        if other_platform == platform:
            continue
        if (abs(platform.rect.top - other_platform.rect.bottom) < 40) and (abs(platform.rect.bottom - other_platform.rect.top) < 40):
            return True
    return False

def handle_events(player: Player, platforms: pygame.sprite.Group):
    """Handles user input events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump(platforms)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player.cancel_jump()

def update_game_state(player: Player, platforms: pygame.sprite.Group, coins: pygame.sprite.Group):
    """Updates the game state, including player and platform positions."""
    if player.rect.top > SCREEN_HEIGHT:
        game_over()
    
    if player.rect.top <= SCREEN_HEIGHT / 3:
        player.pos.y += abs(player.vel.y)
        for platform in platforms:
            platform.rect.y += abs(player.vel.y)
            if platform.rect.top >= SCREEN_HEIGHT:
                player.score += 1
                platform.kill()
        for coin in coins:
            coin.rect.y += abs(player.vel.y)
            if coin.rect.top >= SCREEN_HEIGHT:
                coin.kill()

def game_over():
    """Handles the game over state."""
    for entity in all_sprites:
        entity.kill()
    screen.fill((255, 0, 0))
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

def render(player: Player, all_sprites: pygame.sprite.Group, coins: pygame.sprite.Group):
    """Renders all game objects to the screen."""
    screen.blit(background, (-50, 0))
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
    for coin in coins:
        screen.blit(coin.image, coin.rect)
    
    font = pygame.font.SysFont("Verdana", 20)
    score_text = font.render(str(player.score), True, (0, 0, 0))
    screen.blit(score_text, (SCREEN_WIDTH / 2, 10))
    
    pygame.display.update()

# Initialize game objects
player = Player()
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
coins = pygame.sprite.Group()

# Create initial platforms
ground = Platform()
ground.image = pygame.Surface((SCREEN_WIDTH, 20))
ground.image.fill((255, 0, 0))
ground.rect = ground.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 10))
ground.moving = False

all_sprites.add(ground)
platforms.add(ground)
all_sprites.add(player)

for _ in range(random.randint(5, 6)):
    platform = Platform()
    while check_collision(platform, platforms):
        platform = Platform()
    platform.generate_coin()
    platforms.add(platform)
    all_sprites.add(platform)

# Main game loop
while True:
    handle_events(player, platforms)
    update_game_state(player, platforms, coins)
    player.update(platforms)
    platform_generator(platforms, all_sprites)
    for entity in all_sprites:
        entity.move()
    for coin in coins:
        coin.update()
    render(player, all_sprites, coins)
    clock.tick(FPS)