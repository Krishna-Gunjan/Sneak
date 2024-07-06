import pygame
from background import Background

bg = Background()
stage = bg.setBackground()
bg.setBoundary(screen=stage)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
