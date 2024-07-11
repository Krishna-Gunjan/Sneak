import pygame
from typing import List, Tuple, Any, Dict

class GameMap:
    
    def __init__ (
            self, 
            grid: List[List[str]], 
            x_size: float, 
            y_size: float, 
            theme: Dict[str, Any]
        ) -> None:
        
        """
        Initialize the GameMap class with the grid, tile sizes, and theme.
        
        Args:
            grid (List[List[str]]): The game grid.
            x_size (float): The width of each tile.
            y_size (float): The height of each tile.
            theme (dict): The theme dictionary containing colors and other UI elements.
        """
        self.grid = grid
        self.x_size = x_size
        self.y_size = y_size
        self.theme = theme
        self.seeker_positions: List[List[int]] = []

    def resetGame (
            self
        ) -> Tuple[List[int], List[List[int]]]:
        
        """
        Reset the game by finding the player's start position and seekers' positions.
        
        Returns:
            Tuple: Player's starting position and seekers' positions.
        """
        
        player_pos = None
        self.seeker_positions = []

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 'S':
                    player_pos = [x, y]
                elif cell == '$':
                    self.seeker_positions.append([x, y, 1])
        
        return player_pos, self.seeker_positions

    def drawGrid (
            self, 
            screen: pygame.Surface, 
            player_pos: List[int], 
            seeker_positions: List[List[int]], 
            circle_radius: int
        ) -> None:
        
        """
        Draw the grid, player, seekers, and the player's circle on the screen.
        
        Args:
            screen (pygame.Surface): The screen surface to draw on.
            player_pos (List[int]): The player's position.
            seeker_positions (List[List[int]]): The seekers' positions.
            circle_radius (int): The radius of the player's circle.
        """
        
        rows = len(self.grid)
        cols = len(self.grid[0])
        
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * self.x_size, y * self.y_size, self.x_size, self.y_size)
                if cell == '#':
                    pygame.draw.rect(screen, self.theme['WALL_COLOR'], rect)
                elif cell == 'S':
                    pygame.draw.rect(screen, self.theme['START_COLOR'], rect)
                elif cell == 'E':
                    pygame.draw.rect(screen, self.theme['END_COLOR'], rect)

        player_rect = pygame.Rect(player_pos[0] * self.x_size, player_pos[1] * self.y_size, self.x_size, self.y_size)
        pygame.draw.rect(screen, self.theme['START_COLOR'], player_rect)

        for pos in seeker_positions:
            seeker_rect = pygame.Rect(pos[0] * self.x_size, pos[1] * self.y_size, self.x_size, self.y_size)
            pygame.draw.rect(screen, self.theme['SEEKER_COLOR'], seeker_rect)

        circle_center = (player_pos[0] * self.x_size + self.x_size // 2, player_pos[1] * self.y_size + self.y_size // 2)
        pygame.draw.circle(screen, self.theme['CIRCLE_COLOR'], circle_center, circle_radius, 3)

    def updateSeekers (
            self
        ) -> None:
        
        """
        Update the positions of the seekers.
        """
        
        for seeker in self.seeker_positions:
        
            x, y, direction = seeker
            new_x = x + direction
            
            if new_x < 0 or new_x >= len(self.grid[0]) or self.grid[y][new_x] == '#':
                direction *= -1
            
            else:
                seeker[0] = new_x
            seeker[2] = direction

    def checkCollisions (
            self,
            player_pos: List[int], 
            seeker_positions: List[List[int]], 
            circle_radius: int, 
            x_size: float, 
            y_size: float
        ) -> bool:
        
        """
        Check for collisions between the player and the seekers.
        
        Args:
            player_pos (List[int]): The player's position.
            seeker_positions (List[List[int]]): The seekers' positions.
            circle_radius (int): The radius of the player's circle.
            x_size (float): The width of each tile.
            y_size (float): The height of each tile.
        
        Returns:
            bool: True if a collision is detected, False otherwise.
        """
        
        for seeker in seeker_positions:
            seeker_center = (seeker[0] * int(x_size) + int(x_size) // 2, seeker[1] * int(y_size) + int(y_size) // 2)
            circle_center = (player_pos[0] * int(x_size) + int(x_size) // 2, player_pos[1] * int(y_size) + int(y_size) // 2)
            distance = ((seeker_center[0] - circle_center[0]) ** 2 + (seeker_center[1] - circle_center[1]) ** 2) ** 0.5

            if distance < circle_radius + int(x_size) // 2:
                return True
            
        return False
