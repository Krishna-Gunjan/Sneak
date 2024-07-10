import pygame
import sys
import json
import os
from screen_dimension import get_screen_dimensions
from map_reader import read_grid
from display import Display
from draw_map import GameMap
from read_theme import read_theme

class SeekerGame:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.stages = ['stage_1.txt', 'stage_2.txt']
        self.current_stage = 0

        # Read theme
        self.theme = read_theme(r'src\theme.json')

        # Get screen dimensions
        self.screen_width, self.screen_height = get_screen_dimensions()

        # Load initial grid
        self.grid = read_grid('maps\\' + self.stages[self.current_stage])
        self.rows, self.cols = len(self.grid), len(self.grid[0])

        # Calculate tile sizes
        self.x_size = self.screen_width / self.cols
        self.y_size = self.screen_height / self.rows

        # Set up the initial screen
        self.display = Display(self.screen_width, self.screen_height, self.x_size, self.y_size, self.theme)
        self.game_map = GameMap(self.grid, self.x_size, self.y_size, self.theme)

        self.player_pos, self.seeker_positions = self.game_map.reset_game()
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_won = False
        self.all_levels_cleared = False
        self.initial_circle_radius = 10

    def run(self):
        while self.running:
            self.display.screen.fill(self.theme['BACKGROUND_COLOR'])
            if self.game_won:
                self.handle_win()
            else:
                self.handle_gameplay()

            pygame.display.flip()
            self.clock.tick(10)
        pygame.quit()
        sys.exit()
