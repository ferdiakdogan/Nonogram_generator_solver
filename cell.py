import pygame


class Cell:
    def __init__(self, id, x, y, color, width=10):
        self.id = id
        self.x = x
        self.y = y
        self.color = color
        self.width = width

    def update_cell(self, screen, color):
        pygame.draw.rect(screen, color, (self.x + 2, self.y + 2, self.width - 4, self.width - 4))
        pygame.display.update()

    def cross(self, screen):
        pygame.draw.line(screen, (0, 0, 0), [self.x + 3, self.y + 3], [self.x + self.width - 3, self.y + self.width - 3], 3)
        pygame.draw.line(screen, (0, 0, 0), [self.x + 3, self.y + self.width - 3], [self.x + self.width - 3, self.y + 3], 3)

