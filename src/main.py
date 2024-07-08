import pygame
import sys
from read_theme import read_json
from map_reader import MapReader
from screen_dimensions import ScreenDimensions
from display import Display
from draw_map import MapDrawer

# Load JSON files 
colors = read_json(r'src\theme.json')
messages = read_json(r'src\messages.json')

# Initialize pygame
pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 40)

# Initialize maps
map_reader = MapReader()
current_map = map_reader.readMap()
rows, cols = map_reader.mapDimensions()

# Get Screen Dimensions
user_dimensions = ScreenDimensions().getDimensions()

# Initialize Screen
renderor = Display((rows, cols))
screen = renderor.setScreen()
tile_size = renderor.getTileSize()

# Initialise Map
map_rendoror = MapDrawer(current_map, (rows, cols), 0, colors)

# Initialize Player instance
player_position, seeker_positions = map_rendoror.player_pos, map_rendoror.seeker_positions

# Initialise variable to track game completion rate
GAME_COMPLETE = False
GAME_COMPLETION_RATE = map_reader.current_stage / map_reader.total_stages
GAME_WON = False

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(colors["BACKGROUND_COLOR"])

    if GAME_WON:
        win_message = font.render(messages["won"]["win_text"].format(stage=map_reader.current_stage), True, colors["TEXT_COLOR"])
        next_level_message = font.render(messages["won"]["next_level_text"], True, colors["TEXT_COLOR"])
        exit_message = font.render(messages["exit"]["exit_text"], True, colors["TEXT_COLOR"])

        screen.blit(win_message, )

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()
