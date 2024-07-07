import ctypes

class ScreenDimensions():

    def __init__(self) -> None:
        self.user32 = ctypes.windll.user32

    def getDimensions(self):

        width = self.user32.GetSystemMetrics(0)
        height = self.user32.GetSystemMetrics(1)

        return (width, height)
