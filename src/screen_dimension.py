import sys
import pygame
import ctypes

def get_screen_dimensions():
    """
    Get the screen dimensions in a cross-platform way.
    Uses ctypes for Windows, and pygame for macOS and Linux.
    """
    if sys.platform == 'win32':
        # Windows
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        
    else:
        # macOS and Linux
        pygame.init()
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
    
    return screen_width, screen_height
