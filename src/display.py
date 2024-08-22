import pygame
import json
from typing import Dict

class Display:
    def __init__(
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

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption('Sneak')
        self.font = pygame.font.Font(None, 74)
        self.theme = theme

        # Load images
        self.coin_image = pygame.image.load(r'src\coin.jpg')
        self.seeker_image = pygame.image.load(r'src\seeker.jpg')
        self.clock_image = pygame.image.load(r'src\clock.jpg')


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
        Draw the taskbar with current game statistics and images.

        Args:
            coins (int): The number of coins collected.
            collisions (int): The number of seeker collisions.
            stopwatch (str): The elapsed time formatted as a string.
        """

        # Resize images
        self.image_size = 40
        self.coin_image = pygame.transform.scale(self.coin_image, (self.image_size, self.image_size))
        self.seeker_image = pygame.transform.scale(self.seeker_image, (self.image_size, self.image_size))
        self.clock_image = pygame.transform.scale(self.clock_image, (self.image_size, self.image_size))

        # Draw the taskbar background
        taskbar_rect = pygame.Rect(0, 0, self.screen_width, self.taskbar_height)
        pygame.draw.rect(self.screen, self.taskbar_color, taskbar_rect)

        # Font for taskbar text
        font = pygame.font.SysFont(None, self.taskbar_font_size)
        text_color = (255, 255, 255)

        # Render the number of coins with image
        coins_text = font.render(f'Coins: {coins}', True, text_color)
        self.screen.blit(self.coin_image, (10, 10))
        self.screen.blit(coins_text, (10 + self.image_size + 10, 10))  # Text position

        # Render the stopwatch with image
        stopwatch_text = font.render(f'Time: {stopwatch}', True, text_color)
        stopwatch_width = stopwatch_text.get_width()
        self.screen.blit(self.clock_image, (self.screen_width // 2 - stopwatch_width // 2 - self.image_size - 10, 10))  # Image position
        self.screen.blit(stopwatch_text, (self.screen_width // 2 - stopwatch_width // 2, 10))  # Text position

        # Render the number of seeker collisions with image
        collisions_text = font.render(f'Collisions: {collisions}', True, text_color)
        self.screen.blit(self.seeker_image, (self.screen_width - self.image_size - 10, 10))  # Image position
        self.screen.blit(collisions_text, (self.screen_width - collisions_text.get_width() - 10 - self.image_size - 10, 10))  # Text position

    def showWinScreen(
        self,
        cols: int,
        rows: int,
        seeker_collisions: int,
        time_taken: str,
        coins_collected: int
    ) -> None:
        """
        Display the win screen with the appropriate messages and images.

        Args:
            cols (int): Number of columns in the grid.
            rows (int): Number of rows in the grid.
            seeker_collisions (int): Number of seeker collisions that occurred.
            time_taken (str): The time taken to complete the level.
            coins_collected (int): The number of coins collected by the player.
        """
        # Resize images
        self.image_size = 74
        self.coin_image = pygame.transform.scale(self.coin_image, (self.image_size, self.image_size))
        self.seeker_image = pygame.transform.scale(self.seeker_image, (self.image_size, self.image_size))
        self.clock_image = pygame.transform.scale(self.clock_image, (self.image_size, self.image_size))

        # Win Messages
        win_text = "YOU WON"
        collisions_text = f"Seeker Collisions: {seeker_collisions}"
        time_text = f"Time Taken: {time_taken}"
        coins_text = f"Coins Collected: {coins_collected}"
        exit_text = "Press SPACE to continue or ESC to exit"

        # Render win messages
        win_surface = self.font.render(win_text, True, self.theme['START_COLOR'])
        collisions_surface = self.font.render(collisions_text, True, self.theme['SEEKER_COLOR'])
        time_surface = self.font.render(time_text, True, self.theme['END_COLOR'])
        coins_surface = self.font.render(coins_text, True, self.theme['COIN_COLOR'])
        exit_surface = self.font.render(exit_text, True, self.theme['START_COLOR'])

        # Calculate positions
        center_x_position = self.screen_width // 2

        top_padding = int(self.screen_height * 0.1)
        vertical_spacing = int(self.screen_height * 0.05)

        # Display win message
        self.screen.blit(win_surface, (center_x_position - win_surface.get_width() // 2, top_padding))

        # Display exit message
        self.screen.blit(exit_surface, (center_x_position - exit_surface.get_width() // 2,
                                        top_padding + win_surface.get_height() + vertical_spacing))

        # Calculate positions
        left_offset = int(center_x_position * 0.6)
        stats_start_y_position = top_padding + win_surface.get_height() + exit_surface.get_height() + vertical_spacing * 4

        # Spacing between the stats
        stats_spacing = int(self.screen_height * 0.1)

        # Display images and text
        # Display seeker image and collisions text
        self.screen.blit(self.seeker_image, (left_offset - self.image_size - 10, stats_start_y_position))
        self.screen.blit(collisions_surface, (left_offset, stats_start_y_position))

        # Display clock image and time text
        self.screen.blit(self.clock_image, (left_offset - self.image_size - 10,
                                            stats_start_y_position + stats_spacing))
        self.screen.blit(time_surface, (left_offset, stats_start_y_position + stats_spacing))

        # Display coin image and coins text
        self.screen.blit(self.coin_image, (left_offset - self.image_size - 10,
                                           stats_start_y_position + 2 * stats_spacing))
        self.screen.blit(coins_surface, (left_offset, stats_start_y_position + 2 * stats_spacing))