"""
JavaScript Flappy Bird Tutorial Templates

This module provides comprehensive templates for creating a JavaScript Flappy Bird game.
Includes vanilla HTML5 Canvas game, Jest tests, and tutorial documentation.
"""

import textwrap


JAVASCRIPT_MAIN_GAME = textwrap.dedent("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flappy Bird - JavaScript Canvas Game</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background: linear-gradient(#4ec0ca, #87ceeb);
                font-family: 'Arial', sans-serif;
            }}
            
            #gameCanvas {{
                border: 3px solid #2c3e50;
                background: #70c5ce;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }}
            
            .info {{
                position: absolute;
                top: 20px;
                left: 20px;
                color: white;
                font-size: 14px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }}
        </style>
    </head>
    <body>
        <div class="info">Press SPACE or CLICK to flap!</div>
        <canvas id="gameCanvas" width="400" height="600"></canvas>
        
        <script>
            // =================================================================
            // FLAPPY BIRD - HTML5 Canvas Game
            // A complete implementation with physics, collision, and game states
            // =================================================================
            
            // Get canvas context for drawing
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            
            // =================================================================
            // GAME CONSTANTS - Configuration values for game mechanics
            // =================================================================
            const GRAVITY = 0.5;           // Downward acceleration per frame
            const JUMP_STRENGTH = -8;      // Upward velocity when jumping
            const PIPE_SPEED = 2;          // Horizontal pipe movement speed
            const PIPE_GAP = 150;          // Vertical gap between pipe pairs
            const PIPE_WIDTH = 60;         // Width of each pipe
            const PIPE_SPAWN_INTERVAL = 90; // Frames between new pipe spawns
            const BIRD_SIZE = 30;          // Bird hitbox size
            const GROUND_HEIGHT = 100;     // Height of ground from bottom
            
            // =================================================================
            // GAME STATE - Enumeration for different game phases
            // =================================================================
            const GameState = {{
                MENU: 'menu',
                PLAYING: 'playing',
                GAME_OVER: 'gameOver'
            }};
            
            // =================================================================
            // BIRD OBJECT - Player character with physics
            // =================================================================
            const bird = {{
                x: 80,                     // Fixed horizontal position
                y: canvas.height / 2,      // Vertical position (changes)
                velocity: 0,               // Current vertical velocity
                
                // Apply gravity to bird's velocity and position
                update() {{
                    this.velocity += GRAVITY;
                    this.y += this.velocity;
                    
                    // Clamp bird position to canvas bounds
                    if (this.y < 0) {{
                        this.y = 0;
                        this.velocity = 0;
                    }}
                    
                    // Check if bird hit the ground
                    if (this.y > canvas.height - GROUND_HEIGHT - BIRD_SIZE) {{
                        this.y = canvas.height - GROUND_HEIGHT - BIRD_SIZE;
                        this.velocity = 0;
                        if (gameState === GameState.PLAYING) {{
                            gameOver();
                        }}
                    }}
                }},
                
                // Make bird jump by setting negative velocity
                jump() {{
                    this.velocity = JUMP_STRENGTH;
                }},
                
                // Draw bird as a yellow circle with eye and beak
                draw() {{
                    // Bird body
                    ctx.fillStyle = '#FFD700';
                    ctx.beginPath();
                    ctx.arc(this.x, this.y, BIRD_SIZE / 2, 0, Math.PI * 2);
                    ctx.fill();
                    
                    // Bird eye
                    ctx.fillStyle = 'white';
                    ctx.beginPath();
                    ctx.arc(this.x + 8, this.y - 5, 6, 0, Math.PI * 2);
                    ctx.fill();
                    
                    ctx.fillStyle = 'black';
                    ctx.beginPath();
                    ctx.arc(this.x + 10, this.y - 5, 3, 0, Math.PI * 2);
                    ctx.fill();
                    
                    // Bird beak
                    ctx.fillStyle = '#FF6347';
                    ctx.beginPath();
                    ctx.moveTo(this.x + BIRD_SIZE / 2, this.y);
                    ctx.lineTo(this.x + BIRD_SIZE / 2 + 10, this.y - 3);
                    ctx.lineTo(this.x + BIRD_SIZE / 2 + 10, this.y + 3);
                    ctx.closePath();
                    ctx.fill();
                }},
                
                // Reset bird to initial state
                reset() {{
                    this.y = canvas.height / 2;
                    this.velocity = 0;
                }}
            }};
            
            // =================================================================
            // PIPES SYSTEM - Obstacle management and collision detection
            // =================================================================
            let pipes = [];
            let frameCount = 0;
            let score = 0;
            
            // Pipe factory function - creates a new pipe pair
            function createPipe() {{
                // Random height for top pipe (leaving gap for bottom pipe)
                const minHeight = 50;
                const maxHeight = canvas.height - GROUND_HEIGHT - PIPE_GAP - 50;
                const topHeight = Math.random() * (maxHeight - minHeight) + minHeight;
                
                return {{
                    x: canvas.width,
                    topHeight: topHeight,
                    bottomY: topHeight + PIPE_GAP,
                    scored: false,  // Track if player passed this pipe
                    
                    // Move pipe left and check if off-screen
                    update() {{
                        this.x -= PIPE_SPEED;
                    }},
                    
                    // Draw top and bottom pipes with 3D effect
                    draw() {{
                        // Top pipe
                        ctx.fillStyle = '#2ecc71';
                        ctx.fillRect(this.x, 0, PIPE_WIDTH, this.topHeight);
                        
                        // Top pipe cap
                        ctx.fillStyle = '#27ae60';
                        ctx.fillRect(this.x - 5, this.topHeight - 30, PIPE_WIDTH + 10, 30);
                        
                        // Bottom pipe
                        ctx.fillStyle = '#2ecc71';
                        ctx.fillRect(this.x, this.bottomY, PIPE_WIDTH, 
                                   canvas.height - GROUND_HEIGHT - this.bottomY);
                        
                        // Bottom pipe cap
                        ctx.fillStyle = '#27ae60';
                        ctx.fillRect(this.x - 5, this.bottomY, PIPE_WIDTH + 10, 30);
                        
                        // Add pipe highlights for 3D effect
                        ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
                        ctx.fillRect(this.x + 5, 0, 10, this.topHeight);
                        ctx.fillRect(this.x + 5, this.bottomY, 10, 
                                   canvas.height - GROUND_HEIGHT - this.bottomY);
                    }},
                    
                    // Check if bird collides with this pipe
                    // Uses Axis-Aligned Bounding Box (AABB) collision detection
                    collidesWith(bird) {{
                        // Check if bird is horizontally aligned with pipe
                        if (bird.x + BIRD_SIZE / 2 > this.x && 
                            bird.x - BIRD_SIZE / 2 < this.x + PIPE_WIDTH) {{
                            
                            // Check if bird hits top or bottom pipe
                            if (bird.y - BIRD_SIZE / 2 < this.topHeight || 
                                bird.y + BIRD_SIZE / 2 > this.bottomY) {{
                                return true;
                            }}
                        }}
                        return false;
                    }},
                    
                    // Check if bird passed this pipe (for scoring)
                    isPassed(bird) {{
                        return !this.scored && bird.x > this.x + PIPE_WIDTH;
                    }}
                }};
            }}
            
            // Update all pipes and handle scoring
            function updatePipes() {{
                // Spawn new pipes at regular intervals
                if (frameCount % PIPE_SPAWN_INTERVAL === 0) {{
                    pipes.push(createPipe());
                }}
                
                // Update each pipe and check collisions
                for (let i = pipes.length - 1; i >= 0; i--) {{
                    pipes[i].update();
                    
                    // Remove pipes that are off-screen (optimization)
                    if (pipes[i].x + PIPE_WIDTH < 0) {{
                        pipes.splice(i, 1);
                        continue;
                    }}
                    
                    // Check collision with bird
                    if (pipes[i].collidesWith(bird)) {{
                        gameOver();
                    }}
                    
                    // Check if bird passed pipe (increment score)
                    if (pipes[i].isPassed(bird)) {{
                        pipes[i].scored = true;
                        score++;
                    }}
                }}
            }}
            
            // Draw all pipes on canvas
            function drawPipes() {{
                pipes.forEach(pipe => pipe.draw());
            }}
            
            // =================================================================
            // BACKGROUND & ENVIRONMENT - Clouds, ground, and decorations
            // =================================================================
            
            // Animated clouds for background atmosphere
            let clouds = [
                {{ x: 100, y: 100, speed: 0.3 }},
                {{ x: 250, y: 150, speed: 0.2 }},
                {{ x: 350, y: 80, speed: 0.25 }}
            ];
            
            function drawBackground() {{
                // Sky gradient (already set in CSS)
                
                // Draw and animate clouds
                ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
                clouds.forEach(cloud => {{
                    // Draw cloud as three overlapping circles
                    ctx.beginPath();
                    ctx.arc(cloud.x, cloud.y, 20, 0, Math.PI * 2);
                    ctx.arc(cloud.x + 25, cloud.y, 30, 0, Math.PI * 2);
                    ctx.arc(cloud.x + 50, cloud.y, 20, 0, Math.PI * 2);
                    ctx.fill();
                    
                    // Move cloud left and wrap around
                    cloud.x -= cloud.speed;
                    if (cloud.x < -60) {{
                        cloud.x = canvas.width + 60;
                    }}
                }});
            }}
            
            // Draw ground at bottom of screen
            function drawGround() {{
                // Ground
                ctx.fillStyle = '#DEB887';
                ctx.fillRect(0, canvas.height - GROUND_HEIGHT, canvas.width, GROUND_HEIGHT);
                
                // Grass on top of ground
                ctx.fillStyle = '#8FBC8F';
                ctx.fillRect(0, canvas.height - GROUND_HEIGHT, canvas.width, 20);
                
                // Ground pattern (vertical lines)
                ctx.strokeStyle = '#D2691E';
                ctx.lineWidth = 2;
                for (let x = 0; x < canvas.width; x += 30) {{
                    ctx.beginPath();
                    ctx.moveTo(x, canvas.height - GROUND_HEIGHT + 20);
                    ctx.lineTo(x, canvas.height);
                    ctx.stroke();
                }}
            }}
            
            // =================================================================
            // UI RENDERING - Score, menus, and text displays
            // =================================================================
            
            function drawScore() {{
                ctx.fillStyle = 'white';
                ctx.strokeStyle = 'black';
                ctx.lineWidth = 3;
                ctx.font = 'bold 40px Arial';
                ctx.textAlign = 'center';
                
                // Draw score with outline for visibility
                ctx.strokeText(score, canvas.width / 2, 60);
                ctx.fillText(score, canvas.width / 2, 60);
            }}
            
            function drawMenu() {{
                // Semi-transparent overlay
                ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                // Title
                ctx.fillStyle = 'white';
                ctx.strokeStyle = 'black';
                ctx.lineWidth = 4;
                ctx.font = 'bold 50px Arial';
                ctx.textAlign = 'center';
                ctx.strokeText('FLAPPY BIRD', canvas.width / 2, 200);
                ctx.fillText('FLAPPY BIRD', canvas.width / 2, 200);
                
                // Instructions
                ctx.font = 'bold 24px Arial';
                ctx.lineWidth = 3;
                ctx.strokeText('Click or Press SPACE to Start', canvas.width / 2, 300);
                ctx.fillText('Click or Press SPACE to Start', canvas.width / 2, 300);
                
                // Controls info
                ctx.font = '18px Arial';
                ctx.lineWidth = 2;
                ctx.strokeText('Avoid the pipes!', canvas.width / 2, 350);
                ctx.fillText('Avoid the pipes!', canvas.width / 2, 350);
            }}
            
            function drawGameOver() {{
                // Semi-transparent overlay
                ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                // Game Over text
                ctx.fillStyle = '#FF6347';
                ctx.strokeStyle = 'black';
                ctx.lineWidth = 4;
                ctx.font = 'bold 60px Arial';
                ctx.textAlign = 'center';
                ctx.strokeText('GAME OVER', canvas.width / 2, 200);
                ctx.fillText('GAME OVER', canvas.width / 2, 200);
                
                // Final score
                ctx.fillStyle = 'white';
                ctx.font = 'bold 30px Arial';
                ctx.lineWidth = 3;
                ctx.strokeText(`Score: ${{score}}`, canvas.width / 2, 270);
                ctx.fillText(`Score: ${{score}}`, canvas.width / 2, 270);
                
                // Restart instruction
                ctx.font = 'bold 24px Arial';
                ctx.strokeText('Click or Press SPACE to Restart', canvas.width / 2, 350);
                ctx.fillText('Click or Press SPACE to Restart', canvas.width / 2, 350);
            }}
            
            // =================================================================
            // GAME STATE MANAGEMENT - Control game flow
            // =================================================================
            
            let gameState = GameState.MENU;
            
            function startGame() {{
                gameState = GameState.PLAYING;
                bird.reset();
                pipes = [];
                score = 0;
                frameCount = 0;
            }}
            
            function gameOver() {{
                gameState = GameState.GAME_OVER;
            }}
            
            // =================================================================
            // INPUT HANDLING - Keyboard and mouse events
            // =================================================================
            
            function handleInput() {{
                if (gameState === GameState.MENU) {{
                    startGame();
                    bird.jump();
                }} else if (gameState === GameState.PLAYING) {{
                    bird.jump();
                }} else if (gameState === GameState.GAME_OVER) {{
                    startGame();
                }}
            }}
            
            // Keyboard input (spacebar)
            document.addEventListener('keydown', (e) => {{
                if (e.code === 'Space') {{
                    e.preventDefault();  // Prevent page scroll
                    handleInput();
                }}
            }});
            
            // Mouse/touch input
            canvas.addEventListener('click', handleInput);
            
            // =================================================================
            // GAME LOOP - Main rendering and update cycle
            // Uses requestAnimationFrame for smooth 60fps animation
            // =================================================================
            
            function gameLoop() {{
                // Clear canvas for new frame
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                // Draw background elements
                drawBackground();
                
                // Update and render based on game state
                if (gameState === GameState.PLAYING) {{
                    frameCount++;
                    
                    // Update game objects
                    bird.update();
                    updatePipes();
                    
                    // Draw game objects
                    drawPipes();
                    bird.draw();
                    drawScore();
                }} else if (gameState === GameState.MENU) {{
                    // Draw static bird in menu
                    bird.draw();
                    drawMenu();
                }} else if (gameState === GameState.GAME_OVER) {{
                    // Draw final game state
                    drawPipes();
                    bird.draw();
                    drawGameOver();
                }}
                
                // Always draw ground on top
                drawGround();
                
                // Request next frame (creates ~60fps loop)
                requestAnimationFrame(gameLoop);
            }}
            
            // =================================================================
            // START THE GAME - Initialize and begin game loop
            // =================================================================
            
            // Begin the game loop
            gameLoop();
        </script>
    </body>
    </html>
