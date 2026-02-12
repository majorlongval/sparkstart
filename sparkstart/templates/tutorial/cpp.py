import textwrap

CPP_MAIN_GAME = textwrap.dedent('''
    #include <raylib.h>
    #include <vector>
    #include <string>
    #include <cmath>
    
    // Game configuration constants
    // These are defined as constants to make the game easy to tune and modify
    const int SCREEN_WIDTH = 800;
    const int SCREEN_HEIGHT = 600;
    const int PADDLE_WIDTH = 100;
    const int PADDLE_HEIGHT = 20;
    const int PADDLE_SPEED = 8;
    const int BALL_RADIUS = 8;
    const float BALL_SPEED = 5.0f;
    const int BRICK_WIDTH = 75;
    const int BRICK_HEIGHT = 20;
    const int BRICK_ROWS = 5;
    const int BRICK_COLS = 10;
    const int BRICK_OFFSET_X = 5;
    const int BRICK_OFFSET_Y = 50;
    const int BRICK_SPACING = 5;
    
    // Game states help organize the flow of the game
    // Using an enum makes the code more readable than magic numbers
    enum class GameState {
        MENU,      // Start screen
        PLAYING,   // Active gameplay
        WIN,       // Player wins when all bricks are destroyed
        LOSE       // Player loses when ball falls below paddle
    };
    
    // Brick structure to track individual brick state
    // Using a struct keeps related data together and makes code cleaner
    struct Brick {
        Rectangle rect;    // Position and size of the brick
        bool active;       // Whether the brick is still in play (not destroyed)
        Color color;       // Visual appearance of the brick
        int points;        // Score value when destroyed
        
        // Constructor with default values for easy initialization
        Brick() : active(false), color(RED), points(10) {}
    };
    
    // Paddle represents the player-controlled object at the bottom
    struct Paddle {
        Rectangle rect;
        float speed;
        
        Paddle(float x, float y, float width, float height, float spd) {
            rect = { x, y, width, height };
            speed = spd;
        }
        
        // Update paddle position based on keyboard input
        // We clamp the position to prevent the paddle from going off-screen
        void Update() {
            // Check left/right arrow keys or A/D keys for movement
            if ((IsKeyDown(KEY_LEFT) || IsKeyDown(KEY_A)) && rect.x > 0) {
                rect.x -= speed;
            }
            if ((IsKeyDown(KEY_RIGHT) || IsKeyDown(KEY_D)) && 
                rect.x < SCREEN_WIDTH - rect.width) {
                rect.x += speed;
            }
        }
        
        void Draw() const {
            DrawRectangleRec(rect, BLUE);
        }
    };
    
    // Ball handles the main game object that bounces around
    struct Ball {
        Vector2 position;
        Vector2 velocity;
        float radius;
        bool active;       // Ball is only active during gameplay
        
        Ball(float x, float y, float r) {
            position = { x, y };
            velocity = { 0, 0 };
            radius = r;
            active = false;
        }
        
        // Launch the ball with an initial upward velocity
        // We use a slight angle to make the game more interesting
        void Launch() {
            if (!active) {
                active = true;
                // Launch at an angle (not straight up) to avoid boring vertical bouncing
                velocity.x = BALL_SPEED * 0.7f;
                velocity.y = -BALL_SPEED;
            }
        }
        
        // Reset ball to starting position (when player loses a life)
        void Reset(float x, float y) {
            position.x = x;
            position.y = y;
            velocity.x = 0;
            velocity.y = 0;
            active = false;
        }
        
        // Update ball physics each frame
        void Update() {
            if (!active) return;
            
            // Apply velocity to position (basic physics)
            position.x += velocity.x;
            position.y += velocity.y;
            
            // Wall collision detection - bounce off left and right walls
            // We reverse the x-velocity to simulate a bounce
            if (position.x - radius <= 0 || position.x + radius >= SCREEN_WIDTH) {
                velocity.x *= -1;
                // Clamp position to prevent ball from getting stuck in wall
                position.x = Clamp(position.x, radius, SCREEN_WIDTH - radius);
            }
            
            // Ceiling collision - bounce off top
            if (position.y - radius <= 0) {
                velocity.y *= -1;
                position.y = radius;
            }
        }
        
        // Check if ball has fallen below the paddle (lose condition)
        bool IsBelowScreen() const {
            return position.y - radius > SCREEN_HEIGHT;
        }
        
        void Draw() const {
            DrawCircleV(position, radius, WHITE);
        }
    };
    
    // Game class encapsulates all game logic and state
    class Game {
    private:
        GameState state;
        Paddle paddle;
        Ball ball;
        std::vector<Brick> bricks;
        int score;
        int activeBricks;
        
    public:
        Game() : 
            state(GameState::MENU),
            paddle(SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2, 
                   SCREEN_HEIGHT - 40, 
                   PADDLE_WIDTH, 
                   PADDLE_HEIGHT, 
                   PADDLE_SPEED),
            ball(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BALL_RADIUS),
            score(0),
            activeBricks(0) {
            InitBricks();
        }
        
        // Initialize the brick grid at the top of the screen
        // We create a colorful pattern and assign point values
        void InitBricks() {
            bricks.clear();
            activeBricks = 0;
            
            // Colors for different rows - makes the game more visually appealing
            Color rowColors[] = { RED, ORANGE, YELLOW, GREEN, BLUE };
            
            for (int row = 0; row < BRICK_ROWS; row++) {
                for (int col = 0; col < BRICK_COLS; col++) {
                    Brick brick;
                    
                    // Calculate brick position based on row and column
                    // We add spacing between bricks for visual clarity
                    float x = BRICK_OFFSET_X + col * (BRICK_WIDTH + BRICK_SPACING);
                    float y = BRICK_OFFSET_Y + row * (BRICK_HEIGHT + BRICK_SPACING);
                    
                    brick.rect = { x, y, BRICK_WIDTH, BRICK_HEIGHT };
                    brick.active = true;
                    brick.color = rowColors[row % 5];
                    
                    // Higher rows are worth more points (they're harder to reach)
                    brick.points = (BRICK_ROWS - row) * 10;
                    
                    bricks.push_back(brick);
                    activeBricks++;
                }
            }
        }
        
        // Reset game state for a new game
        void ResetGame() {
            score = 0;
            ball.Reset(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2);
            paddle.rect.x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2;
            InitBricks();
            state = GameState::PLAYING;
        }
        
        // Main game update loop - called every frame
        void Update() {
            switch (state) {
                case GameState::MENU:
                    // Wait for player to press SPACE to start
                    if (IsKeyPressed(KEY_SPACE)) {
                        ResetGame();
                    }
                    break;
                    
                case GameState::PLAYING:
                    UpdatePlaying();
                    break;
                    
                case GameState::WIN:
                case GameState::LOSE:
                    // Allow player to restart after win/lose
                    if (IsKeyPressed(KEY_SPACE)) {
                        ResetGame();
                    }
                    // Return to menu with ESC
                    if (IsKeyPressed(KEY_ESCAPE)) {
                        state = GameState::MENU;
                    }
                    break;
            }
        }
        
        // Update logic during active gameplay
        void UpdatePlaying() {
            // Launch ball when player presses SPACE
            if (IsKeyPressed(KEY_SPACE)) {
                ball.Launch();
            }
            
            // Update game objects
            paddle.Update();
            ball.Update();
            
            // Check collision between ball and paddle
            // This is crucial for gameplay - if ball hits paddle, it bounces back up
            if (ball.active && CheckCollisionCircleRec(ball.position, ball.radius, paddle.rect)) {
                // Only bounce if ball is moving downward (prevents sticky paddle)
                if (ball.velocity.y > 0) {
                    ball.velocity.y *= -1;
                    
                    // Add horizontal influence based on where ball hits paddle
                    // This gives the player more control and makes gameplay more interesting
                    float hitPos = (ball.position.x - paddle.rect.x) / paddle.rect.width;
                    float influence = (hitPos - 0.5f) * 2.0f; // Range: -1 to 1
                    ball.velocity.x += influence * 3.0f;
                    
                    // Clamp ball speed to prevent it from getting too fast
                    float speed = sqrt(ball.velocity.x * ball.velocity.x + 
                                     ball.velocity.y * ball.velocity.y);
                    if (speed > BALL_SPEED * 2) {
                        ball.velocity.x = (ball.velocity.x / speed) * BALL_SPEED * 2;
                        ball.velocity.y = (ball.velocity.y / speed) * BALL_SPEED * 2;
                    }
                }
            }
            
            // Check collision between ball and bricks
            CheckBrickCollisions();
            
            // Check win condition - all bricks destroyed
            if (activeBricks == 0) {
                state = GameState::WIN;
            }
            
            // Check lose condition - ball fell below paddle
            if (ball.IsBelowScreen()) {
                state = GameState::LOSE;
            }
        }
        
        // Brick collision detection and response
        // This is one of the most important functions in the game
        void CheckBrickCollisions() {
            if (!ball.active) return;
            
            for (auto& brick : bricks) {
                // Skip inactive (already destroyed) bricks
                if (!brick.active) continue;
                
                // Check if ball intersects with brick rectangle
                if (CheckCollisionCircleRec(ball.position, ball.radius, brick.rect)) {
                    // Deactivate the brick and increase score
                    brick.active = false;
                    activeBricks--;
                    score += brick.points;
                    
                    // Determine which side of the brick was hit
                    // This allows for realistic bouncing behavior
                    Vector2 brickCenter = {
                        brick.rect.x + brick.rect.width / 2,
                        brick.rect.y + brick.rect.height / 2
                    };
                    
                    Vector2 difference = {
                        ball.position.x - brickCenter.x,
                        ball.position.y - brickCenter.y
                    };
                    
                    // Calculate which axis has the greater difference
                    // This tells us if we hit the brick from the side or top/bottom
                    float ratioX = abs(difference.x) / (brick.rect.width / 2);
                    float ratioY = abs(difference.y) / (brick.rect.height / 2);
                    
                    if (ratioX > ratioY) {
                        // Hit from left or right - reverse horizontal velocity
                        ball.velocity.x *= -1;
                    } else {
                        // Hit from top or bottom - reverse vertical velocity
                        ball.velocity.y *= -1;
                    }
                    
                    // Only check one brick collision per frame to prevent issues
                    // (ball destroying multiple bricks in one frame can cause weird bounces)
                    break;
                }
            }
        }
        
        // Render all game objects
        void Draw() {
            BeginDrawing();
            ClearBackground(BLACK);
            
            switch (state) {
                case GameState::MENU:
                    DrawMenu();
                    break;
                    
                case GameState::PLAYING:
                    DrawGame();
                    break;
                    
                case GameState::WIN:
                    DrawGame();
                    DrawWinScreen();
                    break;
                    
                case GameState::LOSE:
                    DrawGame();
                    DrawLoseScreen();
                    break;
            }
            
            EndDrawing();
        }
        
        void DrawMenu() {
            const char* title = "BRICK BREAKER";
            const char* subtitle = "Press SPACE to Start";
            
            int titleWidth = MeasureText(title, 60);
            int subtitleWidth = MeasureText(subtitle, 30);
            
            DrawText(title, SCREEN_WIDTH / 2 - titleWidth / 2, 200, 60, WHITE);
            DrawText(subtitle, SCREEN_WIDTH / 2 - subtitleWidth / 2, 300, 30, GRAY);
            
            // Draw controls
            DrawText("Controls:", 50, 400, 25, WHITE);
            DrawText("Arrow Keys / A & D - Move Paddle", 50, 435, 20, LIGHTGRAY);
            DrawText("SPACE - Launch Ball", 50, 460, 20, LIGHTGRAY);
        }
        
        void DrawGame() {
            // Draw all active bricks
            for (const auto& brick : bricks) {
                if (brick.active) {
                    DrawRectangleRec(brick.rect, brick.color);
                    // Draw a border for better visual definition
                    DrawRectangleLinesEx(brick.rect, 2, BLACK);
                }
            }
            
            // Draw game objects
            paddle.Draw();
            ball.Draw();
            
            // Draw score at top
            std::string scoreText = "Score: " + std::to_string(score);
            DrawText(scoreText.c_str(), 10, 10, 25, WHITE);
            
            // Draw remaining bricks count
            std::string bricksText = "Bricks: " + std::to_string(activeBricks);
            DrawText(bricksText.c_str(), SCREEN_WIDTH - 150, 10, 25, WHITE);
            
            // Draw hint if ball not launched yet
            if (!ball.active) {
                const char* hint = "Press SPACE to launch ball";
                int width = MeasureText(hint, 20);
                DrawText(hint, SCREEN_WIDTH / 2 - width / 2, 
                        SCREEN_HEIGHT / 2 + 50, 20, YELLOW);
            }
        }
        
        void DrawWinScreen() {
            // Semi-transparent overlay
            DrawRectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, Fade(BLACK, 0.7f));
            
            const char* winText = "YOU WIN!";
            const char* scoreText = TextFormat("Final Score: %d", score);
            const char* restartText = "Press SPACE to play again";
            
            int winWidth = MeasureText(winText, 60);
            int scoreWidth = MeasureText(scoreText, 30);
            int restartWidth = MeasureText(restartText, 25);
            
            DrawText(winText, SCREEN_WIDTH / 2 - winWidth / 2, 200, 60, GREEN);
            DrawText(scoreText, SCREEN_WIDTH / 2 - scoreWidth / 2, 280, 30, WHITE);
            DrawText(restartText, SCREEN_WIDTH / 2 - restartWidth / 2, 350, 25, GRAY);
        }
        
        void DrawLoseScreen() {
            // Semi-transparent overlay
            DrawRectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, Fade(BLACK, 0.7f));
            
            const char* loseText = "GAME OVER";
            const char* scoreText = TextFormat("Final Score: %d", score);
            const char* restartText = "Press SPACE to try again";
            
            int loseWidth = MeasureText(loseText, 60);
            int scoreWidth = MeasureText(scoreText, 30);
            int restartWidth = MeasureText(restartText, 25);
            
            DrawText(loseText, SCREEN_WIDTH / 2 - loseWidth / 2, 200, 60, RED);
            DrawText(scoreText, SCREEN_WIDTH / 2 - scoreWidth / 2, 280, 30, WHITE);
            DrawText(restartText, SCREEN_WIDTH / 2 - restartWidth / 2, 350, 25, GRAY);
        }
    };
    
    // Main entry point
    int main() {
        // Initialize the window
        // We use FLAG_VSYNC_HINT to prevent screen tearing and limit frame rate
        SetConfigFlags(FLAG_VSYNC_HINT);
        InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Brick Breaker");
        SetTargetFPS(60); // Target 60 FPS for smooth gameplay
        
        // Create game instance
        Game game;
        
        // Main game loop - runs until window is closed
        // This is the heart of the game: update state, render, repeat
        while (!WindowShouldClose()) {
            game.Update();
            game.Draw();
        }
        
        // Cleanup
        CloseWindow();
        
        return 0;
    }
''').strip()

