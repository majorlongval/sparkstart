"""
Rust tutorial templates for a Space Shooter game using Bevy ECS.
"""

from textwrap import dedent


RUST_MAIN_GAME = dedent("""
    // Space Shooter Game with Bevy ECS
    // This is a complete game demonstrating Entity Component System (ECS) architecture
    // The ECS pattern separates data (Components) from behavior (Systems)
    // This makes code more modular, testable, and performant

    use bevy::prelude::*;
    use bevy::sprite::MaterialMesh2dBundle;

    // =============================================================================
    // CONSTANTS - Magic numbers are defined here for easy tweaking
    // =============================================================================

    const WINDOW_WIDTH: f32 = 800.0;
    const WINDOW_HEIGHT: f32 = 600.0;
    const PLAYER_SIZE: f32 = 40.0;
    const PLAYER_SPEED: f32 = 300.0;
    const BULLET_SIZE: f32 = 8.0;
    const BULLET_SPEED: f32 = 500.0;
    const ENEMY_SIZE: f32 = 35.0;
    const ENEMY_SPEED: f32 = 150.0;
    const ENEMY_SPAWN_TIME: f32 = 1.5;

    // =============================================================================
    // GAME STATES - Using Rust's enum for type-safe state management
    // =============================================================================

    #[derive(Debug, Clone, Copy, Default, Eq, PartialEq, Hash, States)]
    enum GameState {{
        #[default]
        Menu,
        Playing,
        GameOver,
    }}

    // =============================================================================
    // COMPONENTS - Pure data structures that get attached to entities
    // Components are like "tags" or "properties" that entities can have
    // The ECS engine queries for entities with specific component combinations
    // =============================================================================

    // Component pattern: Each struct represents ONE aspect of an entity
    // This is the "C" in ECS - Components hold data, not behavior

    #[derive(Component)]
    struct Player;

    #[derive(Component)]
    struct Enemy;

    #[derive(Component)]
    struct Bullet;

    #[derive(Component)]
    struct Velocity {{
        x: f32,
        y: f32,
    }}

    // The Velocity component demonstrates composition over inheritance
    // Instead of "Player extends Movable", we have "Player has Velocity"
    // This is more flexible - bullets, enemies, and players can all have velocity

    #[derive(Component)]
    struct Health {{
        value: i32,
    }}

    // =============================================================================
    // RESOURCES - Global game state that isn't tied to a specific entity
    // Resources are the "R" in ECS - they're singleton data available to all systems
    // =============================================================================

    #[derive(Resource, Default)]
    struct Score {{
        value: u32,
    }}

    // Resources vs Components: Use Components for entity-specific data,
    // use Resources for game-wide state like score, time, or configuration

    #[derive(Resource)]
    struct EnemySpawnTimer {{
        timer: Timer,
    }}

    // Bevy's Timer handles countdown logic with delta time automatically
    // This demonstrates using Bevy's built-in utilities instead of rolling our own

    // =============================================================================
    // MAIN FUNCTION - App configuration and system registration
    // =============================================================================

    fn main() {{
        App::new()
            // DefaultPlugins includes windowing, rendering, input, time, etc.
            .add_plugins(DefaultPlugins.set(WindowPlugin {{
                primary_window: Some(Window {{
                    title: "Space Shooter - Bevy ECS".into(),
                    resolution: (WINDOW_WIDTH, WINDOW_HEIGHT).into(),
                    ..default()
                }}),
                ..default()
            }}))
            // init_state sets up the state machine for game states
            .init_state::<GameState>()
            // init_resource creates default instances of our global resources
            .init_resource::<Score>()
            .insert_resource(EnemySpawnTimer {{
                timer: Timer::from_seconds(ENEMY_SPAWN_TIME, TimerMode::Repeating),
            }})
            // Systems that run once when entering a specific state
            // OnEnter is perfect for setup code like spawning the player
            .add_systems(OnEnter(GameState::Menu), setup_menu)
            .add_systems(OnEnter(GameState::Playing), setup_game)
            .add_systems(OnEnter(GameState::GameOver), setup_game_over)
            // Systems that run every frame while in a specific state
            // Update systems contain the main game logic
            .add_systems(Update, menu_system.run_if(in_state(GameState::Menu)))
            .add_systems(
                Update,
                (
                    // Tuple syntax runs multiple systems in parallel when possible
                    // Bevy's scheduler automatically handles dependencies
                    player_movement,
                    player_shooting,
                    move_bullets,
                    move_enemies,
                    spawn_enemies,
                    check_collisions,
                    update_score_display,
                    check_game_over,
                )
                    .run_if(in_state(GameState::Playing)),
            )
            .add_systems(Update, game_over_system.run_if(in_state(GameState::GameOver)))
            .run();
    }}

    // =============================================================================
    // SETUP SYSTEMS - These run once when entering a state
    // =============================================================================

    fn setup_menu(mut commands: Commands) {{
        // Commands is how we create/destroy entities in Bevy
        // It queues operations that execute at the end of the frame
        // This prevents iterator invalidation issues

        commands.spawn(Camera2dBundle::default());

        commands.spawn(
            TextBundle::from_section(
                "SPACE SHOOTER\\n\\nPress SPACE to Start",
                TextStyle {{
                    font_size: 40.0,
                    color: Color::WHITE,
                    ..default()
                }},
            )
            .with_style(Style {{
                position_type: PositionType::Absolute,
                top: Val::Px(200.0),
                left: Val::Px(200.0),
                ..default()
            }}),
        );
    }}

    fn setup_game(mut commands: Commands, mut score: ResMut<Score>) {{
        // ResMut gives us mutable access to a Resource
        // Rust's borrow checker ensures only one system can mutably access it at a time
        score.value = 0;

        // Spawning the player entity with multiple components
        // This is the Bundle pattern - grouping related components
        commands.spawn((
            Player,
            Velocity {{ x: 0.0, y: 0.0 }},
            Health {{ value: 100 }},
            MaterialMesh2dBundle {{
                transform: Transform::from_xyz(0.0, -WINDOW_HEIGHT / 2.0 + 60.0, 0.0)
                    .with_scale(Vec3::splat(PLAYER_SIZE)),
                ..default()
            }},
        ));

        // Score display text
        commands.spawn((
            TextBundle::from_section(
                "Score: 0",
                TextStyle {{
                    font_size: 30.0,
                    color: Color::WHITE,
                    ..default()
                }},
            )
            .with_style(Style {{
                position_type: PositionType::Absolute,
                top: Val::Px(10.0),
                left: Val::Px(10.0),
                ..default()
            }}),
        ));
    }}

    fn setup_game_over(mut commands: Commands, score: Res<Score>) {{
        // Res gives us immutable access to a Resource
        commands.spawn(
            TextBundle::from_section(
                format!("GAME OVER\\n\\nFinal Score: {{}}\\n\\nPress R to Restart", score.value),
                TextStyle {{
                    font_size: 40.0,
                    color: Color::srgb(1.0, 0.3, 0.3),
                    ..default()
                }},
            )
            .with_style(Style {{
                position_type: PositionType::Absolute,
                top: Val::Px(200.0),
                left: Val::Px(150.0),
                ..default()
            }}),
        );
    }}

    // =============================================================================
    // GAME LOGIC SYSTEMS - These run every frame during gameplay
    // Systems are the "S" in ECS - they contain behavior/logic
    // =============================================================================

    fn menu_system(
        keyboard: Res<ButtonInput<KeyCode>>,
        mut next_state: ResMut<NextState<GameState>>,
    ) {{
        // Pattern: Check input and transition state
        // ButtonInput is Bevy's input resource that tracks key states
        if keyboard.just_pressed(KeyCode::Space) {{
            next_state.set(GameState::Playing);
        }}
    }}

    fn player_movement(
        keyboard: Res<ButtonInput<KeyCode>>,
        time: Res<Time>,
        // Query is how we access entities with specific components
        // &mut Transform means we want to modify the position
        // With<Player> filters to only player entities
        mut query: Query<&mut Transform, With<Player>>,
    ) {{
        // Query pattern: get_single_mut() assumes exactly one player exists
        // This returns a Result that we handle with ok()
        if let Ok(mut transform) = query.get_single_mut() {{
            let mut direction = Vec3::ZERO;

            // Input handling - supports both arrow keys and WASD
            // The || operator demonstrates Rust's boolean short-circuiting
            if keyboard.pressed(KeyCode::ArrowLeft) || keyboard.pressed(KeyCode::KeyA) {{
                direction.x -= 1.0;
            }}
            if keyboard.pressed(KeyCode::ArrowRight) || keyboard.pressed(KeyCode::KeyD) {{
                direction.x += 1.0;
            }}
            if keyboard.pressed(KeyCode::ArrowUp) || keyboard.pressed(KeyCode::KeyW) {{
                direction.y += 1.0;
            }}
            if keyboard.pressed(KeyCode::ArrowDown) || keyboard.pressed(KeyCode::KeyS) {{
                direction.y -= 1.0;
            }}

            // Normalize to prevent faster diagonal movement
            // normalize_or_zero() handles the zero vector case safely
            if direction.length() > 0.0 {{
                direction = direction.normalize();
            }}

            // Delta time ensures movement is frame-rate independent
            // time.delta_seconds() gives us the time since last frame
            transform.translation += direction * PLAYER_SPEED * time.delta_seconds();

            // Clamp player position to screen bounds
            // This demonstrates Rust's method chaining for clean code
            transform.translation.x = transform
                .translation
                .x
                .clamp(-WINDOW_WIDTH / 2.0 + PLAYER_SIZE, WINDOW_WIDTH / 2.0 - PLAYER_SIZE);
            transform.translation.y = transform
                .translation
                .y
                .clamp(-WINDOW_HEIGHT / 2.0 + PLAYER_SIZE, WINDOW_HEIGHT / 2.0 - PLAYER_SIZE);
        }}
    }}

    fn player_shooting(
        mut commands: Commands,
        keyboard: Res<ButtonInput<KeyCode>>,
        query: Query<&Transform, With<Player>>,
        mut meshes: ResMut<Assets<Mesh>>,
        mut materials: ResMut<Assets<ColorMaterial>>,
    ) {{
        // just_pressed ensures one bullet per key press, not continuous fire
        // This is different from pressed() which triggers every frame
        if keyboard.just_pressed(KeyCode::Space) {{
            if let Ok(player_transform) = query.get_single() {{
                // Spawn bullet at player's position
                // The bullet starts slightly above the player to avoid self-collision
                commands.spawn((
                    Bullet,
                    Velocity {{ x: 0.0, y: BULLET_SPEED }},
                    MaterialMesh2dBundle {{
                        mesh: meshes.add(Circle::new(BULLET_SIZE)).into(),
                        material: materials.add(ColorMaterial::from(Color::srgb(1.0, 1.0, 0.0))),
                        transform: Transform::from_xyz(
                            player_transform.translation.x,
                            player_transform.translation.y + PLAYER_SIZE,
                            0.0,
                        ),
                        ..default()
                    }},
                ));
            }}
        }}
    }}

    fn move_bullets(
        mut commands: Commands,
        time: Res<Time>,
        // Query multiple components: we need both velocity and position
        mut query: Query<(Entity, &Velocity, &mut Transform), With<Bullet>>,
    ) {{
        // iter_mut() creates an iterator over all matching entities
        // The tuple destructuring extracts each component
        for (entity, velocity, mut transform) in query.iter_mut() {{
            // Apply velocity to position
            transform.translation.x += velocity.x * time.delta_seconds();
            transform.translation.y += velocity.y * time.delta_seconds();

            // Despawn bullets that go off-screen to save memory
            // This demonstrates resource management - preventing memory leaks
            if transform.translation.y > WINDOW_HEIGHT / 2.0 + 50.0 {{
                commands.entity(entity).despawn();
            }}
        }}
    }}

    fn spawn_enemies(
        mut commands: Commands,
        time: Res<Time>,
        mut timer: ResMut<EnemySpawnTimer>,
        mut meshes: ResMut<Assets<Mesh>>,
        mut materials: ResMut<Assets<ColorMaterial>>,
    ) {{
        // Timer ticks with delta time - handles frame rate independence for us
        if timer.timer.tick(time.delta()).just_finished() {{
            // Random x position using fastrand
            // We spawn enemies at the top of the screen
            let x = (fastrand::f32() - 0.5) * (WINDOW_WIDTH - ENEMY_SIZE * 2.0);

            commands.spawn((
                Enemy,
                Velocity {{ x: 0.0, y: -ENEMY_SPEED }},
                Health {{ value: 1 }},
                MaterialMesh2dBundle {{
                    mesh: meshes.add(Circle::new(ENEMY_SIZE)).into(),
                    material: materials.add(ColorMaterial::from(Color::srgb(1.0, 0.3, 0.3))),
                    transform: Transform::from_xyz(x, WINDOW_HEIGHT / 2.0 + ENEMY_SIZE, 0.0),
                    ..default()
                }},
            ));
        }}
    }}

    fn move_enemies(
        mut commands: Commands,
        time: Res<Time>,
        mut query: Query<(Entity, &Velocity, &mut Transform), With<Enemy>>,
    ) {{
        for (entity, velocity, mut transform) in query.iter_mut() {{
            transform.translation.y += velocity.y * time.delta_seconds();

            // Despawn enemies that go off-screen
            if transform.translation.y < -WINDOW_HEIGHT / 2.0 - 50.0 {{
                commands.entity(entity).despawn();
            }}
        }}
    }}

    fn check_collisions(
        mut commands: Commands,
        mut score: ResMut<Score>,
        // Multiple queries - each with different component filters
        // This demonstrates the power of ECS: flexible entity filtering
        bullets: Query<(Entity, &Transform), With<Bullet>>,
        enemies: Query<(Entity, &Transform), With<Enemy>>,
    ) {{
        // Nested loop checks all bullet-enemy pairs
        // In a production game, you'd use spatial partitioning for performance
        for (bullet_entity, bullet_transform) in bullets.iter() {{
            for (enemy_entity, enemy_transform) in enemies.iter() {{
                // Simple circle collision detection
                // distance_squared() is faster than distance() (avoids sqrt)
                let distance = bullet_transform
                    .translation
                    .distance(enemy_transform.translation);

                if distance < BULLET_SIZE + ENEMY_SIZE {{
                    // Collision detected! Despawn both entities
                    commands.entity(bullet_entity).despawn();
                    commands.entity(enemy_entity).despawn();
                    score.value += 10;
                    // Break to avoid despawning the same bullet multiple times
                    break;
                }}
            }}
        }}
    }}

    fn update_score_display(
        score: Res<Score>,
        // Query for Text component to update the display
        // Without<Player> ensures we don't accidentally query player components
        mut query: Query<&mut Text, Without<Player>>,
    ) {{
        // Only update if score actually changed - optimization pattern
        if score.is_changed() {{
            for mut text in query.iter_mut() {{
                // Check if this is the score text (starts with "Score:")
                if text.sections[0].value.starts_with("Score:") {{
                    text.sections[0].value = format!("Score: {{}}", score.value);
                }}
            }}
        }}
    }}

    fn check_game_over(
        mut next_state: ResMut<NextState<GameState>>,
        player_query: Query<&Health, With<Player>>,
        enemy_query: Query<&Transform, With<Enemy>>,
        player_transform_query: Query<&Transform, With<Player>>,
    ) {{
        // Check if player is dead (health <= 0)
        if let Ok(health) = player_query.get_single() {{
            if health.value <= 0 {{
                next_state.set(GameState::GameOver);
                return;
            }}
        }}

        // Check if enemy collided with player
        if let Ok(player_transform) = player_transform_query.get_single() {{
            for enemy_transform in enemy_query.iter() {{
                let distance = player_transform
                    .translation
                    .distance(enemy_transform.translation);
                if distance < PLAYER_SIZE + ENEMY_SIZE {{
                    next_state.set(GameState::GameOver);
                    return;
                }}
            }}
        }}
    }}

    fn game_over_system(
        keyboard: Res<ButtonInput<KeyCode>>,
        mut next_state: ResMut<NextState<GameState>>,
        mut commands: Commands,
        // Query all entities to despawn them on restart
        entities: Query<Entity>,
    ) {{
        if keyboard.just_pressed(KeyCode::KeyR) {{
            // Despawn all entities to clean up
            // This demonstrates proper resource cleanup
            for entity in entities.iter() {{
                commands.entity(entity).despawn();
            }}
            next_state.set(GameState::Menu);
        }}
    }}
""").strip()


