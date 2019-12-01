import pygame
from cell import Cell


class Nonogram:
    def __init__(self, width, height, w=20):
        self.cell_dict = {}
        self.width = width
        self.height = height
        self.w = w
        self.cell_count = 0

    def add_cells(self, item):
        self.cell_dict[item.id] = item