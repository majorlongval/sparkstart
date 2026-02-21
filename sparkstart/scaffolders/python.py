import pathlib
import textwrap
import venv
from sparkstart.templates.python import GITIGNORE_PYTHON

def scaffold_python(path: pathlib.Path, template: str | None = None) -> None:
    """Create Python project structure with Hello World and tests."""
    (path / "src").mkdir()
    (path / "src" / "__init__.py").touch()
    
    if template == "pygame":
        # Snake Game / Pygame Template
        main_py = textwrap.dedent('''
            import pygame
            import sys
            import random

            def main():
                pygame.init()
                clock = pygame.time.Clock()
                
                # Constants
                WIDTH, HEIGHT = 600, 400
                BLOCK_SIZE = 20
                WHITE = (255, 255, 255)
                BLACK = (0, 0, 0)
                RED = (213, 50, 80)
                GREEN = (0, 255, 0)
                
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.display.set_caption('Sparkstart Snake')
                
                # Snake state
                x1, y1 = WIDTH / 2, HEIGHT / 2
                x1_change, y1_change = 0, 0
                snake_list = []
                length_of_snake = 1
                
                # Food
                foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 20.0) * 20.0
                foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 20.0) * 20.0
                
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT:
                                x1_change = -BLOCK_SIZE
                                y1_change = 0
                            elif event.key == pygame.K_RIGHT:
                                x1_change = BLOCK_SIZE
                                y1_change = 0
                            elif event.key == pygame.K_UP:
                                y1_change = -BLOCK_SIZE
                                x1_change = 0
                            elif event.key == pygame.K_DOWN:
                                y1_change = BLOCK_SIZE
                                x1_change = 0

                    if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
                        # Game Over behavior simplified: just reset
                        x1, y1 = WIDTH / 2, HEIGHT / 2
                        x1_change, y1_change = 0, 0
                        snake_list = []
                        length_of_snake = 1
                    
                    x1 += x1_change
                    y1 += y1_change
                    screen.fill(BLACK)
                    
                    pygame.draw.rect(screen, GREEN, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])
                    
                    snake_head = []
                    snake_head.append(x1)
                    snake_head.append(y1)
                    snake_list.append(snake_head)
                    if len(snake_list) > length_of_snake:
                        del snake_list[0]
                        
                    for x in snake_list:
                        pygame.draw.rect(screen, WHITE, [x[0], x[1], BLOCK_SIZE, BLOCK_SIZE])
                        
                    pygame.display.update()
                    
                    if x1 == foodx and y1 == foody:
                        foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 20.0) * 20.0
                        foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 20.0) * 20.0
                        length_of_snake += 1
                        
                    clock.tick(10)

            if __name__ == "__main__":
                main()
        ''').strip()
    else:
        # Standard Hello World
        main_py = textwrap.dedent('''
            def hello() -> str:
                return "Hello, world!"

            if __name__ == "__main__":
                print(hello())
        ''').strip()
    (path / "src" / "main.py").write_text(main_py + "\n")
    
    (path / ".gitignore").write_text(GITIGNORE_PYTHON + "\n")

    # Create tests directory
    (path / "tests").mkdir()
    (path / "tests" / "__init__.py").touch()
    
    # Sample test
    if template == "pygame":
        # Simple import test for pygame
        test_main = textwrap.dedent('''
            def test_import_pygame():
                import pygame
                assert pygame.ver is not None
        ''').strip()
    else:
        test_main = textwrap.dedent('''
            from src.main import hello

            def test_hello():
                assert hello() == "Hello, world!"
        ''').strip()
    (path / "tests" / "test_main.py").write_text(test_main + "\n")
    
    # Create pyproject.toml with pytest and optional deps
    deps = 'dependencies = []'
    if template == "pygame":
        deps = 'dependencies = ["pygame", "requests", "python-dotenv"]' # keeping original reqs + pygame
    else:
        deps = 'dependencies = ["requests", "python-dotenv"]' # Restoring original deps
    
    pyproject = textwrap.dedent(f'''
        [project]
        name = "{path.name}"
        version = "0.1.0"
        description = ""
        requires-python = ">=3.8"
        {deps}

        [project.optional-dependencies]
        test = ["pytest"]
    ''').strip()
    (path / "pyproject.toml").write_text(pyproject + "\n")
    
    # Create virtual environment
    venv.create(path / ".venv", with_pip=True)