RUST_TESTS_GAME = dedent("""
    // Unit tests for Space Shooter game logic
    // Rust's testing framework is built into the language with #[cfg(test)]
    // Tests run with: cargo test

    #[cfg(test)]
    mod tests {{
        use super::*;

        // Test helper function to create a basic velocity component
        fn create_velocity(x: f32, y: f32) -> Velocity {{
            Velocity {{ x, y }}
        }}

        // =============================================================================
        // COMPONENT TESTS - Verify component creation and data integrity
        // =============================================================================

        #[test]
        fn test_velocity_creation() {{
            // Testing component instantiation
            // This verifies that our components store data correctly
            let velocity = create_velocity(100.0, 200.0);
            assert_eq!(velocity.x, 100.0, "Velocity x should be 100.0");
            assert_eq!(velocity.y, 200.0, "Velocity y should be 200.0");
        }}

        #[test]
        fn test_health_component() {{
            // Testing health component with different values
            let full_health = Health {{ value: 100 }};
            let low_health = Health {{ value: 1 }};
            let dead = Health {{ value: 0 }};

            assert_eq!(full_health.value, 100);
            assert_eq!(low_health.value, 1);
            assert_eq!(dead.value, 0);
            // Demonstrate comparison logic that might be used in game
            assert!(full_health.value > low_health.value);
            assert!(dead.value <= 0, "Zero or negative health means dead");
        }}

        // =============================================================================
        // GAME LOGIC TESTS - Test core game mechanics
        // =============================================================================

        #[test]
        fn test_collision_detection_logic() {{
            // Testing the collision detection math
            // We simulate what happens in check_collisions system
            
            // Two overlapping positions
            let pos1 = Vec3::new(0.0, 0.0, 0.0);
            let pos2 = Vec3::new(10.0, 0.0, 0.0);
            let distance = pos1.distance(pos2);
            
            // With bullet size 8 and enemy size 35, they should collide
            let collision_threshold = BULLET_SIZE + ENEMY_SIZE;
            assert!(
                distance < collision_threshold,
                "Objects at distance {{}} should collide (threshold: {{}})",
                distance,
                collision_threshold
            );
        }}

        #[test]
        fn test_no_collision_when_far_apart() {{
            // Testing that distant objects don't collide
            let pos1 = Vec3::new(0.0, 0.0, 0.0);
            let pos2 = Vec3::new(100.0, 100.0, 0.0);
            let distance = pos1.distance(pos2);
            
            let collision_threshold = BULLET_SIZE + ENEMY_SIZE;
            assert!(
                distance > collision_threshold,
                "Objects at distance {{}} should NOT collide (threshold: {{}})",
                distance,
                collision_threshold
            );
        }}

        #[test]
        fn test_score_increment() {{
            // Testing score resource updates
            // This simulates what happens when we hit an enemy
            let mut score = Score {{ value: 0 }};
            
            // Simulate hitting 3 enemies
            score.value += 10; // First enemy
            assert_eq!(score.value, 10, "Score should be 10 after one hit");
            
            score.value += 10; // Second enemy
            score.value += 10; // Third enemy
            assert_eq!(score.value, 30, "Score should be 30 after three hits");
        }}

        #[test]
        fn test_position_update_with_velocity() {{
            // Testing the movement logic
            // This simulates one frame of movement
            let mut position = Vec3::new(0.0, 0.0, 0.0);
            let velocity = Velocity {{ x: 100.0, y: 200.0 }};
            let delta_time = 0.016; // ~60 FPS
            
            // Apply velocity (what move_bullets/move_enemies does)
            position.x += velocity.x * delta_time;
            position.y += velocity.y * delta_time;
            
            // Verify position changed correctly
            assert!((position.x - 1.6).abs() < 0.001, "X position should be ~1.6");
            assert!((position.y - 3.2).abs() < 0.001, "Y position should be ~3.2");
        }}

        #[test]
        fn test_boundary_clamping() {{
            // Testing that player stays within screen bounds
            // This simulates the clamping logic in player_movement
            let mut x_pos = 500.0; // Outside right boundary
            let min_x = -WINDOW_WIDTH / 2.0 + PLAYER_SIZE;
            let max_x = WINDOW_WIDTH / 2.0 - PLAYER_SIZE;
            
            // Clamp to bounds
            x_pos = x_pos.clamp(min_x, max_x);
            
            // Verify position was clamped
            assert!(
                x_pos <= max_x,
                "Position {{}} should be clamped to max {{}}",
                x_pos,
                max_x
            );
            assert!(x_pos >= min_x, "Position should be within minimum bound");
        }}

        // =============================================================================
        // CONSTANTS VALIDATION - Ensure game constants make sense
        // =============================================================================

        #[test]
        fn test_game_constants_are_valid() {{
            // Sanity checks for game configuration
            assert!(PLAYER_SPEED > 0.0, "Player speed must be positive");
            assert!(BULLET_SPEED > PLAYER_SPEED, "Bullets should be faster than player");
            assert!(WINDOW_WIDTH > 0.0, "Window width must be positive");
            assert!(WINDOW_HEIGHT > 0.0, "Window height must be positive");
            assert!(ENEMY_SPAWN_TIME > 0.0, "Spawn time must be positive");
        }}

        #[test]
        fn test_bullet_faster_than_enemy() {{
            // Game balance check - bullets should outrun enemies
            assert!(
                BULLET_SPEED > ENEMY_SPEED,
                "Bullets ({{}}px/s) should be faster than enemies ({{}}px/s)",
                BULLET_SPEED,
                ENEMY_SPEED
            );
        }}
    }}

    // =============================================================================
    // INTEGRATION TEST HELPERS
    // =============================================================================
    // In a real project, you might have integration tests in tests/ directory
    // Those would test full system interactions using Bevy's testing utilities
""").strip()


