import textwrap

PYTHON_MAIN_GAME = textwrap.dedent("""
    import pygame
    import random
    import json
    import os
    from enum import Enum
    from typing import List, Tuple, Optional
    
    # Initialize Pygame - must be called before using any pygame functionality
    pygame.init()
    
    
    class Direction(Enum):
        \"\"\"Enum for snake movement directions. Using Enum prevents invalid direction values
        and makes the code more readable than using strings or magic numbers.\"\"\"
        UP = (0, -1)
        DOWN = (0, 1)
        LEFT = (-1, 0)
        RIGHT = (1, 0)
    
    
    class GameState(Enum):
        \"\"\"Game state machine states. This pattern makes it easy to control which
        logic runs and which graphics are displayed based on the current game state.\"\"\"
        MENU = "menu"
        PLAYING = "playing"
        PAUSED = "paused"
        GAME_OVER = "game_over"
    
    
    class Difficulty(Enum):
        \"\"\"Difficulty levels that control game speed. Higher FPS means faster snake movement,
        making the game more challenging. We use a tuple to store both display name and FPS.\"\"\"
        EASY = ("Easy", 8)
        MEDIUM = ("Medium", 12)
        HARD = ("Hard", 16)
        EXPERT = ("Expert", 20)
    
        @property
        def display_name(self) -> str:
            return self.value[0]
    
        @property
        def fps(self) -> int:
            return self.value[1]
    
    
    class Snake:
        \"\"\"Represents the snake entity in the game.
        
        The snake is stored as a list of (x, y) grid positions, where the head is at index 0.
        This makes it easy to add segments when growing and remove the tail when moving.
        \"\"\"
    
        def __init__(self, start_pos: Tuple[int, int], grid_size: int):
            \"\"\"Initialize snake at starting position.
            
            Args:
                start_pos: Initial (x, y) position on the grid
                grid_size: Size of each grid cell in pixels
            \"\"\"
            self.grid_size = grid_size
            # Start with 3 segments - head in the middle, tail going left
            self.body = [
                start_pos,
                (start_pos[0] - 1, start_pos[1]),
                (start_pos[0] - 2, start_pos[1])
            ]
            self.direction = Direction.RIGHT
            self.next_direction = Direction.RIGHT  # Buffer for direction changes
            self.growing = False  # Flag to indicate if snake should grow
    
        def set_direction(self, new_direction: Direction) -> None:
            \"\"\"Set the snake's direction, preventing 180-degree turns.
            
            We use next_direction as a buffer because the player might press keys faster
            than the game updates. This prevents the snake from reversing into itself.
            \"\"\"
            # Can't turn directly opposite to current direction (would hit ourselves)
            opposite_directions = {
                Direction.UP: Direction.DOWN,
                Direction.DOWN: Direction.UP,
                Direction.LEFT: Direction.RIGHT,
                Direction.RIGHT: Direction.LEFT
            }
            
            if new_direction != opposite_directions[self.direction]:
                self.next_direction = new_direction
    
        def move(self) -> None:
            \"\"\"Move the snake one grid cell in the current direction.
            
            Movement works by adding a new head in the direction of travel.
            If not growing, we remove the tail to maintain length.
            This creates the illusion of the snake sliding forward.
            \"\"\"
            # Apply buffered direction change
            self.direction = self.next_direction
            
            # Calculate new head position based on current direction
            head_x, head_y = self.body[0]
            dx, dy = self.direction.value
            new_head = (head_x + dx, head_y + dy)
            
            # Add new head at the front
            self.body.insert(0, new_head)
            
            # Remove tail unless we're growing
            if not self.growing:
                self.body.pop()
            else:
                self.growing = False  # Only grow for one frame
    
        def grow(self) -> None:
            \"\"\"Mark snake to grow on next move.
            
            We don't immediately add a segment because the new segment should appear
            where the tail currently is after the next move.
            \"\"\"
            self.growing = True
    
        def check_self_collision(self) -> bool:
            \"\"\"Check if snake's head collides with its body.
            
            Returns:
                True if head position matches any body segment (excluding head itself)
            \"\"\"
            head = self.body[0]
            # Check if head position appears anywhere in the body (after index 0)
            return head in self.body[1:]
    
        def check_wall_collision(self, grid_width: int, grid_height: int) -> bool:
            \"\"\"Check if snake hit the wall boundaries.
            
            Args:
                grid_width: Number of grid cells horizontally
                grid_height: Number of grid cells vertically
            
            Returns:
                True if head is outside the grid boundaries
            \"\"\"
            head_x, head_y = self.body[0]
            return head_x < 0 or head_x >= grid_width or head_y < 0 or head_y >= grid_height
    
        def draw(self, surface: pygame.Surface, offset_x: int, offset_y: int) -> None:
            \"\"\"Draw the snake on the game surface.
            
            Args:
                surface: Pygame surface to draw on
                offset_x: X pixel offset for centering the game grid
                offset_y: Y pixel offset for centering the game grid
            \"\"\"
            for i, (x, y) in enumerate(self.body):
                # Convert grid coordinates to pixel coordinates
                pixel_x = offset_x + x * self.grid_size
                pixel_y = offset_y + y * self.grid_size
                
                # Draw head slightly different color for visual clarity
                if i == 0:
                    color = (0, 200, 0)  # Bright green for head
                else:
                    color = (0, 150, 0)  # Darker green for body
                
                # Draw segment with a small margin for visual separation
                pygame.draw.rect(
                    surface,
                    color,
                    (pixel_x + 1, pixel_y + 1, self.grid_size - 2, self.grid_size - 2)
                )
    
    
    class Food:
        \"\"\"Represents food items that the snake can eat.
        
        Food spawns at random positions on the grid, avoiding the snake's body.
        \"\"\"
    
        def __init__(self, grid_width: int, grid_height: int, grid_size: int):
            self.grid_width = grid_width
            self.grid_height = grid_height
            self.grid_size = grid_size
            self.position = (0, 0)
    
        def spawn(self, snake_body: List[Tuple[int, int]]) -> None:
            \"\"\"Spawn food at a random position not occupied by the snake.
            
            Args:
                snake_body: List of (x, y) positions occupied by the snake
            \"\"\"
            while True:
                # Generate random grid position
                x = random.randint(0, self.grid_width - 1)
                y = random.randint(0, self.grid_height - 1)
                
                # Only accept position if it's not occupied by snake
                if (x, y) not in snake_body:
                    self.position = (x, y)
                    break
    
        def draw(self, surface: pygame.Surface, offset_x: int, offset_y: int) -> None:
            \"\"\"Draw the food as a red square.\"\"\"
            x, y = self.position
            pixel_x = offset_x + x * self.grid_size
            pixel_y = offset_y + y * self.grid_size
            
            pygame.draw.rect(
                surface,
                (200, 0, 0),  # Red color
                (pixel_x + 1, pixel_y + 1, self.grid_size - 2, self.grid_size - 2)
            )
    
    
    class Game:
        \"\"\"Main game class that manages game state, logic, and rendering.
        
        This follows the game loop pattern: process input -> update state -> render.
        The game loop runs continuously, with the frame rate controlled by pygame's clock.
        \"\"\"
    
        # Constants for game configuration
        WINDOW_WIDTH = 800
        WINDOW_HEIGHT = 600
        GRID_SIZE = 20  # Size of each grid cell in pixels
        GRID_WIDTH = 30  # Number of cells horizontally
        GRID_HEIGHT = 25  # Number of cells vertically
        HIGH_SCORE_FILE = "high_score.json"
    
        def __init__(self):
            \"\"\"Initialize the game window and game state.\"\"\"
            self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
            pygame.display.set_caption("Snake Game")
            self.clock = pygame.time.Clock()
            
            # Fonts for rendering text
            self.font_large = pygame.font.Font(None, 72)
            self.font_medium = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 24)
            
            # Game state
            self.state = GameState.MENU
            self.difficulty = Difficulty.MEDIUM
            self.score = 0
            self.high_scores = self.load_high_scores()
            
            # Calculate offset to center the grid on the screen
            self.grid_pixel_width = self.GRID_WIDTH * self.GRID_SIZE
            self.grid_pixel_height = self.GRID_HEIGHT * self.GRID_SIZE
            self.offset_x = (self.WINDOW_WIDTH - self.grid_pixel_width) // 2
            self.offset_y = (self.WINDOW_HEIGHT - self.grid_pixel_height) // 2
            
            # Game entities (will be initialized when starting game)
            self.snake: Optional[Snake] = None
            self.food: Optional[Food] = None
    
        def load_high_scores(self) -> dict:
            \"\"\"Load high scores from JSON file.
            
            Returns:
                Dictionary mapping difficulty names to high scores
            \"\"\"
            if os.path.exists(self.HIGH_SCORE_FILE):
                try:
                    with open(self.HIGH_SCORE_FILE, 'r') as f:
                        return json.load(f)
                except (json.JSONDecodeError, IOError):
                    # If file is corrupted, start fresh
                    return self.get_default_high_scores()
            return self.get_default_high_scores()
    
        def get_default_high_scores(self) -> dict:
            \"\"\"Get default high scores (all zeros).\"\"\"
            return {diff.display_name: 0 for diff in Difficulty}
    
        def save_high_scores(self) -> None:
            \"\"\"Save high scores to JSON file.\"\"\"
            try:
                with open(self.HIGH_SCORE_FILE, 'w') as f:
                    json.dump(self.high_scores, f, indent=2)
            except IOError:
                print("Warning: Could not save high scores")
    
        def update_high_score(self) -> None:
            \"\"\"Update high score if current score is higher.\"\"\"
            difficulty_name = self.difficulty.display_name
            if self.score > self.high_scores.get(difficulty_name, 0):
                self.high_scores[difficulty_name] = self.score
                self.save_high_scores()
    
        def start_game(self) -> None:
            \"\"\"Initialize a new game session.\"\"\"
            # Start snake in the middle of the grid
            start_x = self.GRID_WIDTH // 2
            start_y = self.GRID_HEIGHT // 2
            
            self.snake = Snake((start_x, start_y), self.GRID_SIZE)
            self.food = Food(self.GRID_WIDTH, self.GRID_HEIGHT, self.GRID_SIZE)
            self.food.spawn(self.snake.body)
            
            self.score = 0
            self.state = GameState.PLAYING
    
        def handle_menu_input(self, event: pygame.event.Event) -> None:
            \"\"\"Handle keyboard input in menu state.\"\"\"
            if event.key == pygame.K_SPACE:
                self.start_game()
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                # Cycle to previous difficulty
                difficulties = list(Difficulty)
                current_idx = difficulties.index(self.difficulty)
                self.difficulty = difficulties[(current_idx - 1) % len(difficulties)]
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                # Cycle to next difficulty
                difficulties = list(Difficulty)
                current_idx = difficulties.index(self.difficulty)
                self.difficulty = difficulties[(current_idx + 1) % len(difficulties)]
    
        def handle_playing_input(self, event: pygame.event.Event) -> None:
            \"\"\"Handle keyboard input during gameplay.\"\"\"
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.snake.set_direction(Direction.UP)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.snake.set_direction(Direction.DOWN)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.snake.set_direction(Direction.LEFT)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.snake.set_direction(Direction.RIGHT)
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                self.state = GameState.PAUSED
    
        def handle_paused_input(self, event: pygame.event.Event) -> None:
            \"\"\"Handle keyboard input in paused state.\"\"\"
            if event.key == pygame.K_SPACE or event.key == pygame.K_p:
                self.state = GameState.PLAYING
            elif event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU
    
        def handle_game_over_input(self, event: pygame.event.Event) -> None:
            \"\"\"Handle keyboard input in game over state.\"\"\"
            if event.key == pygame.K_SPACE:
                self.start_game()
            elif event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU
    
        def handle_events(self) -> bool:
            \"\"\"Process all pygame events.
            
            Returns:
                False if user wants to quit, True otherwise
            \"\"\"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                if event.type == pygame.KEYDOWN:
                    # Route input to appropriate handler based on game state
                    if self.state == GameState.MENU:
                        self.handle_menu_input(event)
                    elif self.state == GameState.PLAYING:
                        self.handle_playing_input(event)
                    elif self.state == GameState.PAUSED:
                        self.handle_paused_input(event)
                    elif self.state == GameState.GAME_OVER:
                        self.handle_game_over_input(event)
            
            return True
    
        def update(self) -> None:
            \"\"\"Update game logic. Only updates when in PLAYING state.\"\"\"
            if self.state != GameState.PLAYING:
                return
            
            # Move the snake
            self.snake.move()
            
            # Check for food collision
            if self.snake.body[0] == self.food.position:
                self.snake.grow()
                self.score += 10
                self.food.spawn(self.snake.body)
            
            # Check for game over conditions
            if self.snake.check_wall_collision(self.GRID_WIDTH, self.GRID_HEIGHT):
                self.update_high_score()
                self.state = GameState.GAME_OVER
            elif self.snake.check_self_collision():
                self.update_high_score()
                self.state = GameState.GAME_OVER
    
        def draw_grid(self) -> None:
            \"\"\"Draw the game grid background.\"\"\"
            # Draw grid cells with alternating colors for visual clarity
            for y in range(self.GRID_HEIGHT):
                for x in range(self.GRID_WIDTH):
                    # Checkerboard pattern
                    if (x + y) % 2 == 0:
                        color = (40, 40, 40)
                    else:
                        color = (50, 50, 50)
                    
                    pygame.draw.rect(
                        self.screen,
                        color,
                        (self.offset_x + x * self.GRID_SIZE,
                         self.offset_y + y * self.GRID_SIZE,
                         self.GRID_SIZE,
                         self.GRID_SIZE)
                    )
    
        def draw_text(self, text: str, font: pygame.font.Font, color: Tuple[int, int, int],
                      y: int, center: bool = True) -> None:
            \"\"\"Helper method to draw centered text.
            
            Args:
                text: Text to render
                font: Pygame font to use
                color: RGB color tuple
                y: Y position
                center: Whether to center horizontally
            \"\"\"
            surface = font.render(text, True, color)
            rect = surface.get_rect()
            if center:
                rect.centerx = self.WINDOW_WIDTH // 2
            rect.y = y
            self.screen.blit(surface, rect)
    
        def draw_menu(self) -> None:
            \"\"\"Draw the main menu screen.\"\"\"
            self.draw_text("SNAKE GAME", self.font_large, (0, 255, 0), 100)
            self.draw_text("Select Difficulty:", self.font_medium, (255, 255, 255), 220)
            
            # Draw difficulty options
            y_start = 280
            for i, diff in enumerate(Difficulty):
                color = (255, 255, 0) if diff == self.difficulty else (150, 150, 150)
                prefix = "> " if diff == self.difficulty else "  "
                high_score = self.high_scores.get(diff.display_name, 0)
                text = f"{prefix}{diff.display_name} - High Score: {high_score}"
                self.draw_text(text, self.font_small, color, y_start + i * 30)
            
            self.draw_text("Press SPACE to Start", self.font_small, (200, 200, 200), 480)
            self.draw_text("Use W/S or Arrow Keys to select difficulty", 
                          self.font_small, (150, 150, 150), 520)
    
        def draw_playing(self) -> None:
            \"\"\"Draw the game in playing state.\"\"\"
            self.draw_grid()
            self.food.draw(self.screen, self.offset_x, self.offset_y)
            self.snake.draw(self.screen, self.offset_x, self.offset_y)
            
            # Draw score
            score_text = f"Score: {self.score}"
            self.draw_text(score_text, self.font_small, (255, 255, 255), 10)
    
        def draw_paused(self) -> None:
            \"\"\"Draw the paused screen.\"\"\"
            # Draw game state behind semi-transparent overlay
            self.draw_playing()
            
            # Semi-transparent overlay
            overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            self.draw_text("PAUSED", self.font_large, (255, 255, 0), 200)
            self.draw_text("Press SPACE to Resume", self.font_small, (255, 255, 255), 320)
            self.draw_text("Press ESC for Menu", self.font_small, (255, 255, 255), 360)
    
        def draw_game_over(self) -> None:
            \"\"\"Draw the game over screen.\"\"\"
            self.draw_text("GAME OVER", self.font_large, (255, 0, 0), 150)
            self.draw_text(f"Final Score: {self.score}", self.font_medium, (255, 255, 255), 250)
            
            high_score = self.high_scores.get(self.difficulty.display_name, 0)
            self.draw_text(f"High Score: {high_score}", self.font_medium, (255, 255, 0), 300)
            
            self.draw_text("Press SPACE to Play Again", self.font_small, (200, 200, 200), 400)
            self.draw_text("Press ESC for Menu", self.font_small, (200, 200, 200), 440)
    
        def draw(self) -> None:
            \"\"\"Render the current game state.\"\"\"
            # Clear screen with black background
            self.screen.fill((0, 0, 0))
            
            # Route rendering to appropriate method based on game state
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.PLAYING:
                self.draw_playing()
            elif self.state == GameState.PAUSED:
                self.draw_paused()
            elif self.state == GameState.GAME_OVER:
                self.draw_game_over()
            
            # Update the display
            pygame.display.flip()
    
        def run(self) -> None:
            \"\"\"Main game loop. Runs until the player quits.
            
            This implements the classic game loop pattern:
            1. Handle input (events)
            2. Update game state
            3. Render graphics
            4. Control frame rate
            \"\"\"
            running = True
            while running:
                # Process input
                running = self.handle_events()
                
                # Update game logic
                self.update()
                
                # Render
                self.draw()
                
                # Control frame rate based on difficulty
                self.clock.tick(self.difficulty.fps)
            
            # Cleanup
            pygame.quit()
    
    
    if __name__ == "__main__":
        game = Game()
        game.run()
    """).strip()

