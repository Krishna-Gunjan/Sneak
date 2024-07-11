import ctypes

def get_screen_dimensions():
    
    # Refer to the comment in src/read_theme.py

    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    
    return screen_width, screen_height