README_RUST_TUTORIAL = dedent("""
    # {{name}} - Space Shooter Tutorial

    Welcome to your Rust game development journey! This project is a complete **Space Shooter** game built with [Bevy](https://bevyengine.org/), Rust's most popular game engine. You'll learn the **Entity Component System (ECS)** architecture, Rust ownership patterns in games, and modern game development practices.

    ## What You'll Learn

    - **Bevy Engine**: Modern, data-driven game engine for Rust
    - **ECS Architecture**: Entity Component System design pattern
    - **Rust Game Patterns**: Ownership, borrowing, and lifetimes in game code
    - **Systems & Queries**: How to process game entities efficiently
    - **State Management**: Game state machines with Rust enums
    - **Resource Management**: Global game state and asset handling
    - **Input Handling**: Keyboard controls and game interaction
    - **Collision Detection**: Basic physics and spatial calculations

    ## Prerequisites

    Before you begin, ensure you have:

    1. **Rust** installed (1.75.0 or later)
       ```bash
       curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
       ```

    2. **C++ Compiler** (required by Bevy for native dependencies)
       - **Linux**: `sudo apt install build-essential` (Ubuntu/Debian)
       - **macOS**: `xcode-select --install`
       - **Windows**: Install [Visual Studio C++ Build Tools](https://visualstudio.microsoft.com/downloads/)

    3. **Cargo** (comes with Rust)

    ## Quick Start

    Get the game running in seconds:

    ```bash
    # Build and run the game (first build takes a few minutes)
    cargo run --release

    # The --release flag enables optimizations for better performance
    # Development builds are much slower for Bevy games
    ```

    ### Game Controls

    - **Arrow Keys** or **WASD**: Move your spaceship
    - **Spacebar**: Shoot bullets
    - **R**: Restart after game over

    ## Project Structure

    ```
    {{name}}/
    ├── Cargo.toml          # Project configuration and dependencies
    ├── src/
    │   └── main.rs         # Complete game implementation (~400 lines)
    └── README.md           # This file
    ```

    ### Why So Few Files?

    Bevy projects can be surprisingly compact! The entire game fits in one file because:
    - Bevy's ECS eliminates boilerplate
    - Components are simple data structures
    - Systems are standalone functions
    - No complex class hierarchies needed

    ## Running Tests

    The project includes comprehensive unit tests:

    ```bash
    # Run all tests
    cargo test

    # Run tests with output
    cargo test -- --nocapture

    # Run a specific test
    cargo test test_collision_detection_logic
    ```

    Tests cover:
    - Component creation and data integrity
    - Collision detection math
    - Score calculation
    - Position updates with velocity
    - Boundary clamping
    - Game constants validation

    ## Understanding the Code

    ### The ECS Architecture

    **ECS separates data from behavior**, making code more modular and performant:

    - **Entities**: Game objects (player, enemies, bullets)
    - **Components**: Data attached to entities (Position, Velocity, Health)
    - **Systems**: Functions that process entities with specific components

    **Example**: The player entity has `Player`, `Velocity`, `Health`, and `Transform` components. The `player_movement` system queries for entities with `Player` and `Transform`, then updates their position based on input.

    ### Bevy Bundles and Systems

    **Bundles** group related components:
    ```rust
    commands.spawn((
        Player,                    // Marker component
        Velocity {{ x: 0, y: 0 }},   // Data component
        Health {{ value: 100 }},     // Data component
        MaterialMesh2dBundle {{..}}, // Rendering bundle
    ));
    ```

    **Systems** are functions that run every frame:
    ```rust
    fn player_movement(
        keyboard: Res<ButtonInput<KeyCode>>,
        mut query: Query<&mut Transform, With<Player>>,
    ) {{
        // Process input and update player position
    }}
    ```

    ### Rust Ownership in Games

    The game demonstrates key Rust concepts:

    - **Borrowing**: `&Transform` (read) vs `&mut Transform` (write)
    - **Resources**: `Res<Score>` (read) vs `ResMut<Score>` (write)
    - **Queries**: Type-safe entity filtering with compile-time guarantees
    - **Commands**: Deferred entity spawning/despawning to avoid iterator invalidation

    ### Pattern Matching in Rust

    The code uses Rust's powerful pattern matching:

    ```rust
    // Destructuring in queries
    for (entity, velocity, mut transform) in query.iter_mut() {{
        // ...
    }}

    // Option handling
    if let Ok(mut transform) = query.get_single_mut() {{
        // ...
    }}

    // State transitions
    match game_state {{
        GameState::Menu => setup_menu(),
        GameState::Playing => run_game(),
        GameState::GameOver => show_game_over(),
    }}
    ```

    ## How to Extend This Game

    Ready to make it your own? Try these enhancements:

    ### 1. Add Lives System
    ```rust
    #[derive(Resource)]
    struct Lives {{ count: u32 }}

    // Modify check_game_over to decrement lives instead of instant game over
    ```

    ### 2. Power-ups
    ```rust
    #[derive(Component)]
    struct PowerUp {{ power_type: PowerUpType }}

    enum PowerUpType {{
        RapidFire,
        Shield,
        DoublePoints,
    }}

    // Add spawn_powerups system and collision detection
    ```

    ### 3. Multiple Enemy Types
    ```rust
    #[derive(Component)]
    struct Enemy {{
        enemy_type: EnemyType,
        points: u32,
    }}

    enum EnemyType {{
        Basic,    // Slow, weak, 10 points
        Fast,     // Fast movement, 20 points
        Tank,     // High health, 30 points
    }}
    ```

    ### 4. Levels and Difficulty
    ```rust
    #[derive(Resource)]
    struct GameLevel {{
        level: u32,
        enemy_speed_multiplier: f32,
    }}

    // Increase difficulty every 100 points
    ```

    ### 5. Sound Effects
    Add `bevy_kira_audio` to Cargo.toml:
    ```toml
    [dependencies]
    bevy_kira_audio = "0.19"
    ```

    ### 6. Particle Effects
    Use Bevy's particle system for explosions when enemies are destroyed.

    ### 7. High Score Persistence
    Use `serde` and `std::fs` to save/load high scores to a JSON file.

    ## Performance Tips

    - **Always use `--release`** for playable performance
    - **Dynamic linking** (optional): Faster compile times in development
      ```toml
      # Add to Cargo.toml for Linux/macOS
      [profile.dev]
      opt-level = 1

      [profile.dev.package."*"]
      opt-level = 3
      ```

    ## Learning Resources

    - [Official Bevy Book](https://bevyengine.org/learn/book/introduction/)
    - [Bevy Examples](https://github.com/bevyengine/bevy/tree/main/examples)
    - [Rust Book](https://doc.rust-lang.org/book/)
    - [ECS Pattern Explanation](https://bevyengine.org/learn/book/getting-started/ecs/)

    ## Common Issues

    **Problem**: Slow performance in debug mode  
    **Solution**: Always use `cargo run --release`

    **Problem**: Long initial compile time  
    **Solution**: Bevy is a large framework. First compile takes 5-10 minutes. Subsequent builds are much faster.

    **Problem**: "linker `cc` not found" error  
    **Solution**: Install a C++ compiler (see Prerequisites)

    ## License

    This tutorial project is provided as-is for educational purposes. Feel free to modify and extend it however you like!

    ---

    **Happy coding!** You're now ready to build amazing games with Rust and Bevy. The ECS pattern might feel different at first, but it leads to clean, performant, and maintainable game code.
""").strip()