PYTHON_TESTS_GAME = textwrap.dedent("""
    import pytest
    from main import Snake, Food, Direction, Game, GameState, Difficulty
    
    
    @pytest.fixture
    def snake():
        \"\"\"Fixture that creates a fresh Snake instance for each test.
        
        Fixtures prevent code duplication and ensure each test starts with clean state.
        This snake starts at position (5, 5) with a grid size of 20 pixels.
        \"\"\"
        return Snake(start_pos=(5, 5), grid_size=20)
    
    
    @pytest.fixture
    def food():
        \"\"\"Fixture that creates a fresh Food instance for each test.\"\"\"
        return Food(grid_width=20, grid_height=20, grid_size=20)
    
    
    @pytest.fixture
    def game():
        \"\"\"Fixture that creates a fresh Game instance for each test.\"\"\"
        return Game()
    
    
    class TestSnakeMovement:
        \"\"\"Test suite for snake movement logic.\"\"\"
    
        def test_snake_moves_right_by_default(self, snake):
            \"\"\"Test that snake initially moves right and position updates correctly.\"\"\"
            initial_head = snake.body[0]
            snake.move()
            new_head = snake.body[0]
            
            # Head should move one cell to the right (x increases by 1)
            assert new_head == (initial_head[0] + 1, initial_head[1])
    
        def test_snake_changes_direction(self, snake):
            \"\"\"Test that snake can change direction and moves accordingly.\"\"\"
            snake.set_direction(Direction.UP)
            initial_head = snake.body[0]
            snake.move()
            new_head = snake.body[0]
            
            # Head should move one cell up (y decreases by 1)
            assert new_head == (initial_head[0], initial_head[1] - 1)
    
        def test_snake_cannot_reverse_direction(self, snake):
            \"\"\"Test that snake cannot turn 180 degrees (prevents instant death).\"\"\"
            # Snake is moving right, try to turn left
            snake.set_direction(Direction.LEFT)
            snake.move()
            
            # Should still be moving right, not left
            # If it moved left, it would collide with its body
            assert snake.direction == Direction.RIGHT
    
        def test_snake_length_stays_same_when_not_growing(self, snake):
            \"\"\"Test that snake maintains constant length when moving without growing.\"\"\"
            initial_length = len(snake.body)
            snake.move()
            
            # Length should remain the same (new head added, tail removed)
            assert len(snake.body) == initial_length
    
    
    class TestSnakeGrowth:
        \"\"\"Test suite for snake growth mechanics.\"\"\"
    
        def test_snake_grows_when_eating(self, snake):
            \"\"\"Test that snake increases in length after eating food.\"\"\"
            initial_length = len(snake.body)
            
            # Simulate eating food
            snake.grow()
            snake.move()
            
            # Length should increase by 1
            assert len(snake.body) == initial_length + 1
    
        def test_snake_only_grows_once_per_food(self, snake):
            \"\"\"Test that grow() effect only lasts for one move.\"\"\"
            initial_length = len(snake.body)
            
            snake.grow()
            snake.move()  # Grows here
            snake.move()  # Should not grow here
            
            # Length should only increase by 1, not 2
            assert len(snake.body) == initial_length + 1
    
    
    class TestCollisionDetection:
        \"\"\"Test suite for collision detection logic.\"\"\"
    
        def test_wall_collision_detection(self, snake):
            \"\"\"Test that wall collision is detected when snake goes out of bounds.\"\"\"
            # Move snake to the left edge
            snake.body[0] = (0, 5)
            snake.set_direction(Direction.LEFT)
            snake.move()
            
            # Snake should be out of bounds (x = -1)
            assert snake.check_wall_collision(grid_width=20, grid_height=20)
    
        def test_no_wall_collision_in_bounds(self, snake):
            \"\"\"Test that no collision is detected when snake is within bounds.\"\"\"
            # Snake at (5, 5) should be well within a 20x20 grid
            assert not snake.check_wall_collision(grid_width=20, grid_height=20)
    
        def test_self_collision_detection(self, snake):
            \"\"\"Test that self-collision is detected when snake hits its own body.\"\"\"
            # Create a scenario where head collides with body
            # Manually set snake body to form a collision
            snake.body = [(5, 5), (5, 6), (4, 6), (4, 5), (5, 5)]
            
            # Last segment has same position as head
            assert snake.check_self_collision()
    
        def test_no_self_collision_normally(self, snake):
            \"\"\"Test that no self-collision is detected under normal conditions.\"\"\"
            # Default snake configuration should not have self-collision
            assert not snake.check_self_collision()
    
    
    class TestFoodSpawning:
        \"\"\"Test suite for food spawning mechanics.\"\"\"
    
        def test_food_spawns_on_grid(self, food):
            \"\"\"Test that food spawns within grid boundaries.\"\"\"
            snake_body = [(5, 5), (4, 5), (3, 5)]
            food.spawn(snake_body)
            
            x, y = food.position
            # Food should be within grid bounds
            assert 0 <= x < food.grid_width
            assert 0 <= y < food.grid_height
    
        def test_food_does_not_spawn_on_snake(self, food):
            \"\"\"Test that food never spawns on a position occupied by the snake.\"\"\"
            snake_body = [(5, 5), (4, 5), (3, 5)]
            food.spawn(snake_body)
            
            # Food position should not be any of the snake's body segments
            assert food.position not in snake_body
    
    
    class TestGameState:
        \"\"\"Test suite for game state management.\"\"\"
    
        def test_game_starts_in_menu(self, game):
            \"\"\"Test that game initializes in MENU state.\"\"\"
            assert game.state == GameState.MENU
    
        def test_starting_game_changes_state(self, game):
            \"\"\"Test that starting a game transitions to PLAYING state.\"\"\"
            game.start_game()
            assert game.state == GameState.PLAYING
    
        def test_starting_game_initializes_entities(self, game):
            \"\"\"Test that starting a game creates snake and food objects.\"\"\"
            game.start_game()
            
            assert game.snake is not None
            assert game.food is not None
            assert game.score == 0
    
    
    class TestScoring:
        \"\"\"Test suite for score tracking and high score persistence.\"\"\"
    
        def test_initial_score_is_zero(self, game):
            \"\"\"Test that score starts at zero.\"\"\"
            game.start_game()
            assert game.score == 0
    
        def test_high_score_updates(self, game):
            \"\"\"Test that high score updates when current score is higher.\"\"\"
            game.difficulty = Difficulty.EASY
            game.score = 100
            
            # Set initial high score lower than current score
            game.high_scores["Easy"] = 50
            game.update_high_score()
            
            # High score should be updated
            assert game.high_scores["Easy"] == 100
    
        def test_high_score_does_not_decrease(self, game):
            \"\"\"Test that high score is not overwritten by a lower score.\"\"\"
            game.difficulty = Difficulty.EASY
            game.score = 50
            
            # Set initial high score higher than current score
            game.high_scores["Easy"] = 100
            game.update_high_score()
            
            # High score should remain unchanged
            assert game.high_scores["Easy"] == 100
    """).strip()

