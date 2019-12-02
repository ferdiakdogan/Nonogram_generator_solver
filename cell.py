import pygame


class Cell:
    def __init__(self, id, x, y, color, width=10):
        self.id = id
        self.x = x
        self.y = y
        self.color = color
        self.width = width

    def update_cell(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width - 1, self.width - 1))
        pygame.display.update()