CPP_TESTS_GAME = textwrap.dedent('''
    #include <gtest/gtest.h>
    #include <cmath>
    
    // Simple structures for testing
    // In a real project, these would be in your main game header
    struct Vector2 {
        float x, y;
    };
    
    struct Rectangle {
        float x, y, width, height;
    };
    
    // Helper function to check circle-rectangle collision
    // This is the core collision detection algorithm we're testing
    bool CheckCollisionCircleRec(Vector2 center, float radius, Rectangle rec) {
        // Find the closest point on the rectangle to the circle center
        float closestX = fmax(rec.x, fmin(center.x, rec.x + rec.width));
        float closestY = fmax(rec.y, fmin(center.y, rec.y + rec.height));
        
        // Calculate distance between circle center and closest point
        float distanceX = center.x - closestX;
        float distanceY = center.y - closestY;
        float distanceSquared = (distanceX * distanceX) + (distanceY * distanceY);
        
        // Collision occurs if distance is less than radius
        return distanceSquared < (radius * radius);
    }
    
    // Function to update ball position
    Vector2 UpdateBallPosition(Vector2 position, Vector2 velocity) {
        return { position.x + velocity.x, position.y + velocity.y };
    }
    
    // Function to check if ball hit left/right wall and bounce
    Vector2 BounceOffWalls(Vector2 velocity, Vector2 position, float radius, float screenWidth) {
        Vector2 newVelocity = velocity;
        
        if (position.x - radius <= 0 || position.x + radius >= screenWidth) {
            newVelocity.x *= -1;
        }
        
        return newVelocity;
    }
    
    // Calculate score based on brick row
    int CalculateBrickScore(int row, int totalRows) {
        return (totalRows - row) * 10;
    }
    
    // Test fixture for ball physics tests
    // Using a fixture allows us to set up common test data
    class BallPhysicsTest : public ::testing::Test {
    protected:
        Vector2 ballPosition;
        Vector2 ballVelocity;
        float ballRadius;
        float screenWidth;
        
        void SetUp() override {
            // Initialize common test values
            ballPosition = { 400.0f, 300.0f };
            ballVelocity = { 5.0f, -5.0f };
            ballRadius = 8.0f;
            screenWidth = 800.0f;
        }
    };
    
    // Test 1: Ball position updates correctly based on velocity
    // This ensures our basic physics calculation works
    TEST_F(BallPhysicsTest, PositionUpdatesCorrectly) {
        Vector2 newPosition = UpdateBallPosition(ballPosition, ballVelocity);
        
        // Ball should move by velocity amount
        EXPECT_FLOAT_EQ(newPosition.x, 405.0f);
        EXPECT_FLOAT_EQ(newPosition.y, 295.0f);
    }
    
    // Test 2: Ball bounces off left wall
    // Validates that collision with walls reverses horizontal velocity
    TEST_F(BallPhysicsTest, BouncesOffLeftWall) {
        ballPosition = { 5.0f, 300.0f };  // Near left wall
        ballVelocity = { -5.0f, -3.0f };  // Moving left
        
        Vector2 newVelocity = BounceOffWalls(ballVelocity, ballPosition, ballRadius, screenWidth);
        
        // X velocity should reverse, Y velocity should stay the same
        EXPECT_FLOAT_EQ(newVelocity.x, 5.0f);
        EXPECT_FLOAT_EQ(newVelocity.y, -3.0f);
    }
    
    // Test 3: Ball bounces off right wall
    TEST_F(BallPhysicsTest, BouncesOffRightWall) {
        ballPosition = { 795.0f, 300.0f };  // Near right wall
        ballVelocity = { 5.0f, -3.0f };     // Moving right
        
        Vector2 newVelocity = BounceOffWalls(ballVelocity, ballPosition, ballRadius, screenWidth);
        
        // X velocity should reverse
        EXPECT_FLOAT_EQ(newVelocity.x, -5.0f);
        EXPECT_FLOAT_EQ(newVelocity.y, -3.0f);
    }
    
    // Test fixture for collision detection tests
    class CollisionTest : public ::testing::Test {
    protected:
        Rectangle paddle;
        float ballRadius;
        
        void SetUp() override {
            paddle = { 350.0f, 550.0f, 100.0f, 20.0f };
            ballRadius = 8.0f;
        }
    };
    
    // Test 4: Collision detection - ball hits paddle center
    // This tests the core gameplay mechanic
    TEST_F(CollisionTest, BallHitsPaddleCenter) {
        Vector2 ballPos = { 400.0f, 542.0f };  // Just above paddle center
        
        bool collision = CheckCollisionCircleRec(ballPos, ballRadius, paddle);
        
        EXPECT_TRUE(collision);
    }
    
    // Test 5: Collision detection - ball misses paddle
    TEST_F(CollisionTest, BallMissesPaddle) {
        Vector2 ballPos = { 200.0f, 542.0f };  // Far left of paddle
        
        bool collision = CheckCollisionCircleRec(ballPos, ballRadius, paddle);
        
        EXPECT_FALSE(collision);
    }
    
    // Test 6: Collision detection - ball hits paddle edge
    // Edge cases are important to test for robust collision detection
    TEST_F(CollisionTest, BallHitsPaddleEdge) {
        Vector2 ballPos = { 350.0f, 555.0f };  // Left edge of paddle
        
        bool collision = CheckCollisionCircleRec(ballPos, ballRadius, paddle);
        
        EXPECT_TRUE(collision);
    }
    
    // Test 7: Score calculation based on brick row
    // This ensures our scoring system works correctly
    TEST(ScoreTest, HigherRowsWorthMorePoints) {
        int totalRows = 5;
        
        // Top row (row 0) should be worth most
        EXPECT_EQ(CalculateBrickScore(0, totalRows), 50);
        
        // Middle row
        EXPECT_EQ(CalculateBrickScore(2, totalRows), 30);
        
        // Bottom row (row 4) should be worth least
        EXPECT_EQ(CalculateBrickScore(4, totalRows), 10);
    }
    
    // Test 8: Ball below screen detection
    TEST(GameStateTest, DetectsBallBelowScreen) {
        float screenHeight = 600.0f;
        float ballRadius = 8.0f;
        
        Vector2 ballPos = { 400.0f, 610.0f };  // Below screen
        
        bool isBelowScreen = (ballPos.y - ballRadius > screenHeight);
        
        EXPECT_TRUE(isBelowScreen);
    }
    
    // Main function to run all tests
    int main(int argc, char **argv) {
        // Initialize Google Test framework
        ::testing::InitGoogleTest(&argc, argv);
        
        // Run all tests and return result
        // Returns 0 if all tests pass, non-zero otherwise
        return RUN_ALL_TESTS();
    }
''').strip()

