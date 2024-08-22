import pygame
import json
from typing import Dict

class Display:
    def __init__ (
            self,
            screen_width: int,
            screen_height: int,
            x_size: float,
            y_size: float,
            theme: Dict[str, str]
        ) -> None:

        """
        Initialize the Display class by setting up 
        the screen dimensions, tile sizes, and theme.
        
        Args:
            screen_width (int): The width of the screen.
            screen_height (int): The height of the screen.
            x_size (float): The width of each tile.
            y_size (float): The height of each tile.
            theme (dict): The theme dictionary containing colors and other UI elements.
        """

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.taskbar_height = 50
        self.taskbar_color = (0, 0, 0)
        self.taskbar_font_size = 30

        self.x_size = x_size
        self.y_size = y_size

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption('Sneak')
        self.font = pygame.font.Font(None, 74)
        self.theme = theme


    def updateScreenSize (
            self,
            cols: int,
            rows: int
        ) -> None:
        
        """
        Update the screen size based 
        on the number of columns and rows.
        
        Args:
            cols (int): Number of columns in the grid.
            rows (int): Number of rows in the grid.
        """
        
        self.screen = pygame.display.set_mode((cols * int(self.x_size), rows * int(self.y_size) + self.taskbar_height), pygame.FULLSCREEN)

    def drawTaskbar(self, coins: int, collisions: int, stopwatch: str) -> None:
        """
        Draw the taskbar with current game statistics.

        Args:
            coins (int): The number of coins collected.
            collisions (int): The number of seeker collisions.
            stopwatch (str): The elapsed time formatted as a string.
        """
        # Draw the taskbar background
        taskbar_rect = pygame.Rect(0, 0, self.screen_width, self.taskbar_height)
        pygame.draw.rect(self.screen, self.taskbar_color, taskbar_rect)

        # Font for taskbar text
        font = pygame.font.SysFont(None, self.taskbar_font_size)
        text_color = (255, 255, 255)  # White

        # Render the number of coins
        coins_text = font.render(f'Coins: {coins}', True, text_color)
        self.screen.blit(coins_text, (10, 10))

        # Render the stopwatch
        stopwatch_text = font.render(f'Time: {stopwatch}', True, text_color)
        stopwatch_width = stopwatch_text.get_width()
        self.screen.blit(stopwatch_text, (self.screen_width // 2 - stopwatch_width // 2, 10))

        # Render the number of seeker collisions
        collisions_text = font.render(f'Collisions: {collisions}', True, text_color)
        self.screen.blit(collisions_text, (self.screen_width - collisions_text.get_width() - 10, 10))

    def showWinScreen(
        self, 
        cols: int, 
        rows: int, 
        seeker_collisions: int, 
        time_taken: str, 
        coins_collected: int, 
        all_levels_cleared: bool = False
    ) -> None:
    
        """
        Display the win screen with the appropriate messages.
        
        Args:
            cols (int): Number of columns in the grid.
            rows (int): Number of rows in the grid.
            seeker_collisions (int): Number of seeker collisions that occurred.
            time_taken (str): The time taken to complete the level.
            coins_collected (int): The number of coins collected by the player.
            all_levels_cleared (bool): Flag indicating if all levels have been cleared.
        """
    
        # Win Messages
        win_text = "YOU WON"
        collisions_text = f"Seeker Collisions: {seeker_collisions}"
        time_text = f"Time Taken: {time_taken}"
        coins_text = f"Coins Collected: {coins_collected}"
        next_level_text = "Press SPACE to go to the next level"
        exit_text = "Press ESC to exit"
    
        # Render win messages
        win_surface = self.font.render(win_text, True, self.theme['TEXT_COLOR'])
        collisions_surface = self.font.render(collisions_text, True, self.theme['TEXT_COLOR'])
        time_surface = self.font.render(time_text, True, self.theme['TEXT_COLOR'])
        coins_surface = self.font.render(coins_text, True, self.theme['TEXT_COLOR'])
        next_level_surface = self.font.render(next_level_text, True, self.theme['TEXT_COLOR'])
        exit_surface = self.font.render(exit_text, True, self.theme['TEXT_COLOR'])
    
        # Display win messages
        self.screen.blit(win_surface, ((cols * int(self.x_size)) // 2 - win_surface.get_width() // 2, 
                                       (rows * int(self.y_size)) // 2 - win_surface.get_height() // 2 - 100))
        
        # Display seeker collisions
        self.screen.blit(collisions_surface, ((cols * int(self.x_size)) // 2 - collisions_surface.get_width() // 2, 
                                              (rows * int(self.y_size)) // 2 - collisions_surface.get_height() // 2 - 60))
        
        # Display time taken
        self.screen.blit(time_surface, ((cols * int(self.x_size)) // 2 - time_surface.get_width() // 2, 
                                        (rows * int(self.y_size)) // 2 - time_surface.get_height() // 2 - 20))
    
        # Display coins collected
        self.screen.blit(coins_surface, ((cols * int(self.x_size)) // 2 - coins_surface.get_width() // 2, 
                                         (rows * int(self.y_size)) // 2 - coins_surface.get_height() // 2 + 20))
    
        # Check if game is not complete
        if not all_levels_cleared:
            # Display next level message
            self.screen.blit(next_level_surface, ((cols * int(self.x_size)) // 2 - next_level_surface.get_width() // 2, 
                                                  (rows * int(self.y_size)) // 2 - next_level_surface.get_height() // 2 + 60))
    
        # Display exit message
        self.screen.blit(exit_surface, ((cols * int(self.x_size)) // 2 - exit_surface.get_width() // 2, 
                                        (rows * int(self.y_size)) // 2 - exit_surface.get_height() // 2 + 100))
    