import pygame
from cell import Cell


class Nonogram:
    def __init__(self, width, height, w=20):
        self.cell_dict = {}
        self.width = width
        self.height = height
        self.w = w
        self.cell_count = 0
        self.rows = []
        self.columns = []
        self.rowzies = []
        self.cowzies = []
        self.row_numbers = []
        self.column_numbers = []

    def add_cell(self, item):
        self.cell_dict[item.id] = item
        self.cell_count = len(self.cell_dict)

    def update_screen(self, screen):
        for cell in self.cell_dict.values():
            cell.update_cell(screen, (255, 255, 255))

    def get_cell(self, id):
        return self.cell_dict[id]

    def build_numbers(self, screen):
        for i in range(self.height//self.w):
            row = [cell for cell in self.cell_dict.values() if cell.id[1] == i]
            rowzy = [0 for cell in self.cell_dict.values() if cell.id[1] == i]
            self.rows.append(row)
            self.rowzies.append(rowzy)
        for i in range(self.width//self.w):
            column = [cell for cell in self.cell_dict.values() if cell.id[0] == i]
            cowzy = [0 for cell in self.cell_dict.values() if cell.id[0] == i]
            self.columns.append(column)
            self.cowzies.append(cowzy)
        for row in self.rows:
            count = 0
            enabled = 0
            row_array = []
            full = 0
            for cell in row:
                if cell.color == (0, 0, 0):
                    count += 1
                    enabled = 1
                    full = 1
                else:
                    if enabled:
                        row_array.append(count)
                        enabled = 0
                        count = 0
            if not full or count is not 0:
                row_array.append(count)
            self.row_numbers.append(row_array)
        for column in self.columns:
            count = 0
            enabled = 0
            column_array = []
            full = 0
            for cell in column:
                if cell.color == (0, 0, 0):
                    count += 1
                    enabled = 1
                    full = 1
                else:
                    if enabled:
                        column_array.append(count)
                        enabled = 0
                        count = 0
            if not full or count is not 0:
                column_array.append(count)
            self.column_numbers.append(column_array)
        for i in range(len(self.row_numbers)):
            for j in range(len(self.row_numbers[i])):
                pygame.draw.rect(screen, (100, 100, 100), (self.width + self.w + j*self.w, self.w + i*self.w,
                                                           self.w - 1, self.w - 1))
                font = pygame.font.Font('freesansbold.ttf', self.w // 2)
                text = font.render(str(self.row_numbers[i][j]), True, (255, 255, 255), (100, 100, 100))
                textRect = text.get_rect()
                textRect.center = (self.width + self.w + j*self.w + self.w // 2, self.w + i*self.w + self.w // 2)
                screen.blit(text, textRect)
        for i in range(len(self.column_numbers)):
            for j in range(len(self.column_numbers[i])):
                pygame.draw.rect(screen, (100, 100, 100), (self.w + i*self.w, self.height + self.w + j*self.w,
                                                           self.w - 1, self.w - 1))
                font = pygame.font.Font('freesansbold.ttf', self.w // 2)
                text = font.render(str(self.column_numbers[i][j]), True, (255, 255, 255), (100, 100, 100))
                textRect = text.get_rect()
                textRect.center = (self.w + i*self.w + self.w // 2, self.height + self.w + j*self.w + self.w // 2)
                screen.blit(text, textRect)

    def check_cell(self, pos):
        x = pos[0]
        y = pos[1]
        if x < self.width + self.w and y < self.height + self.w:
            cell_x = (x - self.w) // self.w
            cell_y = (y - self.w) // self.w
            cell = self.cell_dict[(cell_x, cell_y)]
            return cell
        else:
            return False

    def auto_solve(self, screen, clock):
        for i in range(len(self.rows)):
            first_value = self.row_numbers[i][0]
            if first_value == 0:
                for k in range(len(self.rows[i])):
                    clock.tick(20)
                    self.cell_dict[(k, i)].cross(screen)
            start = first_value - 1
            end = len(self.rows[i]) - first_value
            if start < end:
                continue
            else:
                for k in range(end, start + 1):
                    clock.tick(20)
                    self.cell_dict[(k, i)].update_cell(screen, (0, 0, 0))
            last_value = self.row_numbers[i][-1]
            start = last_value - 1
            end = len(self.rows[i]) - last_value
            if start < end:
                continue
            else:
                for k in range(end, start + 1):
                    clock.tick(20)
                    self.cell_dict[(k, i)].update_cell(screen, (0, 0, 0))
        for i in range(len(self.columns)):
            first_value = self.column_numbers[i][0]
            if first_value == 0:
                for k in range(len(self.columns[i])):
                    clock.tick(20)
                    self.cell_dict[(i, k)].cross(screen)
            start = first_value - 1
            end = len(self.columns[i]) - first_value
            if start < end:
                continue
            else:
                for k in range(end, start + 1):
                    clock.tick(20)
                    self.cell_dict[(i, k)].update_cell(screen, (0, 0, 0))
            last_value = self.column_numbers[i][-1]
            start = last_value - 1
            end = len(self.columns[i]) - last_value
            if start < end:
                continue
            else:
                for k in range(end, start + 1):
                    clock.tick(20)
                    self.cell_dict[(i, k)].update_cell(screen, (0, 0, 0))