README_CPP_TUTORIAL = textwrap.dedent('''
    # {name}
    
    A classic Brick Breaker game built with C++ and raylib. Break all the bricks with your ball and paddle!
    
    ## What You'll Learn
    
    This tutorial project will teach you:
    
    - **Game loop fundamentals**: Understanding the update-render cycle
    - **2D game physics**: Velocity, collision detection, and bouncing mechanics
    - **State management**: Menu, playing, win/lose states
    - **Event handling**: Keyboard input processing
    - **C++ best practices**: Modern C++17 style, RAII, and object-oriented design
    - **Testing**: Writing unit tests with Google Test
    - **Build systems**: Using CMake and Conan for dependency management
    
    ## Prerequisites
    
    Before you begin, make sure you have the following installed:
    
    - **C++ Compiler**: GCC 7+, Clang 5+, or MSVC 2017+
    - **CMake**: Version 3.15 or higher
    - **Conan**: Python package manager for C++ dependencies
      ```bash
      pip install conan
      ```
    - **Git**: For version control
    
    ## Quick Start
    
    ### 1. Install Dependencies
    
    ```bash
    # Create build directory
    mkdir build && cd build
    
    # Install dependencies with Conan
    conan install .. --output-folder=. --build=missing
    
    # If using Conan 2.x, use:
    conan install .. --output-folder=. --build=missing -s compiler.cppstd=17
    ```
    
    ### 2. Build the Project
    
    ```bash
    # Configure CMake
    cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release
    
    # Build
    cmake --build .
    ```
    
    ### 3. Run the Game
    
    ```bash
    # On Linux/Mac
    ./BrickBreaker
    
    # On Windows
    .\\Release\\BrickBreaker.exe
    ```
    
    ### 4. Play!
    
    - **Arrow Keys** or **A/D**: Move the paddle left and right
    - **Space**: Launch the ball
    - **ESC**: Return to menu (from win/lose screen)
    
    ## Project Structure
    
    ```
    {name}/
    ├── src/
    │   └── main.cpp          # Main game code
    ├── tests/
    │   └── test_game.cpp     # Unit tests
    ├── CMakeLists.txt        # Build configuration
    ├── conanfile.txt         # Dependency specification
    ├── .gitignore           # Git ignore rules
    └── README.md            # This file
    ```
    
    ## Running Tests
    
    The project includes unit tests using Google Test framework.
    
    ```bash
    # Build tests
    cd build
    cmake --build . --target BrickBreakerTests
    
    # Run tests
    ./BrickBreakerTests  # Linux/Mac
    .\\Release\\BrickBreakerTests.exe  # Windows
    ```
    
    The tests cover:
    - Ball physics (position updates, wall bouncing)
    - Collision detection (ball-paddle, ball-brick)
    - Score calculation
    - Game state transitions
    
    ## Understanding the Code
    
    ### Game Loop Basics
    
    The game follows the classic game loop pattern:
    
    ```cpp
    while (!WindowShouldClose()) {
        game.Update();  // Update game state
        game.Draw();    // Render everything
    }
    ```
    
    **Update Phase**: This is where all game logic happens:
    - Read player input
    - Update object positions based on velocity
    - Check for collisions
    - Update score and game state
    
    **Draw Phase**: This renders everything to the screen:
    - Clear the screen
    - Draw bricks, paddle, and ball
    - Draw UI (score, instructions)
    - Display the result
    
    ### Collision Detection Explained
    
    The game uses two types of collision detection:
    
    #### 1. Circle-Rectangle Collision (Ball-Paddle, Ball-Brick)
    
    ```cpp
    // Find the closest point on rectangle to circle center
    float closestX = Clamp(circle.x, rect.x, rect.x + rect.width);
    float closestY = Clamp(circle.y, rect.y, rect.y + rect.height);
    
    // Check if distance is less than radius
    float distance = Distance(circle, closest);
    return distance < circle.radius;
    ```
    
    This algorithm finds the point on the rectangle closest to the circle's center. If that distance is less than the ball's radius, a collision occurred.
    
    #### 2. Determining Bounce Direction
    
    When the ball hits a brick, we need to know which side it hit:
    
    ```cpp
    // Compare horizontal vs vertical overlap
    if (overlapX > overlapY) {
        velocity.x *= -1;  // Hit from side
    } else {
        velocity.y *= -1;  // Hit from top/bottom
    }
    ```
    
    This ensures the ball bounces realistically based on the angle of impact.
    
    ### Raylib Concepts
    
    **Raylib** is a simple game programming library. Key concepts used:
    
    - `InitWindow()`: Creates the game window
    - `BeginDrawing()` / `EndDrawing()`: Frame rendering boundaries
    - `DrawRectangleRec()`: Draws rectangles (paddle, bricks)
    - `DrawCircleV()`: Draws circles (ball)
    - `IsKeyDown()` / `IsKeyPressed()`: Input detection
    - `SetTargetFPS()`: Controls game speed
    
    ### Game State Management
    
    The game uses an enum to track states:
    
    ```cpp
    enum class GameState {
        MENU,     // Start screen
        PLAYING,  // Active gameplay
        WIN,      // All bricks destroyed
        LOSE      // Ball fell off screen
    };
    ```
    
    This makes code clearer than using magic numbers and allows different behavior in each state.
    
    ## How to Extend This Game
    
    Here are some ideas to make the game more interesting:
    
    ### 1. Add Multiple Lives
    
    ```cpp
    class Game {
        int lives = 3;
        
        void UpdatePlaying() {
            if (ball.IsBelowScreen()) {
                lives--;
                if (lives <= 0) {
                    state = GameState::LOSE;
                } else {
                    ball.Reset();
                }
            }
        }
    };
    ```
    
    ### 2. Progressive Difficulty
    
    Make the ball faster after clearing each level:
    
    ```cpp
    if (activeBricks == 0) {
        level++;
        ballSpeed *= 1.1f;  // 10% faster
        InitBricks();
    }
    ```
    
    ### 3. Power-ups
    
    Add special bricks that drop power-ups:
    - **Wider Paddle**: Easier to hit the ball
    - **Multi-ball**: Multiple balls in play
    - **Slow-mo**: Reduce ball speed temporarily
    
    ### 4. Sound Effects
    
    Raylib makes audio easy:
    
    ```cpp
    Sound brickHit = LoadSound("brick_hit.wav");
    
    // In collision detection
    if (ballHitBrick) {
        PlaySound(brickHit);
    }
    ```
    
    ### 5. High Score Persistence
    
    Save high scores to a file:
    
    ```cpp
    void SaveHighScore(int score) {
        std::ofstream file("highscore.txt");
        file << score;
    }
    
    int LoadHighScore() {
        std::ifstream file("highscore.txt");
        int score = 0;
        file >> score;
        return score;
    }
    ```
    
    ### 6. Particle Effects
    
    Add visual flair when bricks break:
    
    ```cpp
    struct Particle {
        Vector2 position;
        Vector2 velocity;
        Color color;
        float lifetime;
    };
    
    std::vector<Particle> particles;
    
    // When brick breaks, spawn particles
    ```
    
    ## Troubleshooting
    
    ### Conan Issues
    
    If you get "package not found" errors:
    ```bash
    conan profile detect --force
    conan install .. --output-folder=. --build=missing
    ```
    
    ### Raylib Not Found
    
    Make sure you're using the CMake toolchain file from Conan:
    ```bash
    cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
    ```
    
    ### Game Runs Too Fast/Slow
    
    Adjust the target FPS in `main.cpp`:
    ```cpp
    SetTargetFPS(60);  // Try 30 or 120
    ```
    
    ## Learning Resources
    
    - **Raylib Documentation**: https://www.raylib.com/
    - **C++ Reference**: https://en.cppreference.com/
    - **Google Test Primer**: https://google.github.io/googletest/primer.html
    - **CMake Tutorial**: https://cmake.org/cmake/help/latest/guide/tutorial/
    - **Game Programming Patterns**: https://gameprogrammingpatterns.com/
    
    ## License
    
    This project is open source and available for learning purposes.
    
    ## Next Steps
    
    Once you're comfortable with this code:
    
    1. Try implementing one of the extensions above
    2. Experiment with different game mechanics
    3. Build a completely different game using raylib
    4. Explore more advanced topics like sprite sheets, tilemaps, or physics engines
    
    Happy coding!
''').strip()

