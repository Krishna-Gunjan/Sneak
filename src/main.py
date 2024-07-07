import pygame
from read_theme import read_json
from map_reader import MapReader

# Initialize the color scheme
colors = read_json(r'src\theme.json')

# Initialize pygame
pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 40)

# Initialize maps
map_reader = MapReader()
current_map = MapReader.readMap()
rows, cols = MapReader.mapDimensions()
