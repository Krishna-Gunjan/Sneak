import pygame

class MapDrawer:

    def __init__(self,
                 grid: list[list[str]],
                 tile_size : tuple[float],
                 circle_radius: int,
                 colors
                ):
        
        self.grid = grid
        self.x_size = tile_size[0]
        self.y_size = tile_size[1]
        self.circle_radius = circle_radius
        self.player_pos, self.seeker_positions = self.resetGame()
        self.colors = colors

    def drawMap(self, screen):
        
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * self.x_size, y * self.y_size, self.x_size, self.y_size)
                if cell == '#':
                    pygame.draw.rect(screen, self.colors["WALL_COLOR"], rect)
                elif cell == 'S':
                    pygame.draw.rect(screen, self.colors["START_COLOR"], rect)
                elif cell == 'E':
                    pygame.draw.rect(screen, self.colors["END_COLOR"], rect)

        player_rect = pygame.Rect(self.player_pos[0] * self.x_size, self.player_pos[1] * self.y_size, self.x_size, self.y_size)
        pygame.draw.rect(screen, self.colors["START_COLOR"], player_rect)

        for pos in self.seeker_positions:
            seeker_rect = pygame.Rect(pos[0] * self.x_size, pos[1] * self.y_size, self.x_size, self.y_size)
            pygame.draw.rect(screen, self.colors["SEEKER_COLOR"], seeker_rect)

        circle_center = (self.player_pos[0] * self.x_size + self.x_size // 2, self.player_pos[1] * self.y_size + self.y_size // 2)
        pygame.draw.circle(screen, self.colors["CIRCLE_COLOR"], circle_center, self.circle_radius, 3)

    def resetGame(self):
        player_pos = None
        seeker_positions = []
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 'S':
                    player_pos = [x, y]
                elif cell == '$':
                    seeker_positions.append([x, y, 1]) 
        return player_pos, seeker_positions