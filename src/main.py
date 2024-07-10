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

# Initialize MapDrawer
map_rendoror = MapDrawer(current_map, (50, 50), 10, colors)
screen_width, screen_height = map_rendoror.calculate_screen_size()

# Initialize Screen
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Map Drawer")

# Calculate a relative font size based on screen dimensions
relative_font_size = int(min(screen_width, screen_height) * 0.05)
font = pygame.font.Font(None, relative_font_size)

# Initialize Player instance
player_position, seeker_positions = map_rendoror.player_pos, map_rendoror.seeker_positions
circle_radius = map_rendoror.circle_radius

# Initialise variable to track game completion rate
GAME_COMPLETE = False
GAME_COMPLETION_RATE = map_reader.current_stage / map_reader.total_stages
GAME_WON = False

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(colors["BACKGROUND_COLOR"])
    screen_rect = screen.get_rect() 

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
        win_message_rect = win_message.get_rect(center=(screen_rect.centerx, screen_rect.centery - 40))
        next_level_message_rect = next_level_message.get_rect(center=(screen_rect.centerx, screen_rect.centery))
        exit_message_rect = exit_message.get_rect(center=(screen_rect.centerx, screen_rect.centery + 40))

        screen.blit(win_message, win_message_rect)

        if not GAME_COMPLETE:
            screen.blit(next_level_message, next_level_message_rect)

        screen.blit(exit_message, exit_message_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not GAME_COMPLETE:

                    if map_reader.total_stages > map_reader.current_stage: 
                        map_reader.current_stage += 1
                        current_map = map_reader.readMap()
                        rows, cols = map_reader.mapDimensions()
                        map_rendoror = MapDrawer(current_map, (50, 50), 10, colors)
                        screen_width, screen_height = map_rendoror.calculate_screen_size()
                        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
                        player_position, seeker_positions = map_rendoror.player_pos, map_rendoror.seeker_positions
                        GAME_WON = False
                    else:
                        # All maps are completed
                        GAME_COMPLETE = True

                elif event.key == pygame.K_ESCAPE:
                    running = False

    else:
        map_rendoror.drawMap(screen=screen)

        # Manage seeker's movements
        for seeker in seeker_positions:
            x, y, dir = seeker
            new_x = x + dir

            # If the seeker hits a wall, turn around and walk in another direction
            if new_x < 0 or new_x >= cols or current_map[y][new_x] == '#':
                dir *= -1 
            else:
                seeker[0] = new_x
            seeker[2] = dir

        for seeker in seeker_positions:
            seeker_center = (seeker[0] * int(50) + int(50) // 2, seeker[1] * int(50) + int(50) // 2)
            circle_center = (player_position[0] * int(50) + int(50) // 2, player_position[1] * int(50) + int(50) // 2)
            distance = ((seeker_center[0] - circle_center[0]) ** 2 + (seeker_center[1] - circle_center[1]) ** 2) ** 0.5

            if distance < circle_radius + int(50) // 2:
                lose_message_text = messages["lose"]["lose_text"]
                lose_message = font.render(lose_message_text, True, colors["TEXT_COLOR"])
                
                restart_message_text = messages["lose"]["restart_text"]
                restart_message = font.render(restart_message_text, True, colors["TEXT_COLOR"])

                lose_message_rect = lose_message.get_rect(center=(screen_rect.centerx, screen_rect.centery - 40))
                restart_message_rect = restart_message.get_rect(center=(screen_rect.centerx, screen_rect.centery))
                
                screen.blit(lose_message, lose_message_rect)
                screen.blit(restart_message, restart_message_rect)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:

                            current_map = map_reader.readMap()
                            rows, cols = map_reader.mapDimensions()
                            map_rendoror = MapDrawer(current_map, (50, 50), 10, colors) 
                            screen_width, screen_height = map_rendoror.calculate_screen_size()
                            screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
                            player_position, seeker_positions = map_rendoror.player_pos, map_rendoror.seeker_positions
                            GAME_WON = False

                        elif event.key == pygame.K_ESCAPE:
                            running = False
        if current_map[player_position[1]][player_position[0]] == 'E':
            GAME_WON = True

            if map_reader.current_stage == map_reader.total_stages:
                GAME_COMPLETE = True

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if GAME_WON:
                    if event.key == pygame.K_SPACE and not GAME_COMPLETE:
                        
                        if map_reader.current_stage < map_reader.total_stages:
                            map_reader.current_stage += 1
                            current_map = map_reader.readMap()
                            rows, cols = map_reader.mapDimensions()
                            map_rendoror = MapDrawer(current_map, (50, 50), 10, colors)
                            screen_width, screen_height = map_rendoror.calculate_screen_size()
                            screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
                            player_position, seeker_positions = map_rendoror.player_pos, map_rendoror.seeker_positions
                            GAME_WON = False
                        else:
                            GAME_COMPLETE = True
                    elif event.key == pygame.K_ESCAPE:
                        running = False

                else:

                    new_position = player_position
                    if event.key == pygame.K_LEFT:
                        new_position[0] -= 1
                    elif event.key == pygame.K_RIGHT:
                        new_position[0] += 1
                    elif event.key == pygame.K_UP:
                        new_position[1] -= 1
                    elif event.key == pygame.K_DOWN:
                        new_position[1] += 1
                    if current_map[new_position[1]][new_position[0]] != '#':
                        player_position = new_position
                        map_rendoror.circle_radius += 1.5

        if not GAME_WON and event.type == pygame.KEYDOWN:
            map_rendoror.circle_radius = max(10, map_rendoror.circle_radius - 1)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()