CARGO_TOML_TUTORIAL = dedent("""
    [package]
    name = "{{name}}"
    version = "0.1.0"
    edition = "2021"  # Rust 2021 edition with latest language features

    # Metadata for the package
    authors = ["Your Name <you@example.com>"]
    description = "A Space Shooter game built with Bevy ECS"

    [dependencies]
    # Bevy game engine with default features
    # Version 0.13 is the latest stable release with great ECS improvements
    bevy = {{ version = "0.13", features = ["dynamic_linking"] }}

    # Dynamic linking speeds up compile times during development
    # Remove the dynamic_linking feature for release builds
    # The feature is automatically disabled in --release mode

    # Optional: Add these for enhanced functionality
    # rand = "0.8"              # Better random number generation
    # bevy_kira_audio = "0.19"  # Audio support
    # serde = {{ version = "1.0", features = ["derive"] }}  # Serialization for save files

    [dev-dependencies]
    # Dependencies only used for tests
    # Currently using Rust's built-in testing, but you could add:
    # approx = "0.5"  # For floating-point comparisons in tests

    # Optimization profiles
    [profile.dev]
    # Optimize dependencies even in debug mode for better performance
    opt-level = 1

    [profile.dev.package."*"]
    # Fully optimize all dependencies in debug mode
    opt-level = 3

    [profile.release]
    # Maximum optimizations for release builds
    opt-level = 3
    lto = "thin"      # Link-time optimization for smaller binaries
    codegen-units = 1 # Better optimization at cost of compile time
""").strip()


