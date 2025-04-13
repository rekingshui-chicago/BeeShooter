"""
Game manager
"""
import pygame
import random
import math
import logging
from pygame.locals import *
from src.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, RED, GREEN, BLUE, YELLOW, ORANGE,
    PURPLE, CYAN, PINK, GREY, LIGHT_BLUE, DARK_BLUE, B_KEY, B_KEY_UPPER,
    ENEMY_LEVEL_1, ENEMY_LEVEL_2, ENEMY_LEVEL_3, ENEMY_LEVEL_4,
    WEAPON_LEVEL_1, WEAPON_LEVEL_2, WEAPON_LEVEL_3, WEAPON_LEVEL_4, WEAPON_LEVEL_5,
    MISSILE_LEVEL_1, MISSILE_LEVEL_2, MISSILE_LEVEL_3, MISSILE_LEVEL_4,
    LEVEL_THRESHOLDS
)
from src.utils.resources import load_image, setup_sound_system, play_sound
from src.entities.player import Player
from src.entities.bee import Bee
from src.entities.boss import Boss
from src.entities.powerup import PowerUp
from src.effects.explosion import Explosion
from src.effects.bomb_effect import BombEffect
from src.effects.victory_effect import VictoryEffect

logger = logging.getLogger('bee_shooter.game_manager')

