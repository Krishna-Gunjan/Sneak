import pygame
import sys
import json
import os
from typing import List, Tuple
from screen_dimension import get_screen_dimensions
from map_reader import read_grid
from display import Display
from draw_map import GameMap
from read_theme import read_theme

def add_to_path():
    generator_path = os.path.abspath('src/generator/Model - 2')
    sys.path.append(generator_path)

add_to_path()
from generator import MapGenerator

class SeekerGame:
    def __init__(self) -> None:
        """
        Initialize the SeekerGame class by setting up the 
        Game environment, load stages, load theme, and the map.
        """

        # Initialize pygame
        pygame.init()
        pygame.font.init()
        
        # Read theme
        self.theme: dict = read_theme(r'src\theme.json')
        
        # Get screen dimensions
        self.screen_width: int
        self.screen_height: int
        self.screen_width, self.screen_height = get_screen_dimensions()
        
        # Initialize Map Generator
        self.map_generator = MapGenerator()
        self.map_generator.generateMap()
        
        # Load initial grid
        self.grid: List[List[str]] = self.map_generator.map
        self.rows: int = len(self.grid)
        self.cols: int = len(self.grid[0])
        
        # Calculate tile sizes
        self.x_size: float = self.screen_width / self.cols
        self.y_size: float = self.screen_height / self.rows
        
        # Set up the initial screen
        self.display: Display = Display(self.screen_width, self.screen_height, self.x_size, self.y_size, self.theme)
        self.game_map: GameMap = GameMap(self.grid, self.x_size, self.y_size, self.theme)
        
        # Set up player attributes
        self.player_pos: List[int]
        self.seeker_positions: List[List[int]]
        self.player_pos, self.seeker_positions, self.coin_positions = self.game_map.resetGame()
        self.clock: pygame.time.Clock = pygame.time.Clock()
        
        # Initialize game management variable
        self.running: bool = True
        self.game_won: bool = False
        self.all_levels_cleared: bool = False
        
        # Initial circle radius
        self.default_radius = 10
        self.initial_circle_radius: int = 10
    
    def main_menu(self) -> None:
        """
        Display the main menu and wait for user input to start the game.
        """
        while True:
            self.display.screen.fill(self.theme['BACKGROUND_COLOR'])

            font = pygame.font.SysFont(None, 74)
            title = font.render('Sneak', True, (255, 0, 0))
            self.display.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, self.screen_height // 2 - title.get_height() // 2 - 100))

            font = pygame.font.SysFont(None, 50)
            prompt1 = font.render('Press SPACE to Start or ESC to Quit', True, self.theme['TEXT_COLOR'])
            self.display.screen.blit(prompt1, (self.screen_width // 2 - prompt1.get_width() // 2, self.screen_height // 2))

            prompt2 = font.render('THE GAME IS STILL UNDER DEVELOPMENT AND MAY HAVE SOME BUGS', True, (255, 0, 0))
            self.display.screen.blit(prompt2, (self.screen_width // 2 - prompt2.get_width() // 2, self.screen_height // 2 + 50))

            prompt3 = font.render('Press R to restart the game or move to a new map', True, self.theme['TEXT_COLOR'])
            self.display.screen.blit(prompt3, (self.screen_width // 2 - prompt3.get_width() // 2, self.screen_height // 2 + 100))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_r:
                        self.map_generator.generateMap()
                        self.grid = self.map_generator.map
                        self.game_map.grid = self.grid
                        # Get new map dimensions
                        self.rows, self.cols = len(self.grid), len(self.grid[0])
                        # Calculate tile size
                        self.x_size = self.screen_width / self.cols
                        self.y_size = self.screen_height / self.rows
                        # Update the screen to display new map
                        self.display.updateScreenSize(self.cols, self.rows)
                        self.player_pos, self.seeker_positions, self.coin_positions = self.game_map.resetGame()
                        self.game_won = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def run(self) -> None:
        """
        Main game loop for running the game.
        """
        self.main_menu()
        while self.running:
            self.display.screen.fill(self.theme['BACKGROUND_COLOR'])

            # Check Game winning conditions
            if self.game_won:
                self.handle_win()
            else:
                self.handle_gameplay()

            pygame.display.flip()
            self.clock.tick(10)

        pygame.quit()
        sys.exit()

    def handle_win(self) -> None:
        """
        Handle the win state of the game.
        """

        # Display the win screen
        self.display.showWinScreen(self.cols, self.rows)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                # If user continues to the next stage
                if event.key == pygame.K_SPACE:

                    # Read next stage map
                    self.map_generator.generateMap()
                    self.grid = self.map_generator.map
                    self.game_map.grid = self.grid

                    # Get new map dimensions
                    self.rows, self.cols = len(self.grid), len(self.grid[0])

                    # Calculate tile size
                    self.x_size = self.screen_width / self.cols
                    self.y_size = self.screen_height / self.rows

                    # Update the screen to display new map
                    self.display.updateScreenSize(self.cols, self.rows)
                    self.player_pos, self.seeker_positions, self.coin_positions = self.game_map.resetGame()
                    self.game_won = False

                    self.initial_circle_radius = self.default_radius

                elif event.key == pygame.K_ESCAPE:
                    # User wants to end game
                    self.running = False
                    self.main_menu()

                elif event.key == pygame.K_r:

                    self.map_generator.generateMap()
                    self.grid = self.map_generator.map
                    self.game_map.grid = self.grid

                    # Get new map dimensions
                    self.rows, self.cols = len(self.grid), len(self.grid[0])

                    # Calculate tile size
                    self.x_size = self.screen_width / self.cols
                    self.y_size = self.screen_height / self.rows

                    # Update the screen to display new map
                    self.display.updateScreenSize(self.cols, self.rows)
                    self.player_pos, self.seeker_positions, self.coin_positions = self.game_map.resetGame()
                    self.game_won = False
                    

            elif event.type == pygame.QUIT:
                # User wants to end game
                self.running = False

    def handle_gameplay(self) -> None:
        """
        Handle the gameplay mechanics, including 
        drawing the map, updating seeker movements, and handling player input.
        """

        # Update current game with new positions
        self.game_map.drawGrid(self.display.screen, self.player_pos, self.seeker_positions, self.coin_positions, self.initial_circle_radius)
        self.game_map.updateSeekers()

        # Check Collisions
        seeker_collision, coin_collision = self.game_map.checkCollisions(self.player_pos, self.seeker_positions, self.initial_circle_radius, self.x_size, self.y_size)
        
        if seeker_collision:
            # Check Collisions -> Passed
            self.initial_circle_radius = 10
            self.player_pos, self.seeker_positions, self.coin_positions = self.game_map.resetGame()

        # Check if player reach end
        if self.grid[self.player_pos[1]][self.player_pos[0]] == 'E':
            # Check -> Passed
            self.game_won = True

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                # Users end game
                self.running = False

            elif event.type == pygame.KEYDOWN:
                # Update player position
                new_pos: List[int] = self.player_pos[:]
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

                    # Update circle radius
                    self.initial_circle_radius += 4

                if event.key == pygame.K_ESCAPE:
                    self.main_menu()

                elif event.key == pygame.K_r:
                    self.map_generator.generateMap()
                    self.grid = self.map_generator.map
                    self.game_map.grid = self.grid

                    # Get new map dimensions
                    self.rows, self.cols = len(self.grid), len(self.grid[0])

                    # Calculate tile size
                    self.x_size = self.screen_width / self.cols
                    self.y_size = self.screen_height / self.rows
                    
                    # Update the screen to display new map
                    self.display.updateScreenSize(self.cols, self.rows)
                    self.player_pos, self.seeker_positions, self.coin_positions = self.game_map.resetGame()
                    self.game_won = False

        if not self.game_won:
            self.initial_circle_radius = max(self.default_radius, self.initial_circle_radius - 1)

if __name__ == '__main__':
    game = SeekerGame()
    game.run()