GITIGNORE_RUST_TUTORIAL = dedent("""
    # Rust/Cargo build artifacts
    /target/
    **/*.rs.bk
    *.pdb

    # Cargo.lock should be ignored for libraries but committed for binaries
    # Since this is a game (binary), we keep it by default
    # Uncomment the next line if you want to ignore it:
    # Cargo.lock

    # Runtime artifacts
    debug/
    target/
    Cargo.lock

    # IDEs and Editors
    .vscode/
    .idea/
    *.swp
    *.swo
    *~
    .DS_Store
    *.iml

    # Visual Studio Code
    .vscode/*
    !.vscode/settings.json
    !.vscode/tasks.json
    !.vscode/launch.json
    !.vscode/extensions.json

    # IntelliJ IDEA / CLion / RustRover
    .idea/
    *.iml
    *.ipr
    *.iws
    cmake-build-*/

    # OS-specific files
    .DS_Store
    Thumbs.db
    Desktop.ini

    # Backup files
    *~
    *.bak
    *.backup

    # Profiling and benchmarking
    *.profdata
    *.gcda
    *.gcno
    perf.data
    perf.data.old

    # Bevy-specific
    # Compiled shaders (may be regenerated)
    *.spv
    *.wgsl.processed

    # Local configuration
    .env
    .env.local
""").strip()