class GameManager:
    """Main game manager class"""
    def __init__(self, args):
        """Initialize the game manager"""
        self.args = args
        self.screen = None
        self.clock = None
        self.running = True
        self.game_over = False
        self.score = 0
        self.high_score = 0
        self.debug_info = args.debug

        # Initialize pygame
        pygame.init()
        pygame.display.set_caption("Bee Shooter")

        # Create screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Setup sound system
        self.sounds, self.sound_enabled = setup_sound_system(args)

        # Start background music if sound is enabled
        if self.sound_enabled:
            try:
                # Play background music on a loop (-1 means loop indefinitely)
                print("Attempting to play background music...")
                play_sound('background_music', channel='background_music', loops=-1, fade_ms=2000)
                print("Background music started successfully")
                logger.info("Background music started")
            except Exception as e:
                print(f"Failed to play background music: {e}")
                logger.error(f"Failed to play background music: {e}")
                # Continue game without background music

        # Initialize sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.bees = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.missiles_group = pygame.sprite.Group()

        # Screen shake effect
        self.screen_shake = 0

        # B key debounce variables
        self.last_b_key_time = 0
        self.b_key_debounce_time = 500  # milliseconds

        # Auto-missile launch variables
        self.last_auto_missile_time = 0
        self.auto_missile_delay = 3000  # Launch a missile every 3 seconds

        # Background scrolling variables
        self.bg_scroll_x = 0
        self.bg_scroll_y = 0
        self.bg_scroll_speed = 5.0  # Very fast scrolling speed for high-speed flight effect
        self.bg_auto_scroll_speed = 3.0  # Faster automatic vertical scrolling speed

        # Create background
        self.background = load_image("background")

        # Create twinkling stars effect with varying speeds for parallax effect
        self.twinkle_stars = []
        for _ in range(50):  # Increased number of stars
            x = random.randrange(0, SCREEN_WIDTH)
            y = random.randrange(0, SCREEN_HEIGHT)
            size = random.randrange(1, 4)  # Slightly larger stars
            twinkle_speed = random.uniform(0.02, 0.1)
            # Star movement speed (for parallax effect)
            move_speed = random.uniform(0.5, 5.0)  # Varying speeds for depth effect
            self.twinkle_stars.append({
                "pos": [x, y],  # Using list instead of tuple to allow modification
                "size": size,
                "phase": random.uniform(0, 2*math.pi),
                "twinkle_speed": twinkle_speed,
                "move_speed": move_speed  # Stars move at different speeds
            })

        # Create moving nebula effect with more red nebulae
        self.nebula_clouds = []
        for _ in range(4):  # Increased from 2 to 4 for more nebulae
            x = random.randrange(-100, SCREEN_WIDTH)
            y = random.randrange(-100, SCREEN_HEIGHT)
            size = random.randrange(150, 300)
            speed_x = random.uniform(-0.2, 0.2)
            speed_y = random.uniform(-0.2, 0.2)

            # Create a nebula surface with transparency
            nebula_surf = pygame.Surface((size, size), pygame.SRCALPHA)

            # Choose a random color for the nebula with emphasis on red colors
            nebula_colors = [
                (60, 20, 60),   # Purple
                (50, 20, 70),   # Blue-purple
                (20, 40, 70),   # Blue
                (120, 30, 30),   # Red
                (150, 40, 30),   # Bright red
                (100, 30, 20),   # Dark red
                (130, 50, 30),   # Red-orange
                (140, 30, 40)    # Red-purple
            ]
            # Increase probability of red nebulae (last 5 colors are reddish)
            weights = [1, 1, 1, 3, 3, 3, 3, 3]  # Higher weights for red colors
            nebula_color = random.choices(nebula_colors, weights=weights, k=1)[0] + (3,)  # Very low alpha

            # Draw the nebula as a series of transparent circles
            for _ in range(40):
                nx = random.randrange(0, size)
                ny = random.randrange(0, size)
                nr = random.randrange(20, size // 2)
                pygame.draw.circle(nebula_surf, nebula_color, (nx, ny), nr)

            self.nebula_clouds.append({"surf": nebula_surf, "pos": [x, y], "speed": (speed_x, speed_y)})

        # Level system variables
        self.current_level = 1
        self.max_level = 3
        self.level_complete = False
        self.boss_active = False
        self.boss = None
        self.victory = False
        self.level_thresholds = LEVEL_THRESHOLDS  # Use the constants

        # Create player
        self.player = Player()
        self.all_sprites.add(self.player)

        # Spawn initial bees for level 1
        self.spawn_bees_for_level(self.current_level)

    def spawn_bees_for_level(self, level):
        """Spawn bees appropriate for the current level"""
        # Clear existing bees
        for bee in list(self.bees):
            bee.kill()

        # Reduced number of bees for lower difficulty
        num_bees = 5 + level * 2  # Level 1: 7, Level 2: 9, Level 3: 11

        # Adjust level distribution based on current game level
        for _ in range(num_bees):
            # Higher levels have more difficult bees
            if level == 1:
                level_weights = [ENEMY_LEVEL_1] * 60 + [ENEMY_LEVEL_2] * 30 + [ENEMY_LEVEL_3] * 10
                bee_level = random.choice(level_weights)
            elif level == 2:
                level_weights = [ENEMY_LEVEL_1] * 30 + [ENEMY_LEVEL_2] * 50 + [ENEMY_LEVEL_3] * 20
                bee_level = random.choice(level_weights)
            else:  # Level 3
                level_weights = [ENEMY_LEVEL_1] * 10 + [ENEMY_LEVEL_2] * 30 + [ENEMY_LEVEL_3] * 40 + [ENEMY_LEVEL_4] * 20
                bee_level = random.choice(level_weights)

            new_bee = Bee(level=bee_level)
            self.all_sprites.add(new_bee)
            self.bees.add(new_bee)

    def handle_b_key(self):
        """Handle B key press for bomb"""
        # Use bomb directly here
        if self.player.bomb():
            # Create bomb effect
            bomb_effect = BombEffect(self.player.rect.center)
            self.all_sprites.add(bomb_effect)

            # Store bee data
            bee_data = []
            for bee in list(self.bees):
                bee_data.append((bee.rect.center, bee.points))

            # Increase score
            score_increase = sum(points for _, points in bee_data)
            self.score += score_increase

            # Remove all bees
            for bee in list(self.bees):
                bee.kill()

            # Create explosion effects
            for pos, _ in bee_data[:5]:
                explosion = Explosion(pos)
                self.all_sprites.add(explosion)
                self.explosions.add(explosion)

            # Generate new bees (increased from 3 to 6)
            for _ in range(6):
                new_bee = Bee()
                self.all_sprites.add(new_bee)
                self.bees.add(new_bee)

            # Force event processing to ensure keyboard input isn't blocked
            pygame.event.pump()

    def run(self):
        """Main game loop"""
        while self.running:
            # Keep loop running at the right speed
            self.clock.tick(FPS)

            # Process input (events)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False  # Exit the game

                # Custom event for boss redraw after flash
                elif event.type == pygame.USEREVENT + 1:
                    # Redraw boss if it exists and is alive
                    if self.boss_active and self.boss and self.boss.alive():
                        self.boss.redraw()
                    # Stop the timer
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Mouse click to shoot
                    bullets = self.player.shoot()
                    if bullets:
                        for bullet in bullets:
                            self.all_sprites.add(bullet)
                            self.bullets.add(bullet)

                elif event.type == pygame.KEYDOWN:
                    # Keyboard controls
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        return False

                    # Space to shoot
                    elif event.key == pygame.K_SPACE:
                        bullets = self.player.shoot()
                        if bullets:
                            for bullet in bullets:
                                self.all_sprites.add(bullet)
                                self.bullets.add(bullet)

                    # M to launch missile
                    elif event.key == pygame.K_m:
                        missiles = self.player.launch_missile()
                        if missiles:
                            for missile in missiles:
                                self.all_sprites.add(missile)
                                self.missiles_group.add(missile)

                                # Find closest bee for targeting
                                if self.bees and len(self.bees) > 0:
                                    try:
                                        # Get all bees that are on screen or just above it
                                        valid_targets = [bee for bee in self.bees.sprites()
                                                        if bee.rect.bottom > -50 and bee.rect.top < SCREEN_HEIGHT]

                                        if valid_targets:
                                            closest_bee = min(valid_targets,
                                                            key=lambda bee: ((bee.rect.centerx - missile.rect.centerx)**2 +
                                                                            (bee.rect.centery - missile.rect.centery)**2))
                                            missile.set_target(closest_bee)
                                            print(f"Missile launched and targeting {closest_bee.__class__.__name__} at {closest_bee.rect.center}")
                                        else:
                                            # No valid targets, try to find any bee
                                            closest_bee = min(self.bees.sprites(),
                                                            key=lambda bee: ((bee.rect.centerx - missile.rect.centerx)**2 +
                                                                            (bee.rect.centery - missile.rect.centery)**2))
                                            missile.set_target(closest_bee)
                                            print(f"Missile launched and targeting off-screen bee at {closest_bee.rect.center}")
                                    except (ValueError, AttributeError) as e:
                                        print(f"Error finding target for missile: {e}")
                                        # If there's an error, try to target the boss instead
                                        if self.boss_active and self.boss and self.boss.alive():
                                            missile.set_target(self.boss)
                                            print(f"Missile targeting boss instead at {self.boss.rect.center}")
                                # If no bees but boss is active, target the boss
                                elif self.boss_active and self.boss and self.boss.alive():
                                    missile.set_target(self.boss)
                                    print(f"Missile launched and targeting boss at {self.boss.rect.center}")
                                else:
                                    print("Missile launched but no targets available")

                    # Enter to restart after game over
                    elif event.key == pygame.K_RETURN and (self.game_over or self.victory):
                        # Reset game
                        self.__init__(self.args)
                        self.game_over = False
                        self.victory = False

                    # Detect B key for bomb with debounce
                    # Try multiple ways to detect B key
                    b_key_codes = [B_KEY, B_KEY_UPPER, K_b, pygame.K_b, 98, ord('b'), ord('B')]
                    if event.key in b_key_codes or pygame.key.name(event.key).lower() == 'b':
                        print("\n\n*** B KEY PRESSED IN EVENT HANDLER ***\n\n")

                        # Check debounce
                        now = pygame.time.get_ticks()
                        if now - self.last_b_key_time > self.b_key_debounce_time:
                            # Update last B key press time
                            self.last_b_key_time = now

                            # Use bomb
                            self.handle_b_key()

                            # Force event processing to ensure keyboard input isn't blocked
                            pygame.event.pump()

                            # Force update player position
                            keys = pygame.key.get_pressed()
                            if keys[K_LEFT] and self.player.rect.left > 0:
                                self.player.rect.x -= self.player.speed
                            if keys[K_RIGHT] and self.player.rect.right < SCREEN_WIDTH:
                                self.player.rect.x += self.player.speed
                            if keys[K_UP] and self.player.rect.top > 0:
                                self.player.rect.y -= self.player.speed
                            if keys[K_DOWN] and self.player.rect.bottom < SCREEN_HEIGHT:
                                self.player.rect.y += self.player.speed

            # Skip update if game over
            if self.game_over or self.victory:
                # Only update explosions and effects
                for sprite in self.all_sprites:
                    if isinstance(sprite, Explosion) or isinstance(sprite, BombEffect) or isinstance(sprite, VictoryEffect):
                        sprite.update()
            else:
                # Detect B key directly in game loop
                keys = pygame.key.get_pressed()
                now = pygame.time.get_ticks()

                # Print pressed keys once per second
                if self.debug_info and now % 1000 < 20:  # Only print once per second
                    pressed_keys = [i for i, pressed in enumerate(keys) if pressed]
                    if pressed_keys:
                        key_names = [pygame.key.name(k) for k in pressed_keys]
                        print(f"Currently pressed keys: {key_names}")
                        print(f"B key code (K_b): {K_b}")
                        print(f"B key pressed: {keys[K_b]}")

                # Detect B key with debounce mechanism
                # Try multiple ways to detect B key
                try:
                    # Detect all possible B key codes, including uppercase and lowercase
                    # All possible B key codes
                    b_key_codes = [B_KEY, B_KEY_UPPER, K_b, pygame.K_b, 98, ord('b'), ord('B')]
                    # Check if any B key is pressed
                    b_pressed = any(keys[code] for code in b_key_codes if code < len(keys))

                    # Print B key status
                    if self.debug_info and now % 1000 < 20:  # Only print once per second
                        print(f"B_KEY (lowercase): {B_KEY}, pressed: {keys[B_KEY] if B_KEY < len(keys) else 'out of range'}")
                        print(f"B_KEY_UPPER (uppercase): {B_KEY_UPPER}, pressed: {keys[B_KEY_UPPER] if B_KEY_UPPER < len(keys) else 'out of range'}")

                    # Handle B key press with debounce
                    if b_pressed and now - self.last_b_key_time > self.b_key_debounce_time:
                        self.last_b_key_time = now
                        self.handle_b_key()

                except Exception as e:
                    if self.debug_info:
                        print(f"Error detecting B key: {e}")

                # Auto-launch missiles if available
                now = pygame.time.get_ticks()
                if now - self.last_auto_missile_time > self.auto_missile_delay:
                    # Try to launch a missile
                    missiles = self.player.launch_missile(auto_launch=True)
                    if missiles:
                        self.last_auto_missile_time = now
                        for missile in missiles:
                            self.all_sprites.add(missile)
                            self.missiles_group.add(missile)

                            # Find closest bee for targeting
                            if self.bees and len(self.bees) > 0:
                                try:
                                    # Get all bees that are on screen or just above it
                                    valid_targets = [bee for bee in self.bees.sprites()
                                                    if bee.rect.bottom > -50 and bee.rect.top < SCREEN_HEIGHT]

                                    if valid_targets:
                                        closest_bee = min(valid_targets,
                                                        key=lambda bee: ((bee.rect.centerx - missile.rect.centerx)**2 +
                                                                        (bee.rect.centery - missile.rect.centery)**2))
                                        missile.set_target(closest_bee)
                                        print(f"Auto-missile targeting {closest_bee.__class__.__name__} at {closest_bee.rect.center}")
                                    else:
                                        # No valid targets, try to find any bee
                                        closest_bee = min(self.bees.sprites(),
                                                        key=lambda bee: ((bee.rect.centerx - missile.rect.centerx)**2 +
                                                                        (bee.rect.centery - missile.rect.centery)**2))
                                        missile.set_target(closest_bee)
                                        print(f"Auto-missile targeting off-screen bee at {closest_bee.rect.center}")
                                except (ValueError, AttributeError) as e:
                                    print(f"Error finding target for auto-missile: {e}")
                                    # If there's an error, try to target the boss instead
                                    if self.boss_active and self.boss and self.boss.alive():
                                        missile.set_target(self.boss)
                                        print(f"Auto-missile targeting boss instead at {self.boss.rect.center}")
                            # If no bees but boss is active, target the boss
                            elif self.boss_active and self.boss and self.boss.alive():
                                missile.set_target(self.boss)
                                print(f"Auto-missile targeting boss at {self.boss.rect.center}")
                            else:
                                print("Auto-missile launched but no targets available")

                # Update all sprites
                self.all_sprites.update()

                # Update missile targets if needed
                for missile in self.missiles_group:
                    # If missile has no target or target is no longer alive
                    if missile.target_seeking and (missile.target is None or not hasattr(missile.target, 'alive') or not missile.target.alive()):
                        # Find a new target
                        if self.bees and len(self.bees) > 0:
                            # Find closest bee
                            try:
                                closest_bee = min(self.bees.sprites(),
                                                key=lambda bee: ((bee.rect.centerx - missile.rect.centerx)**2 +
                                                                (bee.rect.centery - missile.rect.centery)**2))
                                missile.set_target(closest_bee)
                                print(f"Missile assigned target: {closest_bee.__class__.__name__} at {closest_bee.rect.center}")
                            except (ValueError, AttributeError) as e:
                                print(f"Error finding closest bee: {e}")
                                # If there's an error, try to target the boss instead
                                if self.boss_active and self.boss and self.boss.alive():
                                    missile.set_target(self.boss)
                                    print(f"Missile assigned boss target at {self.boss.rect.center}")
                        elif self.boss_active and self.boss and self.boss.alive():
                            # Target boss if no bees
                            missile.set_target(self.boss)
                            print(f"Missile assigned boss target at {self.boss.rect.center}")

                # Update background scroll position based on player movement
                # Use different speeds for different layers to create parallax effect
                player_move_speed_x = self.bg_scroll_speed * 1.5
                player_move_speed_y = self.bg_scroll_speed * 1.5

                if keys[K_LEFT]:
                    self.bg_scroll_x += player_move_speed_x
                if keys[K_RIGHT]:
                    self.bg_scroll_x -= player_move_speed_x
                if keys[K_UP]:
                    self.bg_scroll_y += player_move_speed_y
                if keys[K_DOWN]:
                    self.bg_scroll_y -= player_move_speed_y

                # Apply automatic vertical scrolling for high-speed flight effect
                # Increase the speed for more dramatic effect
                self.bg_scroll_y += self.bg_auto_scroll_speed * 1.5

                # Add some subtle horizontal drift for more dynamic effect
                # Use a combination of sine waves for more complex movement
                time_ms = pygame.time.get_ticks()
                self.bg_scroll_x += math.sin(time_ms / 2000) * 0.8 + math.sin(time_ms / 1000) * 0.3

                # Add occasional turbulence effect
                if random.random() < 0.01:  # 1% chance each frame
                    self.bg_scroll_x += random.uniform(-2, 2)
                    self.bg_scroll_y += random.uniform(-1, 1)

                # No need to wrap manually - our new rendering system handles this

                # Check for bullet-bee collisions
                hits = pygame.sprite.groupcollide(self.bullets, self.bees, True, False)
                for bullet, bees_hit in hits.items():
                    for bee in bees_hit:
                        if bee.hit(bullet.damage):
                            # Add score
                            self.score += bee.points

                            # Create explosion
                            explosion = Explosion(bee.rect.center)
                            self.all_sprites.add(explosion)
                            self.explosions.add(explosion)

                            # Play explosion sound
                            play_sound('explosion', channel='explosion')

                            # Random chance to spawn a power-up based on bee's drop chance
                            if random.random() < bee.drop_chance:
                                # Determine power-up type based on bee's drop weights and player's weapon level
                                weights = dict(bee.drop_weights)  # Copy the weights

                                # Adjust weapon_upgrade weight based on player's weapon level
                                if self.player.weapon_level >= WEAPON_LEVEL_5 and "weapon_upgrade" in weights:
                                    # Remove weapon upgrade if already at max level
                                    weights["weapon_upgrade"] = 0
                                elif self.player.weapon_level > WEAPON_LEVEL_1 and "weapon_upgrade" in weights:
                                    # Reduce weapon upgrade chance by 30% for each level above 1
                                    reduction_factor = 1.0 - (0.3 * (self.player.weapon_level - WEAPON_LEVEL_1))
                                    weights["weapon_upgrade"] = max(1, int(weights["weapon_upgrade"] * reduction_factor))

                                # Adjust missile_upgrade weight based on player's missile level
                                if self.player.missile_level >= MISSILE_LEVEL_4 and "missile_upgrade" in weights:
                                    # Reduce missile upgrade chance if already at max level
                                    weights["missile_upgrade"] = max(1, weights["missile_upgrade"] // 2)

                                # Create weighted choices list
                                powerup_choices = []
                                for ptype, weight in weights.items():
                                    if weight > 0:  # Only add types with weight > 0
                                        powerup_choices.extend([ptype] * weight)

                                # If no valid choices (unlikely), default to bomb
                                if not powerup_choices:
                                    powerup_type = "bomb"
                                else:
                                    powerup_type = random.choice(powerup_choices)

                                # Create power-up
                                powerup = PowerUp(bee.rect.center, powerup_type)
                                self.all_sprites.add(powerup)
                                self.powerups.add(powerup)

                            # Remove the bee
                            bee.kill()

                # Check for missile-bee collisions
                hits = pygame.sprite.groupcollide(self.missiles_group, self.bees, True, False)
                for missile, bees_hit in hits.items():
                    for bee in bees_hit:
                        if bee.hit(missile.damage):
                            # Add score
                            self.score += bee.points

                            # Create explosion
                            explosion = Explosion(bee.rect.center)
                            self.all_sprites.add(explosion)
                            self.explosions.add(explosion)

                            # Play explosion sound
                            play_sound('explosion', channel='explosion')

                            # Higher chance to spawn a power-up with missiles (1.5x normal drop rate)
                            if random.random() < (bee.drop_chance * 1.5):
                                # Determine power-up type with weighted probabilities favoring missiles
                                weights = dict(bee.drop_weights)  # Copy the weights

                                # Slightly increase missile weight
                                if "missile" in weights:
                                    weights["missile"] += 1

                                # Adjust weapon_upgrade weight based on player's weapon level
                                if self.player.weapon_level >= WEAPON_LEVEL_5 and "weapon_upgrade" in weights:
                                    # Remove weapon upgrade if already at max level
                                    weights["weapon_upgrade"] = 0
                                elif self.player.weapon_level > WEAPON_LEVEL_1 and "weapon_upgrade" in weights:
                                    # Reduce weapon upgrade chance by 30% for each level above 1
                                    reduction_factor = 1.0 - (0.3 * (self.player.weapon_level - WEAPON_LEVEL_1))
                                    weights["weapon_upgrade"] = max(1, int(weights["weapon_upgrade"] * reduction_factor))

                                # Adjust missile_upgrade weight based on player's missile level
                                if self.player.missile_level >= MISSILE_LEVEL_4 and "missile_upgrade" in weights:
                                    # Reduce missile upgrade chance if already at max level
                                    weights["missile_upgrade"] = max(1, weights["missile_upgrade"] // 2)

                                # Create weighted choices list
                                powerup_choices = []
                                for ptype, weight in weights.items():
                                    if weight > 0:  # Only add types with weight > 0
                                        powerup_choices.extend([ptype] * weight)

                                # If no valid choices (unlikely), default to bomb
                                if not powerup_choices:
                                    powerup_type = "bomb"
                                else:
                                    powerup_type = random.choice(powerup_choices)

                                # Create power-up
                                powerup = PowerUp(bee.rect.center, powerup_type)
                                self.all_sprites.add(powerup)
                                self.powerups.add(powerup)

                            # Remove the bee
                            bee.kill()

                # Check for player-powerup collisions
                hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
                for hit in hits:
                    # Apply power-up effect
                    if hit.type == "weapon_upgrade":
                        self.player.upgrade_weapon()
                    elif hit.type == "bomb":
                        self.player.add_bomb()
                    elif hit.type == "missile":
                        self.player.add_missile()
                    elif hit.type == "missile_upgrade":
                        self.player.upgrade_missile()

                # Check for bee-player collisions
                hits = pygame.sprite.spritecollide(self.player, self.bees, False)
                if hits and not self.game_over:
                    self.game_over = True
                    # Play game over sound
                    play_sound('game_over', channel='game_over', fade_ms=500)

                # Check if we need to spawn more bees
                if not self.boss_active and not self.game_over and not self.victory:
                    # If there are fewer than 3 bees, spawn more
                    if len(self.bees) < 3:
                        # Calculate how many bees to spawn
                        num_to_spawn = 5 + self.current_level * 2 - len(self.bees)

                        # Spawn new bees
                        for _ in range(num_to_spawn):
                            # Determine bee level based on current game level
                            if self.current_level == 1:
                                level_weights = [ENEMY_LEVEL_1] * 60 + [ENEMY_LEVEL_2] * 30 + [ENEMY_LEVEL_3] * 10
                            elif self.current_level == 2:
                                level_weights = [ENEMY_LEVEL_1] * 30 + [ENEMY_LEVEL_2] * 50 + [ENEMY_LEVEL_3] * 20
                            else:  # Level 3
                                level_weights = [ENEMY_LEVEL_1] * 10 + [ENEMY_LEVEL_2] * 30 + [ENEMY_LEVEL_3] * 40 + [ENEMY_LEVEL_4] * 20

                            bee_level = random.choice(level_weights)
                            new_bee = Bee(level=bee_level)
                            self.all_sprites.add(new_bee)
                            self.bees.add(new_bee)

                    # Level progression logic - check if score threshold reached to spawn boss
                    current_threshold = self.level_thresholds[self.current_level - 1]  # Arrays are 0-indexed
                    if self.score >= current_threshold:
                        # Spawn boss for current level
                        self.boss = Boss(self.current_level)
                        self.all_sprites.add(self.boss)
                        self.boss_active = True

                        # Clear regular bees when boss appears
                        for bee in list(self.bees):
                            bee.kill()

                # Boss battle logic
                if self.boss_active and self.boss.alive():
                    # Check for bullet-boss collisions
                    hits = pygame.sprite.spritecollide(self.boss, self.bullets, True)
                    for hit in hits:
                        if self.boss.hit(1):  # Boss defeated
                            # Add score
                            self.score += self.boss.points

                            # Remove boss from all sprite groups
                            self.boss.kill()
                            self.boss_active = False

                            # Create explosion
                            for _ in range(10):  # Multiple explosions for boss
                                pos = (self.boss.rect.centerx + random.randint(-50, 50),
                                      self.boss.rect.centery + random.randint(-50, 50))
                                explosion = Explosion(pos)
                                explosion_size = random.randint(30, 60)
                                explosion.image = pygame.transform.scale(explosion.image, (explosion_size, explosion_size))
                                self.all_sprites.add(explosion)
                                self.explosions.add(explosion)

                            # Play explosion sound
                            play_sound('explosion', channel='explosion2')

                            # Level completion logic
                            if self.current_level < self.max_level:
                                # Advance to next level
                                self.current_level += 1
                                self.level_complete = True

                                # Spawn bees for next level
                                self.spawn_bees_for_level(self.current_level)
                            else:
                                # Game completed - victory!
                                self.victory = True
                                victory_effect = VictoryEffect()
                                self.all_sprites.add(victory_effect)

                    # Check for missile-boss collisions
                    hits = pygame.sprite.spritecollide(self.boss, self.missiles_group, True)
                    for hit in hits:
                        if self.boss.hit(3):  # Missiles do more damage
                            # Same logic as above for boss defeat
                            self.score += self.boss.points

                            # Remove boss from all sprite groups
                            self.boss.kill()
                            self.boss_active = False

                            for _ in range(10):
                                pos = (self.boss.rect.centerx + random.randint(-50, 50),
                                      self.boss.rect.centery + random.randint(-50, 50))
                                explosion = Explosion(pos)
                                explosion_size = random.randint(30, 60)
                                explosion.image = pygame.transform.scale(explosion.image, (explosion_size, explosion_size))
                                self.all_sprites.add(explosion)
                                self.explosions.add(explosion)

                            play_sound('explosion', channel='explosion')

                            if self.current_level < self.max_level:
                                self.current_level += 1
                                self.level_complete = True
                                self.spawn_bees_for_level(self.current_level)
                            else:
                                self.victory = True
                                victory_effect = VictoryEffect()
                                self.all_sprites.add(victory_effect)

                    # Process boss attacks
                    if self.boss.alive():
                        # Check if boss has attacked
                        attack_bees = self.boss.attack()
                        if attack_bees:
                            # Add spawned bees to sprite groups
                            for bee in attack_bees:
                                self.all_sprites.add(bee)
                                self.bees.add(bee)

                # Update screen shake effect
                if self.screen_shake > 0:
                    self.screen_shake -= 1

            # Calculate screen shake offset
            shake_offset = (0, 0)
            if self.screen_shake > 0:
                shake_offset = (random.randint(-5, 5), random.randint(-5, 5))

            # Draw / render
            # Draw scrolling background with shake offset
            # Use modulo for seamless scrolling of the large background
            bg_width = self.background.get_width()
            bg_height = self.background.get_height()

            # Calculate the visible portion of the background
            # We use modulo to wrap around the background seamlessly
            view_x = int(self.bg_scroll_x) % bg_width
            view_y = int(self.bg_scroll_y) % bg_height

            # Draw the background in a way that ensures seamless scrolling
            # We need to draw up to 4 sections to cover the screen when scrolling
            self.screen.blit(self.background,
                           (-view_x + shake_offset[0],
                            -view_y + shake_offset[1]))

            # Draw additional sections if needed to cover the screen edges
            if view_x + SCREEN_WIDTH > bg_width:
                # Draw right section
                self.screen.blit(self.background,
                               (bg_width - view_x + shake_offset[0],
                                -view_y + shake_offset[1]))

            if view_y + SCREEN_HEIGHT > bg_height:
                # Draw bottom section
                self.screen.blit(self.background,
                               (-view_x + shake_offset[0],
                                bg_height - view_y + shake_offset[1]))

            if view_x + SCREEN_WIDTH > bg_width and view_y + SCREEN_HEIGHT > bg_height:
                # Draw bottom-right section
                self.screen.blit(self.background,
                               (bg_width - view_x + shake_offset[0],
                                bg_height - view_y + shake_offset[1]))

            # Draw moving nebula clouds (behind stars)
            for cloud in self.nebula_clouds:
                # Update cloud position
                cloud["pos"][0] += cloud["speed"][0]
                cloud["pos"][1] += cloud["speed"][1]

                # Wrap around screen edges
                if cloud["pos"][0] < -cloud["surf"].get_width():
                    cloud["pos"][0] = SCREEN_WIDTH
                elif cloud["pos"][0] > SCREEN_WIDTH:
                    cloud["pos"][0] = -cloud["surf"].get_width()

                if cloud["pos"][1] < -cloud["surf"].get_height():
                    cloud["pos"][1] = SCREEN_HEIGHT
                elif cloud["pos"][1] > SCREEN_HEIGHT:
                    cloud["pos"][1] = -cloud["surf"].get_height()

                # Draw the cloud
                self.screen.blit(cloud["surf"], (int(cloud["pos"][0]) + shake_offset[0], int(cloud["pos"][1]) + shake_offset[1]))

            # Draw twinkling stars with parallax effect
            for star in self.twinkle_stars:
                # Update star twinkle phase
                star["phase"] += star["twinkle_speed"]
                if star["phase"] > 2 * math.pi:
                    star["phase"] -= 2 * math.pi

                # Move star position for parallax effect (faster stars = closer to viewer)
                star["pos"][1] += star["move_speed"]  # Move down at varying speeds

                # Wrap around screen
                if star["pos"][1] > SCREEN_HEIGHT:
                    star["pos"][1] = 0
                    star["pos"][0] = random.randrange(0, SCREEN_WIDTH)

                # Calculate brightness based on sine wave
                brightness = int(127 * math.sin(star["phase"]) + 128)  # Range from 1 to 255
                color = (brightness, brightness, brightness)

                # Draw the star with current brightness
                # Larger/faster stars are brighter (closer to viewer)
                size_multiplier = 1.0 + (star["move_speed"] / 5.0) * 0.5
                pygame.draw.circle(self.screen, color,
                                 (int(star["pos"][0]) + shake_offset[0],
                                  int(star["pos"][1]) + shake_offset[1]),
                                 star["size"] * size_multiplier)

            # Draw all sprites
            for sprite in self.all_sprites:
                self.screen.blit(sprite.image, (sprite.rect.x + shake_offset[0], sprite.rect.y + shake_offset[1]))

            # Use smaller font for status displays
            small_font = pygame.font.Font(None, 24)  # Reduced from 36 to 24

            # Draw score
            score_text = small_font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))

            # Draw level indicator
            level_text = small_font.render(f"Level: {self.current_level}", True, WHITE)
            self.screen.blit(level_text, (10, 35))  # Adjusted position

            # Draw boss health bar if boss is active
            if self.boss_active and self.boss.alive():
                self.boss.draw_health_bar(self.screen)

            # Create a status panel in the top-right corner
            status_x = SCREEN_WIDTH - 120  # Moved closer to edge
            status_y_start = 10
            status_y_spacing = 25  # Reduced spacing

            # Draw missile count
            missile_text = small_font.render(f"Missiles: {self.player.missiles}", True, WHITE)
            self.screen.blit(missile_text, (status_x, status_y_start))

            # Draw bomb count
            bomb_text = small_font.render(f"Bombs: {self.player.bombs}", True, WHITE)
            self.screen.blit(bomb_text, (status_x, status_y_start + status_y_spacing))

            # Draw weapon level
            weapon_text = small_font.render(f"Weapon: Lv.{self.player.weapon_level}", True, WHITE)
            self.screen.blit(weapon_text, (status_x, status_y_start + status_y_spacing * 2))

            # Draw missile level
            missile_level_text = small_font.render(f"Missile: Lv.{self.player.missile_level}", True, WHITE)
            self.screen.blit(missile_level_text, (status_x, status_y_start + status_y_spacing * 3))

            # Draw game over message
            if self.game_over:
                # Use medium font for game over message (reduced from 74 to 60)
                medium_font = pygame.font.Font(None, 60)
                text = medium_font.render("GAME OVER", True, RED)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(text, text_rect)

                # Use small font for instructions (reduced from 36 to 28)
                small_font_2 = pygame.font.Font(None, 28)
                text = small_font_2.render("Press ENTER to play again", True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))  # Adjusted position
                self.screen.blit(text, text_rect)

            # After drawing everything, flip the display
            pygame.display.flip()

        pygame.quit()
