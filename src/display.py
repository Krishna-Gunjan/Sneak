import pygame
import json

class Display:
    def __init__ (
            self,
            screen_width,
            screen_height,
            x_size,
            y_size,
            theme
        ):
        
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
            cols,
            rows
        ):
        
        self.screen = pygame.display.set_mode((cols * int(self.x_size), rows * int(self.y_size)), pygame.FULLSCREEN)

    def showWinScreen (
            self,
            cols,
            rows,
            all_levels_cleared
        ):

        win_text = "YOU WON"
        next_level_text = "Press SPACE to go to the next level"
        exit_text = "Press ESC to exit"
        
        win_surface = self.font.render(win_text, True, self.theme['TEXT_COLOR'])
        next_level_surface = self.font.render(next_level_text, True, self.theme['TEXT_COLOR'])
        exit_surface = self.font.render(exit_text, True, self.theme['TEXT_COLOR'])

        self.screen.blit(win_surface, ((cols * int(self.x_size)) // 2 - win_surface.get_width() // 2, (rows * int(self.y_size)) // 2 - win_surface.get_height() // 2 - 40))

        if not all_levels_cleared:
            self.screen.blit(next_level_surface, ((cols * int(self.x_size)) // 2 - next_level_surface.get_width() // 2, (rows * int(self.y_size)) // 2 - next_level_surface.get_height() // 2))

        self.screen.blit(exit_surface, ((cols * int(self.x_size)) // 2 - exit_surface.get_width() // 2, (rows * int(self.y_size)) // 2 - exit_surface.get_height() // 2 + 40))
