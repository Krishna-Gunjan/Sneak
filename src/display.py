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
        self.x_size = x_size
        self.y_size = y_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption('Seeker Game')
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
        
        self.screen = pygame.display.set_mode((cols * int(self.x_size), rows * int(self.y_size)), pygame.FULLSCREEN)

    def showWinScreen (
            self, 
            cols: int, 
            rows: int, 
            all_levels_cleared: bool
        ) -> None:
        
        """
        Display the win screen with the appropriate messages.
        
        Args:
            cols (int): Number of columns in the grid.
            rows (int): Number of rows in the grid.
            all_levels_cleared (bool): Flag indicating if all levels have been cleared.
        """
        
        # Win Messages
        win_text = "YOU WON"
        next_level_text = "Press SPACE to go to the next level"
        exit_text = "Press ESC to exit"

        # Rendored win messages
        win_surface = self.font.render(win_text, True, self.theme['TEXT_COLOR'])
        next_level_surface = self.font.render(next_level_text, True, self.theme['TEXT_COLOR'])
        exit_surface = self.font.render(exit_text, True, self.theme['TEXT_COLOR'])

        # Display win messages
        self.screen.blit(win_surface, ((cols * int(self.x_size)) // 2 - win_surface.get_width() // 2, 
                                       (rows * int(self.y_size)) // 2 - win_surface.get_height() // 2 - 40))

        # Check if game is not complete
        if not all_levels_cleared:

            # Check -> Passed
            # Display next level message
            self.screen.blit(next_level_surface, ((cols * int(self.x_size)) // 2 - next_level_surface.get_width() // 2, 
                                                  (rows * int(self.y_size)) // 2 - next_level_surface.get_height() // 2))

        # Dislpay exit message
        self.screen.blit(exit_surface, ((cols * int(self.x_size)) // 2 - exit_surface.get_width() // 2, 
                                        (rows * int(self.y_size)) // 2 - exit_surface.get_height() // 2 + 40))
