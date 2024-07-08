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

# Calculate a relative font size based on screen dimensions
relative_font_size = int(min(user_dimensions[0], user_dimensions[1]) * 0.05)
font = pygame.font.Font(None, relative_font_size)

# Initialise Map
map_rendoror = MapDrawer(current_map, (rows, cols), 0, colors)

# Initialize Player instance
player_position, seeker_positions = map_rendoror.player_pos, map_rendoror.seeker_positions

# Initialise variable to track game completion rate
GAME_COMPLETE = False
GAME_COMPLETION_RATE = map_reader.current_stage / map_reader.total_stages
GAME_WON = True

# Main game loop
running = True
clock = pygame.time.Clock()

while running:

    screen.fill(colors["BACKGROUND_COLOR"])
    if GAME_WON:

        # WIN MESSAGE
        win_message_text = messages["win"]["win_text"].format(stage=map_reader.current_stage)
        win_message = font.render(win_message_text, True, colors["TEXT_COLOR"])
        
        # NEXT LEVEL MESSAGE
        next_level_message_text = messages["win"]["next_level_text"]
        next_level_message = font.render(next_level_message_text, True, colors["TEXT_COLOR"])
        
        # EXIT MESSAGE
        exit_message_text = messages["exit"]["exit_text"]
        exit_message = font.render(exit_message_text, True, colors["TEXT_COLOR"])

        # Calculate positions
        screen_rect = screen.get_rect()
        win_message_rect = win_message.get_rect(center=(screen_rect.centerx, screen_rect.centery - 40))
        next_level_message_rect = next_level_message.get_rect(center=(screen_rect.centerx, screen_rect.centery))
        exit_message_rect = exit_message.get_rect(center=(screen_rect.centerx, screen_rect.centery + 40))

        # Blit messages to the screen
        screen.blit(win_message, win_message_rect)

        if not GAME_COMPLETE:
            screen.blit(next_level_message, next_level_message_rect)

        screen.blit(exit_message, exit_message_rect)

        print(f"Win message: {win_message_text}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not GAME_COMPLETE:

                    if map_reader.total_stages > map_reader: 
                        map_reader.current_stage += 1
                        current_map = map_reader.readMap()
                        rows, cols = map_reader.mapDimensions()
                        renderor.map_dimensions = (rows, cols)
                        screen = renderor.setScreen()
                        player_position, seeker_positions = map_rendoror.player_pos, map_rendoror.seeker_positions
                        GAME_WON = False

                    else:
                        GAME_COMPLETE = True
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()
