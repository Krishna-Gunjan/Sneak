import pygame
import sys
import json
import os
import ctypes

# Constants for colors and other settings
WALL_COLOR = (102, 113, 126)
SEEKER_COLOR = (255, 255, 0)
START_COLOR = (255, 0, 0)
END_COLOR = (0, 255, 0)
BACKGROUND_COLOR = (0, 0, 0)
CIRCLE_COLOR = (255, 0, 0)  # Red circumference for the circle
TEXT_COLOR = (255, 255, 255)

# Function to read JSON file (not currently used in the provided code)
def read_json():
    try:
        file_path = os.path.relpath('theme.json')
        with open(file_path, 'r') as file:
            colors = json.load(file)
        return json
    except FileNotFoundError as e:
        raise Exception("File not found")

# Function to read grid from file
def read_grid(filename):
    with open(filename, 'r') as file:
        grid = [list(line.strip()) for line in file.readlines()]
    return grid

# Function to draw the grid and game objects
def draw_grid(screen, grid, player_pos, seeker_positions, circle_radius, x_size, y_size):
    rows = len(grid)
    cols = len(grid[0])
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * x_size, y * y_size, x_size, y_size)
            if cell == '#':
                pygame.draw.rect(screen, WALL_COLOR, rect)
            elif cell == 'S':
                pygame.draw.rect(screen, START_COLOR, rect)
            elif cell == 'E':
                pygame.draw.rect(screen, END_COLOR, rect)

    player_rect = pygame.Rect(player_pos[0] * x_size, player_pos[1] * y_size, x_size, y_size)
    pygame.draw.rect(screen, START_COLOR, player_rect)

    for pos in seeker_positions:
        seeker_rect = pygame.Rect(pos[0] * x_size, pos[1] * y_size, x_size, y_size)
        pygame.draw.rect(screen, SEEKER_COLOR, seeker_rect)

    circle_center = (player_pos[0] * x_size + x_size // 2, player_pos[1] * y_size + y_size // 2)
    pygame.draw.circle(screen, CIRCLE_COLOR, circle_center, circle_radius, 3)  # Hollow circle with red circumference

# Function to reset the game state
def reset_game(grid):
    player_pos = None
    seeker_positions = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'S':
                player_pos = [x, y]
            elif cell == '$':
                seeker_positions.append([x, y, 1])  # Assuming seeker starts moving to the right initially
    return player_pos, seeker_positions

# Initialize pygame and font
pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 74)

# Define stages and initialize variables
stages = ['stage_1.txt', 'stage_2.txt', 'stage_3.txt']
current_stage = 0

# Calculate tile sizes based on screen dimensions and grid size
grid = read_grid('maps\\' + stages[current_stage])
rows, cols = len(grid), len(grid[0])

user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Calculate tile size
x_size = screen_width / cols
y_size = screen_height / rows

initial_circle_radius = 10

# Set up the initial screen
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption('Seeker Game')

# Initialize game variables
player_pos, seeker_positions = reset_game(grid)
clock = pygame.time.Clock()
running = True
game_won = False
all_levels_cleared = False

# Main game loop
while running:
    screen.fill(BACKGROUND_COLOR)

    if game_won:
        win_text = "YOU WON"
        next_level_text = "Press SPACE to go to the next level"
        exit_text = "Press ESC to exit"
        win_surface = font.render(win_text, True, TEXT_COLOR)
        next_level_surface = font.render(next_level_text, True, TEXT_COLOR)
        exit_surface = font.render(exit_text, True, TEXT_COLOR)

        screen.blit(win_surface, ((cols * int(x_size)) // 2 - win_surface.get_width() // 2, (rows * int(y_size)) // 2 - win_surface.get_height() // 2 - 40))

        if not all_levels_cleared:
            screen.blit(next_level_surface, ((cols * int(x_size)) // 2 - next_level_surface.get_width() // 2, (rows * int(y_size)) // 2 - next_level_surface.get_height() // 2))

        screen.blit(exit_surface, ((cols * int(x_size)) // 2 - exit_surface.get_width() // 2, (rows * int(y_size)) // 2 - exit_surface.get_height() // 2 + 40))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not all_levels_cleared:
                    current_stage += 1
                    if current_stage < len(stages):
                        grid = read_grid('maps\\' + stages[current_stage])
                        rows, cols = len(grid), len(grid[0])
                        x_size = screen_width / cols
                        y_size = screen_height / rows
                        screen = pygame.display.set_mode((cols * int(x_size), rows * int(y_size)))
                        player_pos, seeker_positions = reset_game(grid)
                        game_won = False
                    else:
                        all_levels_cleared = True
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.QUIT:
                running = False

    else:
        draw_grid(screen, grid, player_pos, seeker_positions, initial_circle_radius, int(x_size), int(y_size))

        for seeker in seeker_positions:
            x, y, direction = seeker
            new_x = x + direction
            if new_x < 0 or new_x >= cols or grid[y][new_x] == '#':
                direction *= -1
            else:
                seeker[0] = new_x
            seeker[2] = direction

        for seeker in seeker_positions:
            seeker_center = (seeker[0] * int(x_size) + int(x_size) // 2, seeker[1] * int(y_size) + int(y_size) // 2)
            circle_center = (player_pos[0] * int(x_size) + int(x_size) // 2, player_pos[1] * int(y_size) + int(y_size) // 2)
            distance = ((seeker_center[0] - circle_center[0]) ** 2 + (seeker_center[1] - circle_center[1]) ** 2) ** 0.5

            if distance < initial_circle_radius + int(x_size) // 2:
                print("YOU LOST")
                initial_circle_radius = 10
                player_pos, seeker_positions = reset_game(grid)

        if grid[player_pos[1]][player_pos[0]] == 'E':
            game_won = True
            if current_stage == len(stages) - 1:
                all_levels_cleared = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_won:
                    if event.key == pygame.K_SPACE and not all_levels_cleared:
                        current_stage += 1
                        if current_stage < len(stages):
                            grid = read_grid('maps\\' + stages[current_stage])
                            rows, cols = len(grid), len(grid[0])
                            x_size = screen_width / cols
                            y_size = screen_height / rows
                            screen = pygame.display.set_mode((cols * int(x_size), rows * int(y_size)))
                            player_pos, seeker_positions = reset_game(grid)
                            game_won = False
                        else:
                            all_levels_cleared = True
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                else:
                    new_pos = player_pos[:]
                    if event.key == pygame.K_LEFT:
                        new_pos[0] -= 1
                    elif event.key == pygame.K_RIGHT:
                        new_pos[0] += 1
                    elif event.key == pygame.K_UP:
                        new_pos[1] -= 1
                    elif event.key == pygame.K_DOWN:
                        new_pos[1] += 1
                    if grid[new_pos[1]][new_pos[0]] != '#':
                        player_pos = new_pos
                        initial_circle_radius += 1.5

        if not game_won and event.type != pygame.KEYDOWN:
            initial_circle_radius = max(10, initial_circle_radius - 1)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()