CMAKE_TUTORIAL = textwrap.dedent('''
    # CMake version requirement
    # 3.15 introduced many useful features for modern C++ projects
    cmake_minimum_required(VERSION 3.15)
    
    # Project declaration
    # This sets the project name and enables C++ language support
    project({name} LANGUAGES CXX)
    
    # C++ Standard
    # We use C++17 for modern features like structured bindings and std::optional
    set(CMAKE_CXX_STANDARD 17)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)
    set(CMAKE_CXX_EXTENSIONS OFF)  # Use -std=c++17, not -std=gnu++17
    
    # Output directories
    # This keeps build artifacts organized
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/bin)
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/lib)
    set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/lib)
    
    # ============================================================================
    # Dependencies
    # ============================================================================
    
    # Find raylib
    # Raylib is our game development framework
    # Conan will make this available via find_package
    find_package(raylib REQUIRED)
    
    # Find Google Test (optional, only needed for tests)
    # We use GTest for unit testing our game logic
    find_package(GTest REQUIRED)
    
    # ============================================================================
    # Main Game Executable
    # ============================================================================
    
    # Define source files for the main game
    # Add new .cpp files here as your project grows
    set(GAME_SOURCES
        src/main.cpp
        # Add more source files here as needed:
        # src/game.cpp
        # src/ball.cpp
        # src/paddle.cpp
    )
    
    # Create the main executable
    add_executable(BrickBreaker ${{GAME_SOURCES}})
    
    # Link raylib to the executable
    # This makes all raylib functions available to our game code
    target_link_libraries(BrickBreaker PRIVATE raylib)
    
    # Include directories (if you have headers in separate folders)
    # target_include_directories(BrickBreaker PRIVATE include)
    
    # Compiler warnings
    # Enable warnings to catch potential bugs early
    if(MSVC)
        # Microsoft Visual C++ warnings
        target_compile_options(BrickBreaker PRIVATE /W4)
    else()
        # GCC/Clang warnings
        target_compile_options(BrickBreaker PRIVATE -Wall -Wextra -Wpedantic)
    endif()
    
    # ============================================================================
    # Tests
    # ============================================================================
    
    # Enable testing support
    enable_testing()
    
    # Define test source files
    set(TEST_SOURCES
        tests/test_game.cpp
        # Add more test files here:
        # tests/test_collision.cpp
        # tests/test_physics.cpp
    )
    
    # Create test executable
    add_executable(BrickBreakerTests ${{TEST_SOURCES}})
    
    # Link Google Test and pthread (required on Linux)
    # GTest::gtest_main provides the main() function for tests
    target_link_libraries(BrickBreakerTests PRIVATE 
        GTest::gtest
        GTest::gtest_main
    )
    
    # Add tests to CTest
    # This allows running tests with "ctest" command
    include(GoogleTest)
    gtest_discover_tests(BrickBreakerTests)
    
    # ============================================================================
    # Installation (Optional)
    # ============================================================================
    
    # Install the game executable
    # This allows "cmake --install" to copy the game to a system directory
    install(TARGETS BrickBreaker
        RUNTIME DESTINATION bin
    )
    
    # ============================================================================
    # Platform-specific settings
    # ============================================================================
    
    # Windows: Copy DLLs to output directory
    if(WIN32)
        # Copy raylib DLL next to executable (if using shared libs)
        add_custom_command(TARGET BrickBreaker POST_BUILD
            COMMAND ${{CMAKE_COMMAND}} -E copy_if_different
            $<TARGET_FILE:raylib>
            $<TARGET_FILE_DIR:BrickBreaker>
        )
    endif()
    
    # macOS: Set app bundle properties (if building .app)
    if(APPLE)
        set_target_properties(BrickBreaker PROPERTIES
            MACOSX_BUNDLE TRUE
            MACOSX_BUNDLE_GUI_IDENTIFIER com.{name}.brickbreaker
            MACOSX_BUNDLE_BUNDLE_VERSION "1.0"
            MACOSX_BUNDLE_SHORT_VERSION_STRING "1.0"
        )
    endif()
    
    # ============================================================================
    # Adding New Files
    # ============================================================================
    # 
    # To add a new source file:
    # 1. Add it to GAME_SOURCES list above
    # 2. Run CMake configuration again: cmake ..
    # 3. Build: cmake --build .
    #
    # To add a new test file:
    # 1. Add it to TEST_SOURCES list above
    # 2. Reconfigure and build
    #
    # To add a new library dependency:
    # 1. Add it to conanfile.txt
    # 2. Run: conan install ..
    # 3. Add find_package(LibraryName REQUIRED) above
    # 4. Add LibraryName to target_link_libraries()
    #
    # ============================================================================
''').strip()