""").strip()


JAVASCRIPT_TESTS_GAME = textwrap.dedent("""
    // =================================================================
    // FLAPPY BIRD GAME TESTS - Jest Unit Tests
    // Testing game logic, physics, and collision detection
    // =================================================================
    
    // Mock the DOM environment for testing
    document.body.innerHTML = '<canvas id="gameCanvas" width="400" height="600"></canvas>';
    
    // Import game logic (in real setup, you'd extract logic to separate module)
    // For this tutorial, we'll test the core game mechanics
    
    describe('Bird Physics', () => {{
        let bird;
        
        beforeEach(() => {{
            // Initialize bird object before each test
            bird = {{
                x: 80,
                y: 300,
                velocity: 0,
                gravity: 0.5,
                jumpStrength: -8,
                size: 30,
                
                update() {{
                    this.velocity += this.gravity;
                    this.y += this.velocity;
                }},
                
                jump() {{
                    this.velocity = this.jumpStrength;
                }}
            }};
        }});
        
        test('bird should fall due to gravity', () => {{
            // Test that gravity accelerates bird downward
            const initialY = bird.y;
            const initialVelocity = bird.velocity;
            
            bird.update();
            
            // Velocity should increase (become more positive/downward)
            expect(bird.velocity).toBe(initialVelocity + bird.gravity);
            
            // Position should move down
            expect(bird.y).toBeGreaterThan(initialY);
        }});
        
        test('bird should jump when jump method is called', () => {{
            // Test that jump applies negative (upward) velocity
            bird.jump();
            
            // Velocity should be negative (upward)
            expect(bird.velocity).toBe(bird.jumpStrength);
            expect(bird.velocity).toBeLessThan(0);
        }});
        
        test('bird should accelerate when falling', () => {{
            // Test that velocity increases over multiple frames
            bird.update();
            const velocityAfterOneFrame = bird.velocity;
            
            bird.update();
            const velocityAfterTwoFrames = bird.velocity;
            
            // Velocity should keep increasing (gravity accumulates)
            expect(velocityAfterTwoFrames).toBeGreaterThan(velocityAfterOneFrame);
        }});
    }});
    
    describe('Pipe Collision Detection', () => {{
        let bird;
        let pipe;
        
        beforeEach(() => {{
            bird = {{
                x: 80,
                y: 300,
                size: 30
            }};
            
            pipe = {{
                x: 200,
                width: 60,
                topHeight: 200,
                bottomY: 350,
                gap: 150,
                
                // AABB collision detection
                collidesWith(bird) {{
                    // Check horizontal overlap
                    if (bird.x + bird.size / 2 > this.x && 
                        bird.x - bird.size / 2 < this.x + this.width) {{
                        
                        // Check vertical collision with top or bottom pipe
                        if (bird.y - bird.size / 2 < this.topHeight || 
                            bird.y + bird.size / 2 > this.bottomY) {{
                            return true;
                        }}
                    }}
                    return false;
                }}
            }};
        }});
        
        test('should detect collision with top pipe', () => {{
            // Position bird to hit top pipe
            bird.x = 220;  // Horizontally aligned with pipe
            bird.y = 180;  // Above the gap (hits top pipe)
            
            expect(pipe.collidesWith(bird)).toBe(true);
        }});
        
        test('should detect collision with bottom pipe', () => {{
            // Position bird to hit bottom pipe
            bird.x = 220;  // Horizontally aligned with pipe
            bird.y = 370;  // Below the gap (hits bottom pipe)
            
            expect(pipe.collidesWith(bird)).toBe(true);
        }});
        
        test('should NOT detect collision when bird passes through gap', () => {{
            // Position bird safely in the gap
            bird.x = 220;  // Horizontally aligned with pipe
            bird.y = 275;  // Centered in gap
            
            expect(pipe.collidesWith(bird)).toBe(false);
        }});
        
        test('should NOT detect collision when bird is before pipe', () => {{
            // Bird hasn't reached pipe yet
            bird.x = 80;
            bird.y = 275;
            
            expect(pipe.collidesWith(bird)).toBe(false);
        }});
    }});
    
    describe('Score System', () => {{
        let score;
        let bird;
        let pipe;
        
        beforeEach(() => {{
            score = 0;
            bird = {{ x: 80 }};
            pipe = {{
                x: 200,
                width: 60,
                scored: false,
                
                isPassed(bird) {{
                    return !this.scored && bird.x > this.x + this.width;
                }}
            }};
        }});
        
        test('should increment score when bird passes pipe', () => {{
            // Bird passes pipe
            bird.x = 270;
            
            if (pipe.isPassed(bird)) {{
                pipe.scored = true;
                score++;
            }}
            
            expect(score).toBe(1);
            expect(pipe.scored).toBe(true);
        }});
        
        test('should NOT increment score twice for same pipe', () => {{
            // Bird passes pipe first time
            bird.x = 270;
            
            if (pipe.isPassed(bird)) {{
                pipe.scored = true;
                score++;
            }}
            
            // Bird continues past pipe (should not score again)
            bird.x = 300;
            
            if (pipe.isPassed(bird)) {{
                pipe.scored = true;
                score++;
            }}
            
            // Score should only increment once
            expect(score).toBe(1);
        }});
    }});
    
    describe('Game State Transitions', () => {{
        test('should transition from MENU to PLAYING when game starts', () => {{
            const GameState = {{
                MENU: 'menu',
                PLAYING: 'playing',
                GAME_OVER: 'gameOver'
            }};
            
            let currentState = GameState.MENU;
            
            // Simulate starting game
            function startGame() {{
                currentState = GameState.PLAYING;
            }}
            
            startGame();
            
            expect(currentState).toBe(GameState.PLAYING);
        }});
        
        test('should transition to GAME_OVER on collision', () => {{
            const GameState = {{
                MENU: 'menu',
                PLAYING: 'playing',
                GAME_OVER: 'gameOver'
            }};
            
            let currentState = GameState.PLAYING;
            
            // Simulate game over
            function gameOver() {{
                currentState = GameState.GAME_OVER;
            }}
            
            gameOver();
            
            expect(currentState).toBe(GameState.GAME_OVER);
        }});
    }});
