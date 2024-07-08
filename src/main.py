import pygame
import sys
from read_theme import read_json
from map_reader import MapReader
from display import Display
from draw_map import MapDrawer

# Initialize the color scheme
colors = read_json(r'src\theme.json')

# Initialize pygame
pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 40)

# Initialize maps
map_reader = MapReader()
current_map = map_reader.readMap()
rows, cols = map_reader.mapDimensions()

# Initialize Screen
renderor = Display((rows, cols))
screen = renderor.setScreen()
tile_size = renderor.getTileSize()

# Initialise Map
map_rendoror = MapDrawer(current_map, (rows, cols), 0, colors)

running = True
clock = pygame.time.Clock()
while running:
    screen.fill(colors["BACKGROUND_COLOR"])

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running =False

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()