CONANFILE_TUTORIAL = textwrap.dedent('''
    [requires]
    # Raylib - Simple and easy-to-use game programming library
    # Provides window management, graphics, input, audio, and more
    # Version 5.0 is the latest stable release with great C++ support
    raylib/5.0
    
    # Google Test - C++ testing framework
    # Industry-standard testing library for writing unit tests
    # Version 1.14.0 is stable and widely compatible
    gtest/1.14.0
    
    [generators]
    # CMakeDeps - Generates CMake config files for find_package()
    # This allows CMake to locate the installed libraries
    CMakeDeps
    
    # CMakeToolchain - Generates CMake toolchain file
    # This configures CMake with the correct compiler settings and paths
    CMakeToolchain
    
    [options]
    # Raylib options
    # Build raylib as a shared library (DLL on Windows, .so on Linux)
    # Set to False if you want static linking
    raylib:shared=True
    
    # Google Test options
    # We don't need gmock for this simple project
    gtest:no_main=False
''').strip()

GITIGNORE_CPP_TUTORIAL = textwrap.dedent('''
    # Build directories
    build/
    cmake-build-*/
    out/
    
    # CMake generated files
    CMakeCache.txt
    CMakeFiles/
    cmake_install.cmake
    CTestTestfile.cmake
    Makefile
    *.cmake
    !CMakeLists.txt
    
    # Conan generated files
    conaninfo.txt
    conanbuildinfo.*
    conan.lock
    graph_info.json
    CMakeUserPresets.json
    
    # Compiled binaries
    *.exe
    *.out
    *.app
    *.dll
    *.so
    *.dylib
    
    # Object files
    *.o
    *.obj
    *.lo
    *.slo
    
    # Precompiled Headers
    *.gch
    *.pch
    
    # Static libraries
    *.lib
    *.a
    *.la
    
    # Executables
    BrickBreaker
    BrickBreakerTests
    
    # Testing
    Testing/
    test_detail.xml
    
    # IDE specific files
    # Visual Studio
    .vs/
    *.vcxproj
    *.vcxproj.filters
    *.vcxproj.user
    *.sln
    *.suo
    *.user
    *.userosscache
    *.sln.docstates
    
    # Visual Studio Code
    .vscode/
    *.code-workspace
    
    # CLion
    .idea/
    cmake-build-debug/
    cmake-build-release/
    
    # Xcode
    *.xcodeproj
    *.xcworkspace
    
    # QtCreator
    CMakeLists.txt.user*
    
    # Sublime Text
    *.sublime-project
    *.sublime-workspace
    
    # Vim
    *.swp
    *.swo
    *~
    
    # Emacs
    *~
    \\#*\\#
    .\\#*
    
    # macOS
    .DS_Store
    .AppleDouble
    .LSOverride
    
    # Windows
    Thumbs.db
    ehthumbs.db
    Desktop.ini
    
    # Linux
    *~
    .directory
    
    # Dependency directories
    dependencies/
    third_party/
    
    # Package files
    *.tar.gz
    *.zip
    
    # Log files
    *.log
    
    # Debug files
    *.dSYM/
    *.pdb
    *.ilk
    
    # Profiling
    *.prof
    perf.data*
    
    # Core dumps
    core
    core.*
    
    # Temporary files
    *.tmp
    *.temp
    *.bak
    *.old
    
    # High scores and game data (optional - remove if you want to track these)
    highscore.txt
    gamedata.dat
''').strip()
