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

import logging
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def add_to_path():
    generator_path = Path('src/generator/Model - 2').resolve()
    sys.path.append(str(generator_path))

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

        logging.debug("pygame initialised")
        
        # Read theme
        theme_path = Path('src') / 'theme.json'
        self.theme: dict = read_theme(theme_path)
        logging.info("Theme initialised")
        
        # Get screen dimensions
        self.screen_width: int
        self.screen_height: int
        self.screen_width, self.screen_height = get_screen_dimensions()
        logging.info(f"Screen Dimensions fetched {self.screen_height} x {self.screen_width}")
        
        # Initialize Map Generatore
        self.map_generator = MapGenerator()
        self.map_generator.generateMap()
        logging.debug("Map Generated")

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
        logging.debug("Screen Initialised")
        
        # Set up player attributes
        self.player_pos: List[int]
        self.seeker_positions: List[List[int]]
        self.player_pos, self.seeker_positions, self.coin_positions = self.game_map.resetGame()
        self.clock: pygame.time.Clock = pygame.time.Clock()
        logging.info("Entities initialised")

        # Initialize game management variable
        self.running: bool = True
        self.game_won: bool = False
        self.all_levels_cleared: bool = False
        
        # Initial circle radius
        self.default_radius = 10
        self.initial_circle_radius: int = 10
        self.n = 0

        # Coin Tracker
        self.coins = 0

    def take_screenshot(self, filename: str) -> None:
        """
        Take a screenshot of the current screen and save it to a file.
        """
        pygame.display.flip()  # Ensure the screen is up-to-date
        pygame.image.save(self.display.screen, filename)
        logging.info(f"Screenshot saved as {filename}")
    
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
                        logging.debug("Exiting Game....")
                        pygame.quit()
                        sys.exit()

                    elif event.key == pygame.K_r:
                        # Reset coins
                        self.coins = 0

                        # Generate new Map
                        self.map_generator.generateMap()
                        self.grid = self.map_generator.map
                        self.game_map.coins_collected, self.game_map.seekers_collisions, self.start_time = 0, 0, pygame.time.get_ticks()
                        logging.info("New Map Generated")

                        self.game_map.grid = self.grid
                        # Get new map dimensions
                        self.rows, self.cols = len(self.grid), len(self.grid[0])
                        # Calculate tile size
                        self.x_size = self.screen_width / self.cols
                        self.y_size = self.screen_height / self.rows

                        # Update the screen to display new map
                        self.display.updateScreenSize(self.cols, self.rows)
                        self.player_pos, self.seeker_positions, self.coin_positions = self.game_map.resetGame()


                        logging.info("New Map Set")
                        self.game_won = False

                    elif event.key == pygame.K_1:
                        self.take_screenshot(f"screenshot{self.n}.png")
                        self.n += 1
                        logging.info("Screenshot taken")

                elif event.type == pygame.QUIT:
                    logging.info("Exiting Game....")
                    pygame.quit()
                    sys.exit()

    def run(self) -> None:
        self.main_menu()
        logging.debug("Main Menu Initialised")

        self.start_time = pygame.time.get_ticks()
        while self.running:
            self.display.screen.fill(self.theme['BACKGROUND_COLOR'])

            # Calculate elapsed time
            if not self.game_won:
                elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
                formatted_time = f"{elapsed_time // 60:02}:{elapsed_time % 60:02}"

            # Check Game winning conditions
            if self.game_won:
                self.handle_win()
                logging.info("Winning Conditions Checked")

            else:
                self.handle_gameplay()
                logging.info("Game Mechanics Handled")

            # Draw taskbar with updated info
            if not self.game_won:
                self.display.drawTaskbar(self.game_map.coins_collected, self.game_map.seekers_collisions, formatted_time)

            pygame.display.flip()
            self.clock.tick(10)

        pygame.quit()
        sys.exit()


    def handle_win(self) -> None:
        """
        Handle the win state of the game.
        """

        # Calculate time taken in minutes and seconds
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        formatted_time = f"{elapsed_time // 60:02}:{elapsed_time % 60:02}"

        # Display the win screen with seeker collisions, time, and coins collected
        self.display.showWinScreen(
            self.cols, 
            self.rows, 
            self.game_map.seekers_collisions, 
            self.time_taken, 
            self.game_map.coins_collected
        )

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                # If user continues to the next stage
                if event.key == pygame.K_SPACE:
                    # Reset Coins
                    self.coins = 0

                    # Read next stage map
                    self.map_generator.generateMap()
                    self.grid = self.map_generator.map
                    self.game_map.grid = self.grid
                    self.game_map.coins_collected, self.game_map.seekers_collisions, self.start_time = 0, 0, pygame.time.get_ticks()
                    logging.debug("New Map Generated")

                    # Get new map dimensions
                    self.rows, self.cols = len(self.grid), len(self.grid[0])

                    # Calculate tile size
                    self.x_size = self.screen_width / self.cols
                    self.y_size = self.screen_height / self.rows

                    # Update the screen to display new map
                    self.display.updateScreenSize(self.cols, self.rows)
                    self.player_pos, self.seeker_positions, self.coin_positions = self.game_map.resetGame()
                    self.game_won = False
                        
                    logging.debug("New Map Set")
                    self.initial_circle_radius = self.default_radius

                elif event.key == pygame.K_ESCAPE:
                    # User wants to end game
                    self.running = False
                    self.main_menu()
                    logging.info("Main Menu Set")

                elif event.key == pygame.K_r:
                    # Reset Coins
                    self.coins = 0

                    # Generate New Map
                    self.map_generator.generateMap()
                    self.grid = self.map_generator.map
                    self.game_map.grid = self.grid
                    self.game_map.coins_collected, self.game_map.seekers_collisions, self.start_time = 0, 0, pygame.time.get_ticks()
                    logging.info("New Map Generated")
                    # Get new map dimensions
                    self.rows, self.cols = len(self.grid), len(self.grid[0])

                    # Calculate tile size
                    self.x_size = self.screen_width / self.cols
                    self.y_size = self.screen_height / self.rows

                    # Update the screen to display new map
                    self.display.updateScreenSize(self.cols, self.rows)
                    self.player_pos, self.seeker_positions, self.coin_positions = self.game_map.resetGame()
                    self.game_won = False
                             
                    logging.info("New Map Set")
            
                elif event.key == pygame.K_1:
                        self.take_screenshot(f"screenshot{self.n}.png")
                        self.n += 1
                        logging.info("Screenshot taken")

            elif event.type == pygame.QUIT:
                # User wants to end game
                self.running = False
                logging.debug("Exiting Game...")

    def handle_gameplay(self) -> None:
        """
        Handle the gameplay mechanics, including 
        drawing the map, updating seeker movements, and handling player input.
        """

        # Update current game with new positions
        self.game_map.drawGrid(self.display.screen, self.player_pos, self.seeker_positions, self.coin_positions, self.initial_circle_radius)
        self.game_map.updateSeekers()
        logging.debug("Seeker Movements Handled")

        # Check Collisions
        seeker_collision, coin_collision = self.game_map.checkCollisions(self.player_pos, self.seeker_positions, self.initial_circle_radius, self.x_size, self.y_size)
        logging.debug("Collisions Handled")

        if seeker_collision:
            # Check Collisions -> Passed
            self.initial_circle_radius = 10
            self.player_pos, self.seeker_positions, self.coin_positions = self.game_map.resetGame()
            logging.info("Seekers Position Updated")

        if coin_collision:
            self.coins += 1

        # Check if player reach end
        if self.grid[self.player_pos[1]][self.player_pos[0]] == 'E':
            # Check -> Passed
            self.game_won = True
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            self.time_taken = f"{elapsed_time // 60:02}:{elapsed_time % 60:02}"
            logging.debug("Game Won")

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                # Users end game
                self.running = False
                logging.debug("Exiting Game...w")

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
                logging.debug("Player Movements Handled")

                if event.key == pygame.K_ESCAPE:
                    self.main_menu()

                elif event.key == pygame.K_r:
                    # Reset coins
                    self.coins += 1

                    # Genrate New Map
                    self.map_generator.generateMap()
                    self.grid = self.map_generator.map
                    self.game_map.grid = self.grid
                    self.game_map.coins_collected, self.game_map.seekers_collisions, self.start_time = 0, 0, pygame.time.get_ticks()
                    logging.debug("New Map Generated")

                    # Get new map dimensions
                    self.rows, self.cols = len(self.grid), len(self.grid[0])

                    # Calculate tile size
                    self.x_size = self.screen_width / self.cols
                    self.y_size = self.screen_height / self.rows
                    
                    # Update the screen to display new map
                    self.display.updateScreenSize(self.cols, self.rows)
                    self.player_pos, self.seeker_positions, self.coin_positions = self.game_map.resetGame()
                    self.game_won = False

                    logging.debug("New Map Set")

                elif event.key == pygame.K_1:
                    self.take_screenshot(f"screenshot{self.n}.png")
                    self.n += 1
                    logging.info("Screenshot taken")

        if not self.game_won:
            self.initial_circle_radius = max(self.default_radius, self.initial_circle_radius - 1)

if __name__ == '__main__':
    logging.info("Starting Game...")
    game = SeekerGame()
    game.run()
