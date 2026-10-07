import os
import pygame
from .player import Player
from .platform import Platform
from .hazard import Hazard

# Game Engine

WHITE = (255, 255, 255)
BROWN = (150, 100, 60)
RED = (220, 60, 60)
GREEN = (0, 200, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.gravity = 0.6

        self.start_x, self.start_y = 40, height - 120
        self.player = Player(self.start_x, self.start_y)

        # A simple hand-built level: platforms with gaps between them
        # (falling into a gap means falling off the bottom of the
        # screen), one hazard, and a goal near the right edge.
        ground_y = height - 40
        self.platforms = [
            Platform(0, ground_y, 160),
            Platform(220, ground_y, 140),
            Platform(420, ground_y - 60, 120),
            Platform(600, ground_y, 180),
        ]
        self.hazards = [Hazard(240, ground_y - 14, 100)]
        self.goal_x = 740

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over = False
        self.exit_requested = False

        # Task 3 menu state.
        self.difficulty_selection = False
        self.game_over_option = 0  # 0 = Play Again, 1 = Exit
        self.difficulty_option = 1  # 0 = Easy, 1 = Medium, 2 = Hard
        self.difficulty_names = ("Easy", "Medium", "Hard")

        self.game_over_font = pygame.font.SysFont("Arial", 56)
        self.game_over_small_font = pygame.font.SysFont("Arial", 28)
        self.menu_font = pygame.font.SysFont("Arial", 32)

        # Task 4: optional sound effects. Missing files or unavailable audio
        # hardware do not prevent the game from running.
        self.sounds = {}
        self._load_sounds()

    def _load_sounds(self):
        sound_files = {
            "jump": "jump.wav",
            "goal": "goal.wav",
            "death": "death.wav",
        }
        sound_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sounds")

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            for name, filename in sound_files.items():
                path = os.path.join(sound_dir, filename)
                if os.path.exists(path):
                    self.sounds[name] = pygame.mixer.Sound(path)
        except (pygame.error, OSError):
            # Audio is optional; gameplay continues normally without it.
            self.sounds.clear()

    def _play_sound(self, name):
        sound = self.sounds.get(name)
        if sound is not None:
            try:
                sound.play()
            except pygame.error:
                pass

    def _set_game_over(self):
        if not self.game_over:
            self.game_over = True
            self._play_sound("death")

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if self.game_over:
            if self.difficulty_selection:
                # Difficulty selection screen.
                if event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_UP, pygame.K_w):
                    self.difficulty_option = (self.difficulty_option - 1) % 3
                elif event.key in (pygame.K_RIGHT, pygame.K_d, pygame.K_DOWN, pygame.K_s):
                    self.difficulty_option = (self.difficulty_option + 1) % 3
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    self.start_new_game(self.difficulty_option)
                elif event.key == pygame.K_ESCAPE:
                    self.difficulty_selection = False
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    self.difficulty_option = event.key - pygame.K_1
                    self.start_new_game(self.difficulty_option)
                return

            # Game Over menu.
            if event.key in (pygame.K_UP, pygame.K_w, pygame.K_LEFT, pygame.K_a,
                             pygame.K_DOWN, pygame.K_s, pygame.K_RIGHT, pygame.K_d):
                if event.key in (pygame.K_UP, pygame.K_w, pygame.K_LEFT, pygame.K_a):
                    self.game_over_option = 0
                else:
                    self.game_over_option = 1
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                if self.game_over_option == 0:
                    self.difficulty_selection = True
                    self.difficulty_option = 1
                else:
                    self.exit_requested = True
            elif event.key == pygame.K_ESCAPE:
                self.exit_requested = True
            return

        if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
            was_on_ground = self.player.on_ground
            self.player.jump()
            if was_on_ground and not self.player.on_ground:
                self._play_sound("jump")

    def start_new_game(self, difficulty):
        # Keep the existing level intact; only reset the current run.
        settings = (
            (0.45, -11),  # Easy
            (0.60, -12),  # Medium
            (0.80, -13),  # Hard
        )
        self.gravity, self.player.jump_strength = settings[difficulty]

        self.player.x = self.start_x
        self.player.y = self.start_y
        self.player.vx = 0
        self.player.vy = 0
        self.player.on_ground = False

        self.score = 0
        self.game_over = False
        self.difficulty_selection = False
        self.game_over_option = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.player.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.vx = -self.player.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.vx = self.player.speed

    def update(self):
        if self.game_over:
            return

        self.player.vy += self.gravity
        self.player.x = max(0, self.player.x + self.player.vx)

        # Store the previous bottom before moving vertically. This lets us
        # detect when the player crosses a platform top during a fast fall,
        # even if the player moves through the platform between frames.
        previous_bottom = self.player.y + self.player.height
        self.player.y += self.player.vy
        current_bottom = self.player.y + self.player.height

        self.player.on_ground = False
        if self.player.vy >= 0:
            for platform in self.platforms:
                platform_rect = platform.rect()

                # The player must overlap the platform horizontally and
                # cross its top surface while moving downward.
                horizontal_overlap = (
                    self.player.x < platform_rect.right
                    and self.player.x + self.player.width > platform_rect.left
                )
                crossed_platform_top = (
                    previous_bottom <= platform_rect.top
                    and current_bottom >= platform_rect.top
                )

                if horizontal_overlap and crossed_platform_top:
                    self.player.y = platform_rect.top - self.player.height
                    self.player.vy = 0
                    self.player.on_ground = True
                    break

        for hazard in self.hazards:
            if self.player.rect().colliderect(hazard.rect()):
                self._set_game_over()
                return

        if self.player.y > self.height:
            self._set_game_over()
            return

        if self.player.x >= self.goal_x:
            self.score += 1
            self._play_sound("goal")
            self.player.x, self.player.y = self.start_x, self.start_y
            self.player.vy = 0

    def render(self, screen):
        for platform in self.platforms:
            pygame.draw.rect(screen, BROWN, platform.rect())
        for hazard in self.hazards:
            pygame.draw.rect(screen, RED, hazard.rect())

        goal_rect = pygame.Rect(self.goal_x, 0, 6, self.height)
        pygame.draw.rect(screen, GREEN, goal_rect)

        pygame.draw.rect(screen, WHITE, self.player.rect())

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.game_over:
            # Dark overlay keeps the final game state visible while clearly
            # separating menus from normal gameplay.
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            screen.blit(overlay, (0, 0))

            if self.difficulty_selection:
                title = self.game_over_font.render("SELECT DIFFICULTY", True, WHITE)
                screen.blit(
                    title,
                    title.get_rect(center=(self.width // 2, self.height // 2 - 100))
                )

                for index, name in enumerate(self.difficulty_names):
                    label = name
                    if index == self.difficulty_option:
                        label = f"> {name} <"
                    text = self.menu_font.render(label, True, WHITE)
                    screen.blit(
                        text,
                        text.get_rect(center=(
                            self.width // 2,
                            self.height // 2 - 30 + index * 50
                        ))
                    )

                prompt = self.game_over_small_font.render(
                    "Arrow keys + Enter   |   1/2/3 to choose   |   Esc to go back",
                    True,
                    WHITE,
                )
                screen.blit(
                    prompt,
                    prompt.get_rect(center=(self.width // 2, self.height - 45))
                )
            else:
                title = self.game_over_font.render("GAME OVER", True, WHITE)
                score = self.game_over_small_font.render(
                    f"Final Score: {self.score}", True, WHITE
                )
                screen.blit(
                    title,
                    title.get_rect(center=(self.width // 2, self.height // 2 - 100))
                )
                screen.blit(
                    score,
                    score.get_rect(center=(self.width // 2, self.height // 2 - 35))
                )

                options = ("Play Again", "Exit")
                for index, option in enumerate(options):
                    label = option
                    if index == self.game_over_option:
                        label = f"> {option} <"
                    text = self.menu_font.render(label, True, WHITE)
                    screen.blit(
                        text,
                        text.get_rect(center=(
                            self.width // 2,
                            self.height // 2 + 25 + index * 50
                        ))
                    )

                prompt = self.game_over_small_font.render(
                    "Arrow keys + Enter   |   Esc to exit",
                    True,
                    WHITE,
                )
                screen.blit(
                    prompt,
                    prompt.get_rect(center=(self.width // 2, self.height - 45))
                )