""").strip()


README_JAVASCRIPT_TUTORIAL = textwrap.dedent("""
    # {name} - Flappy Bird Game Tutorial
    
    Welcome to your JavaScript game development journey! This project teaches you how to build a complete Flappy Bird clone using vanilla JavaScript and HTML5 Canvas.
    
    ## What You'll Learn
    
    Through this tutorial, you'll master:
    
    - **HTML5 Canvas API**: Drawing graphics, shapes, and animations in the browser
    - **Game Loop Architecture**: Using `requestAnimationFrame` for smooth 60fps gameplay
    - **Physics Simulation**: Implementing gravity, velocity, and jump mechanics
    - **Collision Detection**: AABB (Axis-Aligned Bounding Box) collision algorithm
    - **Game State Management**: Handling menu, playing, and game over states
    - **Event Handling**: Responding to keyboard and mouse input
    - **Object-Oriented JavaScript**: Organizing game entities with modern ES6+ syntax
    - **Testing Games**: Writing unit tests for game logic with Jest
    
    ## Zero Setup Required!
    
    One of the best things about web development: **no build step needed!** This is pure vanilla JavaScript that runs directly in your browser. No webpack, no babel, no complicated tooling. Just open the HTML file and play!
    
    ## Prerequisites
    
    All you need is:
    
    - A modern web browser (Chrome, Firefox, Safari, or Edge)
    - A text editor (VS Code, Sublime Text, or even Notepad)
    - Node.js and npm (only for running tests)
    - Basic JavaScript knowledge (variables, functions, objects)
    
    ## Quick Start
    
    ### Option 1: Simple File Open (Easiest!)
    
    1. Simply open `index.html` in your web browser
    2. Double-click the file, or right-click and choose "Open with" your browser
    3. Start playing immediately!
    
    ### Option 2: Local Development Server (Recommended)
    
    For a better development experience with live reloading:
    
    ```bash
    # Install a simple HTTP server (one-time setup)
    npm install -g live-server
    
    # Run the server in your project directory
    live-server
    ```
    
    This will open your game at `http://localhost:8080` and automatically reload when you make changes.
    
    ### Option 3: Python Simple Server
    
    If you have Python installed:
    
    ```bash
    # Python 3
    python -m http.server 8000
    
    # Then open http://localhost:8000 in your browser
    ```
    
    ## Project Structure
    
    ```
    {name}/
    ├── index.html          # Complete game in one file!
    ├── game.test.js        # Jest unit tests for game logic
    ├── package.json        # NPM configuration for testing
    └── README.md           # This file
    ```
    
    This project uses a single-file approach for simplicity. Everything (HTML, CSS, and JavaScript) is in `index.html`. As you learn, you might want to split it into separate files.
    
    ## Running Tests
    
    The project includes comprehensive Jest tests to verify game logic:
    
    ```bash
    # Install dependencies (first time only)
    npm install
    
    # Run all tests
    npm test
    
    # Run tests in watch mode (re-runs on file changes)
    npm test -- --watch
    ```
    
    The tests cover:
    - Bird physics (gravity and jumping)
    - Collision detection algorithms
    - Score tracking and incrementing
    - Game state transitions
    
    ## Understanding the Code
    
    ### The HTML5 Canvas
    
    Canvas is like a blank drawing surface where we can render graphics using JavaScript:
    
    ```javascript
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    
    // Draw a circle (the bird)
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();
    ```
    
    ### The Game Loop with requestAnimationFrame
    
    Games need to update and redraw 60 times per second. We use `requestAnimationFrame` for this:
    
    ```javascript
    function gameLoop() {{
        // 1. Clear the canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // 2. Update game state (physics, collisions)
        bird.update();
        updatePipes();
        
        // 3. Draw everything
        bird.draw();
        drawPipes();
        
        // 4. Request next frame (creates the loop)
        requestAnimationFrame(gameLoop);
    }}
    ```
    
    ### Physics Simulation
    
    The bird physics use basic acceleration and velocity:
    
    ```javascript
    // Each frame:
    velocity += GRAVITY;  // Gravity accelerates bird downward
    y += velocity;        // Velocity changes position
    
    // When jumping:
    velocity = JUMP_STRENGTH;  // Set negative velocity (upward)
    ```
    
    ### Collision Detection (AABB)
    
    We use Axis-Aligned Bounding Box collision - checking if rectangles overlap:
    
    ```javascript
    // Check if bird's box overlaps with pipe's box
    if (birdX + birdWidth > pipeX && birdX < pipeX + pipeWidth) {{
        if (birdY < topPipeHeight || birdY > bottomPipeY) {{
            // Collision detected!
        }}
    }}
    ```
    
    ### Event Handling
    
    Responding to player input:
    
    ```javascript
    // Keyboard input
    document.addEventListener('keydown', (e) => {{
        if (e.code === 'Space') {{
            bird.jump();
        }}
    }});
    
    // Mouse/touch input
    canvas.addEventListener('click', () => {{
        bird.jump();
    }});
    ```
    
    ## How to Extend This Game
    
    Ready to make it your own? Try these ideas:
    
    ### 1. Add Difficulty Levels
    - Increase `PIPE_SPEED` over time
    - Decrease `PIPE_GAP` as score increases
    - Add a difficulty selection menu
    
    ### 2. Power-Ups
    - Shield that allows one collision
    - Slow-motion temporary effect
    - Coin collection for bonus points
    
    ### 3. Visual Enhancements
    - Add sprite images instead of drawn shapes
    - Particle effects when jumping or crashing
    - Background parallax scrolling
    - Day/night cycle
    
    ### 4. Sound Effects
    - Jump sound (using Web Audio API)
    - Scoring sound
    - Background music
    - Collision sound
    
    ```javascript
    const jumpSound = new Audio('jump.mp3');
    jumpSound.play();
    ```
    
    ### 5. High Score System
    - Save high score to localStorage
    - Display leaderboard
    - Share score on social media
    
    ```javascript
    localStorage.setItem('highScore', score);
    const highScore = localStorage.getItem('highScore') || 0;
    ```
    
    ### 6. Mobile Optimization
    - Make canvas responsive
    - Add touch controls
    - Improve performance for mobile devices
    
    ### 7. New Obstacles
    - Moving pipes (up and down)
    - Different pipe patterns
    - Obstacles that move toward the bird
    
    ## Learning Resources
    
    Want to learn more?
    
    - [MDN Canvas Tutorial](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial)
    - [JavaScript.info - Browser Events](https://javascript.info/events)
    - [Game Programming Patterns](https://gameprogrammingpatterns.com/)
    - [HTML5 Game Development by Example](https://www.apress.com/gp/book/9781430247661)
    
    ## Troubleshooting
    
    **Game runs too fast or slow?**
    - The game uses `requestAnimationFrame` which syncs to monitor refresh rate
    - Consider implementing delta time for frame-independent movement
    
    **Canvas looks blurry?**
    - Make sure canvas width/height attributes match CSS dimensions
    - Use `ctx.imageSmoothingEnabled = false` for pixel art
    
    **Tests failing?**
    - Make sure you've run `npm install` first
    - Check that Jest is properly configured in package.json
    
    ## Next Steps
    
    1. Play the game and understand the mechanics
    2. Read through the code comments to understand each section
    3. Modify constants (gravity, speed, gap) and see what happens
    4. Run the tests to see how game logic is verified
    5. Pick one extension idea and implement it
    6. Share your creation with friends!
    
    ## Contributing
    
    Found a bug? Have an improvement? Feel free to:
    - Experiment with the code
    - Add new features
    - Improve the documentation
    - Share what you've learned
    
    Happy coding! May your bird fly high! 🐦
""").strip()


PACKAGE_JSON_TUTORIAL = textwrap.dedent("""
    {{
      "name": "{name}",
      "version": "1.0.0",
      "description": "A Flappy Bird game built with vanilla JavaScript and HTML5 Canvas - learn game development from scratch!",
      "main": "index.html",
      "scripts": {{
        "start": "live-server --port=8080 --open=index.html",
        "test": "jest",
        "test:watch": "jest --watch",
        "test:coverage": "jest --coverage"
      }},
      "keywords": [
        "game",
        "flappy-bird",
        "html5-canvas",
        "javascript",
        "tutorial"
      ],
      "author": "",
      "license": "MIT",
      "devDependencies": {{
        "jest": "^29.7.0",
        "jest-environment-jsdom": "^29.7.0"
      }},
      "jest": {{
        "testEnvironment": "jsdom",
        "collectCoverageFrom": [
          "**/*.js",
          "!**/node_modules/**",
          "!**/coverage/**"
        ]
      }}
    }}
""").strip()


GITIGNORE_JAVASCRIPT_TUTORIAL = textwrap.dedent("""
    # Dependencies
    node_modules/
    package-lock.json
    yarn.lock
    pnpm-lock.yaml
    
    # Testing
    coverage/
    .nyc_output/
    
    # Build outputs
    dist/
    build/
    .cache/
    
    # Environment variables
    .env
    .env.local
    .env.development
    .env.test
    .env.production
    
    # IDE and Editor files
    .vscode/
    .idea/
    *.swp
    *.swo
    *~
    .DS_Store
    
    # Logs
    logs/
    *.log
    npm-debug.log*
    yarn-debug.log*
    yarn-error.log*
    
    # Runtime data
    pids/
    *.pid
    *.seed
    *.pid.lock
    
    # Temporary files
    tmp/
    temp/
    
    # OS files
    Thumbs.db
    .DS_Store
    
    # Optional npm cache directory
    .npm
    
    # Optional eslint cache
    .eslintcache
    
    # Optional REPL history
    .node_repl_history
    
    # Output of 'npm pack'
    *.tgz
    
    # Parcel cache
    .parcel-cache/
""").strip()
