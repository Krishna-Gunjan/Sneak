import ctypes
import pygame

class Background():
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.screen_width = self.user32.GetSystemMetrics(0)
        self.screen_height = self.user32.GetSystemMetrics(1)
        self.background_color = (0, 0, 0)

    def setBackground(self):
        flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        screen = pygame.display.set_mode((self.screen_width, self.screen_height), flags)
        pygame.display.set_caption("Sneak")
        return screen

    def setBoundary(self, screen):
        boundary = [
            (0, 0, self.screen_width // 100, self.screen_height), # Left Wall
            (self.screen_width - self.screen_width // 100, 0, self.screen_width // 100, self.screen_height), # Right Wall
            (0, 0, self.screen_width, self.screen_height // 100), # Top Wall
            (0, self.screen_height - self.screen_height // 100, self.screen_width, self.screen_height // 100) # Bottom Wall
            ]

        for barrier in boundary:
            pygame.draw.rect(screen, (102, 113, 126), barrier)

        pygame.display.flip()