README_PYTHON_TUTORIAL = textwrap.dedent("""
    # {name}
    
    Welcome to your Python Snake game! This tutorial project will teach you fundamental game development concepts using Python and Pygame.
    
    ## What You'll Learn
    
    - **Object-Oriented Programming (OOP)**: Creating classes like `Snake`, `Food`, and `Game` to organize code
    - **Game Loop Pattern**: The core pattern behind all real-time games (input → update → render)
    - **Event Handling**: Processing keyboard input and game events
    - **State Machines**: Managing different game states (menu, playing, paused, game over)
    - **Collision Detection**: Grid-based collision algorithms for walls and self-collision
    - **Data Persistence**: Saving and loading high scores with JSON
    - **Testing**: Writing unit tests with pytest
    
    ## Prerequisites
    
    - Python 3.8 or higher
    - Basic Python knowledge (variables, functions, classes)
    - Familiarity with the terminal/command line
    
    ## Quick Start
    
    1. **Set up a virtual environment** (recommended):
       ```bash
       python -m venv .venv
       source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
       ```
    
    2. **Install dependencies**:
       ```bash
       pip install -e .
       ```
    
    3. **Run the game**:
       ```bash
       python main.py
       ```
    
    4. **Play**:
       - Use arrow keys or WASD to control the snake
       - Press SPACE to start or restart
       - Press ESC to pause or return to menu
       - Select difficulty with W/S or Up/Down in the menu
    
    ## Project Structure
    
    ```
    {name}/
    ├── main.py              # Complete Snake game implementation
    ├── test_main.py         # Unit tests for game logic
    ├── pyproject.toml       # Project configuration and dependencies
    ├── high_score.json      # Persistent high score storage (created automatically)
    └── README.md            # This file
    ```
    
    ## Running the Game
    
    Simply execute:
    ```bash
    python main.py
    ```
    
    ### Controls
    - **Arrow Keys** or **WASD**: Move the snake
    - **SPACE**: Start game / Play again
    - **ESC** or **P**: Pause / Return to menu
    - **W/S** or **Up/Down**: Select difficulty in menu
    
    ### Gameplay
    - Eat the red food to grow and score points
    - Don't hit the walls or yourself
    - Each difficulty level increases snake speed
    - High scores are saved automatically for each difficulty
    
    ## Running Tests
    
    This project includes unit tests to verify game logic works correctly.
    
    **Run all tests**:
    ```bash
    pytest
    ```
    
    **Run with verbose output**:
    ```bash
    pytest -v
    ```
    
    **Run with coverage report**:
    ```bash
    pytest --cov=main --cov-report=term-missing
    ```
    
    The tests cover:
    - Snake movement and direction changes
    - Growth mechanics when eating food
    - Wall and self-collision detection
    - Food spawning logic
    - Game state transitions
    - Score tracking and high score updates
    
    ## Understanding the Code
    
    ### Object-Oriented Design
    
    The game uses classes to organize related data and behavior:
    
    - **`Snake` class**: Manages the snake's body, movement, and collision detection
    - **`Food` class**: Handles food spawning and rendering
    - **`Game` class**: Orchestrates the entire game (state management, game loop, rendering)
    
    This separation makes the code easier to understand, test, and extend.
    
    ### The Pygame Event Loop
    
    Pygame operates on an event-driven model. Events (like key presses, mouse clicks, or window closing) are queued and must be processed each frame:
    
    ```python
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # User closed the window
        elif event.type == pygame.KEYDOWN:
            # User pressed a key
    ```
    
    Not processing events causes the window to become unresponsive.
    
    ### The Game Loop Pattern
    
    The core game loop follows this pattern every frame:
    
    1. **Handle Input**: Process events (keyboard, mouse, etc.)
    2. **Update State**: Move snake, check collisions, update score
    3. **Render**: Draw everything to the screen
    4. **Control Timing**: Limit frame rate with `clock.tick(fps)`
    
    This pattern is universal across game engines and frameworks.
    
    ### State Machine
    
    The game uses a state machine to control behavior:
    
    - **MENU**: Display options, handle difficulty selection
    - **PLAYING**: Run game logic, process movement input
    - **PAUSED**: Freeze game, show pause overlay
    - **GAME_OVER**: Display final score, handle restart
    
    Each state has its own input handlers and rendering logic, preventing code from becoming tangled.
    
    ### Grid-Based Collision Detection
    
    The snake and food exist on a grid (e.g., 30×25 cells). Each position is a tuple `(x, y)`.
    
    **Food collision**: Check if snake head position equals food position
    ```python
    if snake.body[0] == food.position:
        # Collision!
    ```
    
    **Wall collision**: Check if head is outside grid bounds
    ```python
    if head_x < 0 or head_x >= grid_width:
        # Hit wall!
    ```
    
    **Self-collision**: Check if head position appears anywhere in body
    ```python
    if head in body[1:]:
        # Hit self!
    ```
    
    Grid-based collision is simple and efficient for tile-based games.
    
    ## How to Extend This Game
    
    Here are some ideas to make the game your own:
    
    ### 1. Add Obstacles
    Create an `Obstacle` class with random static positions that end the game on collision.
    
    ### 2. Portal Mechanics
    Add portals that teleport the snake from one edge to the opposite edge instead of hitting a wall.
    
    ### 3. Special Food Types
    - **Golden food**: Worth more points but rare
    - **Speed boost**: Temporarily increases snake speed
    - **Shrink food**: Removes a segment from the tail
    
    ### 4. Combo System
    Track consecutive food collection without changing direction for bonus multipliers.
    
    ### 5. Sound Effects
    Use `pygame.mixer` to add sounds for eating, collision, and background music.
    
    ### 6. Persistent Leaderboard
    Expand `high_score.json` to store names and multiple scores, then display a top 10 list.
    
    ### 7. Visual Enhancements
    - Add sprites instead of colored rectangles
    - Particle effects when eating food
    - Screen shake on collision
    - Smooth movement animation between grid cells
    
    ### 8. AI Mode
    Implement pathfinding (like A* or BFS) to create an AI-controlled snake that can play automatically.
    
    ## Tips for Development
    
    - **Test frequently**: Run the game after small changes to catch bugs early
    - **Use print statements**: Debug by printing variables when something doesn't work
    - **Read Pygame docs**: https://www.pygame.org/docs/
    - **Experiment**: Change numbers (speed, grid size, colors) to see what happens
    
    ## Learn More
    
    - **Pygame Documentation**: https://www.pygame.org/docs/
    - **Python Testing with pytest**: https://docs.pytest.org/
    - **Game Programming Patterns**: https://gameprogrammingpatterns.com/
    
    ## License
    
    This tutorial project is free to use, modify, and learn from. Have fun!
    """).strip()

