import pygame
import ctypes
from screen_dimensions import ScreenDimensions
from map_reader import MapReader

class Dispay():

    def __init__(self) -> None:
        self.dimensions = ScreenDimensions().getDimensions()
        self.map_dimensions = MapReader().mapDimensions()
        self.x_size = self.dimensions[0] / self.map_dimensions[0]
        self.y_size = self.dimensions[1] / self.map_dimensions[1]

    def setScreen(self):
        screen = pygame.display.set_mode((self.dimensions[0], self.dimensions[1]), pygame.FULLSCREEN)
