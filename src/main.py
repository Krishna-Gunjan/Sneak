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

        self.player_pos, self.seeker_positions = self.game_map.resetGame()
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

    def handle_win(self):
        self.display.showWinScreen(self.cols, self.rows, self.all_levels_cleared)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.all_levels_cleared:
                    self.current_stage += 1
                    if self.current_stage < len(self.stages):
                        self.grid = read_grid('maps\\' + self.stages[self.current_stage])
                        self.game_map.grid = self.grid
                        self.rows, self.cols = len(self.grid), len(self.grid[0])
                        self.x_size = self.screen_width / self.cols
                        self.y_size = self.screen_height / self.rows
                        self.display.updateScreenSize(self.cols, self.rows)
                        self.player_pos, self.seeker_positions = self.game_map.resetGame()
                        self.game_won = False
                    else:
                        self.all_levels_cleared = True
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.QUIT:
                self.running = False

    def handle_gameplay(self):
        self.game_map.drawGrid(self.display.screen, self.player_pos, self.seeker_positions, self.initial_circle_radius)
        self.game_map.updateSeekers()

        if self.game_map.checkCollisions(self.player_pos, self.seeker_positions, self.initial_circle_radius, self.x_size, self.y_size):
            print("YOU LOST")
            self.initial_circle_radius = 10
            self.player_pos, self.seeker_positions = self.game_map.resetGame()

        if self.grid[self.player_pos[1]][self.player_pos[0]] == 'E':
            self.game_won = True
            if self.current_stage == len(self.stages) - 1:
                self.all_levels_cleared = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                new_pos = self.player_pos[:]
                if event.key == pygame.K_LEFT:
                    new_pos[0] -= 1
                elif event.key == pygame.K_RIGHT:
                    new_pos[0] += 1
                elif event.key == pygame.K_UP:
                    new_pos[1] -= 1
                elif event.key == pygame.K_DOWN:
                    new_pos[1] += 1
                if self.grid[new_pos[1]][new_pos[0]] != '#':
                    self.player_pos = new_pos
                    self.initial_circle_radius += 4
        if not self.game_won:
            self.initial_circle_radius = max(10, self.initial_circle_radius - 1)

if __name__ == '__main__':
    game = SeekerGame()
    game.run()
