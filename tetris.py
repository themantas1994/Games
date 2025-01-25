import pygame
import random

# Constants
WIDTH = 300
HEIGHT = 660
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
FPS = 30
FALL_SPEED = 1.25
FAST_FALL_MULTIPLIER = 20
BORDER_WIDTH = 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Tetromino shapes
SHAPES = [
    {'rotations': [[[1, 1, 1, 1]], [[1], [1], [1], [1]]], 'color': CYAN},
    {'rotations': [[[1, 0, 0], [1, 1, 1]], [[1, 1], [1, 0], [1, 0]], [[1, 1, 1], [0, 0, 1]], [[0, 1], [0, 1], [1, 1]]], 'color': ORANGE},
    {'rotations': [[[0, 0, 1], [1, 1, 1]], [[1, 0], [1, 0], [1, 1]], [[1, 1, 1], [1, 0, 0]], [[1, 1], [0, 1], [0, 1]]], 'color': BLUE},
    {'rotations': [[[1, 1], [1, 1]]], 'color': YELLOW},
    {'rotations': [[[0, 1, 1], [1, 1, 0]], [[1, 0], [1, 1], [0, 1]]], 'color': GREEN},
    {'rotations': [[[0, 1, 0], [1, 1, 1]], [[1, 0], [1, 1], [1, 0]], [[1, 1, 1], [0, 1, 0]], [[0, 1], [1, 1], [0, 1]]], 'color': PURPLE},
    {'rotations': [[[1, 1, 0], [0, 1, 1]], [[0, 1], [1, 1], [1, 0]]], 'color': RED}
]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH + 150, HEIGHT)) 
pygame.display.set_caption("Simple Tetris")
clock = pygame.time.Clock()

# Game functions
def draw_next_tetromino(tetromino):
    """Draws the next tetromino in a preview window."""
    preview_x = GRID_WIDTH + 2  # Start position in the preview window
    preview_y = 2
    shape = tetromino['rotations'][0] 
    for y in range(len(shape)):
        for x in range(len(shape[y])):
            if shape[y][x]:
                draw_block(preview_x + x, preview_y + y, tetromino['color'])

def try_rotate(tetromino, grid):
    original_rotation = tetromino['rotation']
    tetromino['rotation'] = (tetromino['rotation'] + 1) % len(tetromino['rotations'])
    if not check_collision(tetromino, grid):
        return True

    # Wall kick attempts (simplified)
    for x_offset in [-1, 1]:
        if not check_collision(tetromino, grid, x_offset=x_offset):
            tetromino['x'] += x_offset
            return True

    tetromino['rotation'] = original_rotation
    return False

def draw_next_tetromino(tetromino):
    preview_x = GRID_WIDTH + 2
    preview_y = 2
    shape = tetromino['rotations'][0]
    for y in range(len(shape)):
        for x in range(len(shape[y])):
            if shape[y][x]:
                draw_block(preview_x + x, preview_y + y, tetromino['color'])

def new_tetromino():
    shape_data = random.choice(SHAPES)
    return {
        'rotations': shape_data['rotations'],
        'color': shape_data['color'],
        'rotation': 0,
        'x': GRID_WIDTH // 2 - len(shape_data['rotations'][0][0]) // 2,
        'y': 0,
        'shape_index': SHAPES.index(shape_data)
    }