PYPROJECT_TOML_TUTORIAL = textwrap.dedent("""
    [project]
    name = "{name}"
    version = "0.1.0"
    description = "A Snake game built with Pygame - tutorial project"
    requires-python = ">=3.8"
    
    # Runtime dependencies - required to run the game
    dependencies = [
        "pygame>=2.5.0",
    ]
    
    # Development dependencies - required for testing and development
    [project.optional-dependencies]
    dev = [
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
    ]
    
    # Build system configuration
    [build-system]
    requires = ["setuptools>=65.0"]
    build-backend = "setuptools.build_meta"
    
    # Pytest configuration
    [tool.pytest.ini_options]
    testpaths = ["test_main.py"]  # Where to find tests
    python_files = ["test_*.py"]  # Test file naming pattern
    python_classes = ["Test*"]    # Test class naming pattern
    python_functions = ["test_*"] # Test function naming pattern
    
    # Coverage configuration
    [tool.coverage.run]
    source = ["."]  # Measure coverage for files in current directory
    omit = [
        "test_*.py",  # Don't measure coverage of test files themselves
        ".venv/*",    # Ignore virtual environment
    ]
    """).strip()

GITIGNORE_PYTHON_TUTORIAL = textwrap.dedent("""
    # Python compiled files
    __pycache__/
    *.py[cod]
    *$py.class
    *.so
    
    # Virtual environments
    .venv/
    venv/
    ENV/
    env/
    
    # Distribution / packaging
    dist/
    build/
    *.egg-info/
    
    # Testing
    .pytest_cache/
    .coverage
    htmlcov/
    .tox/
    
    # IDEs and editors
    .vscode/
    .idea/
    *.swp
    *.swo
    *~
    .DS_Store
    
    # Game-specific
    high_score.json
    
    # Logs
    *.log
    """).strip()