def draw_block(x, y, color):
    pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_grid(grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                draw_block(x, y, SHAPES[grid[y][x]-1]['color'])

def draw_tetromino(tetromino):
    shape = tetromino['rotations'][tetromino['rotation']]
    for y in range(len(shape)):
        for x in range(len(shape[y])):
            if shape[y][x]:
                draw_block(tetromino['x'] + x, tetromino['y'] + y, tetromino['color'])

def check_collision(tetromino, grid, x_offset=0, y_offset=0, rotation_offset=0):
    shape = tetromino['rotations'][(tetromino['rotation'] + rotation_offset) % len(tetromino['rotations'])]
    for y in range(len(shape)):
        for x in range(len(shape[y])):
            if shape[y][x]:
                new_x = tetromino['x'] + x + x_offset
                new_y = tetromino['y'] + y + y_offset
                if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT or (new_y >= 0 and grid[new_y][new_x]):
                    return True
    return False

def clear_lines(grid):
    lines_cleared = 0
    y = 0
    while y < len(grid):
        if all(grid[y]):
            lines_cleared += 1
            del grid[y]
            grid.insert(0, [0] * GRID_WIDTH)
        else:
            y += 1
    return lines_cleared

def increase_speed(current_speed):
    """Increases the current fall speed by 10%."""
    return current_speed * 1.1 

# Game variables
grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
tetromino = new_tetromino()
next_tetromino = new_tetromino()
fall_counter = 0
score = 0
level = 1
down_pressed = False
game_over = False

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
                    tetromino = new_tetromino()
                    next_tetromino = new_tetromino()
                    fall_counter = 0
                    score = 0
                    level = 1
                    FALL_SPEED = 1.25  # Reset fall speed
                    down_pressed = False
                    game_over = False
        elif not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not check_collision(tetromino, grid, x_offset=-1):
                    tetromino['x'] -= 1
                if event.key == pygame.K_RIGHT and not check_collision(tetromino, grid, x_offset=1):
                    tetromino['x'] += 1
                if event.key == pygame.K_DOWN:
                    down_pressed = True
                if event.key == pygame.K_UP:
                    try_rotate(tetromino, grid)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    down_pressed = False

    # Game logic
    delta_time = clock.get_time()
    fall_counter += delta_time
    clock.tick(FPS)

    current_fall_speed = FALL_SPEED
    if down_pressed:
        current_fall_speed *= FAST_FALL_MULTIPLIER

    if not game_over:
        if fall_counter >= 1000 / current_fall_speed:
            fall_counter -= 1000 / current_fall_speed
            if not check_collision(tetromino, grid, y_offset=1):
                tetromino['y'] += 1
            else:
                # Lock the tetromino in place
                shape = tetromino['rotations'][tetromino['rotation']]
                for y in range(len(shape)):
                    for x in range(len(shape[y])):
                        if shape[y][x]:
                            if 0 <= tetromino['y'] + y < GRID_HEIGHT:
                                grid[tetromino['y'] + y][tetromino['x'] + x] = tetromino['shape_index'] + 1

                # Check for game over
                new_tetromino_check = new_tetromino()
                if check_collision(new_tetromino_check, grid, 0, 0, 0):
                    game_over = True
                    print("Game Over")
                else:
                    #Clear lines and update score
                    lines_cleared = clear_lines(grid)
                    if lines_cleared > 0:
                        score += [0, 100, 300, 500, 800][lines_cleared]
                        # Level up every 1000 points (adjust as needed)
                        if score >= level * 1000:
                            level += 1
                            FALL_SPEED = increase_speed(FALL_SPEED)  # Call the function
                            print("level up")
                    tetromino = next_tetromino
                    next_tetromino = new_tetromino()

    # Draw the screen
    screen.fill(BLACK)
     # --- Draw borders ---
    # Border around the game area
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), BORDER_WIDTH)  

    # Border around the preview window
    preview_window_x = WIDTH + BORDER_WIDTH  # X-coordinate of the preview window
    pygame.draw.rect(screen, WHITE, (preview_window_x, 0, 150 - BORDER_WIDTH, 150), BORDER_WIDTH) 

    # --- Draw the rest of the game elements ---
    draw_grid(grid)
    draw_tetromino(tetromino)
    draw_next_tetromino(next_tetromino) 
    
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, WHITE)
    level_text = font.render("Level: " + str(level), True, WHITE)
    screen.blit(text, (10, 10))
    screen.blit(level_text, (10, 40))

    if game_over:
        game_over_text = font.render("Game Over", True, WHITE)
        restart_text = font.render("Press R to restart", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
