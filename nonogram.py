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

    def solve_nonogram(self, screen):
        for m in range(len(self.rowzies)):
            # INITIAL RUN: Range Estimating
            rls = 0
            n = len(self.rowzies[m])
            k = len(self.row_numbers[m])
            rjs_list = [rls]
            rje_list = []
            for j in range(1, k):
                items = [(self.row_numbers[m][i] + 1) for i in range(0, j)]
                rjs = sum(items)
                rjs_list.append(rjs)
            for j in range(0, k - 1):
                items = [(self.row_numbers[m][i] + 1) for i in range(j + 1, k)]
                rje = n - sum(items)
                rje_list.append(rje)
            rke = n
            rje_list.append(rke)
            if m == 4:
                print(rjs_list)
                print(rje_list)

            # RULE 1.1
            for j in range(k):
                for i in range(n):
                    if rje_list[j] - self.row_numbers[m][j] <= i < rjs_list[j] + self.row_numbers[m][j]:
                        self.rows[m][i].update_cell(screen, (0, 0, 0))
                        self.rows[m][i].state = 1

            # RULE 1.2
            for i in range(n):
                if 0 <= i < rls or rke < i < n or self.row_numbers[m][0] == 0:
                    self.rows[m][i].cross(screen)
                    self.rows[m][i].state = 0
                for j in range(k - 1):
                    if rje_list[j] <= i < rjs_list[j + 1]:
                        self.rows[m][i].cross(screen)
                        self.rows[m][i].state = 0

            # RULE 1.3
            for j in range(k):
                rjs = rjs_list[j]
                if self.rows[m][rjs].state == 1:
                    preempt = True
                    for i in range(k):
                        if rjs_list[i] <= rjs < rje_list[i] and i != j and self.row_numbers[i] != 1:
                            preempt = False
                    if preempt:
                        self.rows[m][rjs - 1].cross(screen)
                        self.rows[m][rjs - 1].state = 0

            # RULE 1.4
            for i in range(1, n - 1):
                if self.rows[m][i - 1].state == 1 and self.rows[m][i + 1].state == 1 and self.rows[m][i].state == -1:
                    maxl = 0
                    for j in range(k):
                        if rjs_list[j] <= i < rje_list[j]:
                            if self.row_numbers[m][j] > maxl:
                                maxl = self.row_numbers[m][j]
                    started = 0
                    enabled = 0
                    segmentl = 0
                    self.rows[m][i].state = 1
                    for cell in self.rows[m]:
                        if cell == self.rows[m][i]:
                            enabled = 1
                        if cell.state == 1:
                            started += 1
                        else:
                            if enabled:
                                segmentl = started
                            started = 0
                    if segmentl > maxl:
                        self.rows[m][i].cross(screen)
                        self.rows[m][i].state = 0
                    else:
                        self.rows[m][i].state = -1

            # RULE 1.5
            for i in range(1, n):
                if self.rows[m][i - 1] != 1 and self.rows[m][i] == 1:
                    minl = 1000
                    for j in range(k):
                        if rjs_list[j] <= i < rje_list[j]:
                            if self.row_numbers[m][j] < minl:
                                minl = self.row_numbers[m][j]
                    distance = 1000
                    closest = 1000
                    for t in range(i - minl + 1, i):
                        if self.rows[m][t].state == 0:
                            if (i - t) < distance:
                                distance = i - t
                                closest = t
                    if distance != 1000:
                        for p in range(i + 1, closest + minl):
                            self.rows[m][p].update_cell(screen, (0, 0, 0))
                            self.rows[m][p].state = 1
                    distance = 1000
                    closest = 1000
                    for t in range(i + 1, i + minl):
                        if self.rows[m][t].state == 0:
                            if (i - t) < distance:
                                distance = i - t
                                closest = t
                    if distance != 1000:
                        for p in range(n - minl, i - 1):
                            self.rows[m][p].update_cell(screen, (0, 0, 0))
                            self.rows[m][p].state = 1
                    enabled = 0
                    started = 0
                    counter = 0
                    segmentl = 0
                    start = 0
                    end = 0
                    for cell in self.rows[m]:
                        if cell == self.rows[m][i]:
                            enabled = 1
                            counter += 1
                        if cell.state == 1:
                            started += 1
                        else:
                            if enabled:
                                segmentl = started
                                end = counter + i
                                start = end - segmentl
                            started = 0
                    enabled = 1
                    for j in range(k):
                        if rjs_list[j] <= i < rje_list[j]:
                            if self.row_numbers[m][j] != segmentl:
                                enabled = 0
                    if enabled:
                        self.rows[m][start - 1].cross(screen)
                        self.rows[m][start - 1].state = 0
                        self.rows[m][end].cross(screen)
                        self.rows[m][end].state = 0

            # RULE 2.1
            for j in range(k):
                if j != 0 and rjs_list[j] <= rjs_list[j - 1]:
                    rjs_list[j] = rjs_list[j - 1] + self.row_numbers[m][j - 1] + 1
                try:
                    if rje_list[j] >= rje_list[j + 1]:
                        rje_list[j] = rje_list[j + 1] - self.row_numbers[m][j + 1] - 1
                except IndexError:
                    continue

            # RULE 2.2
            for j in range(k):
                if j != 0 and self.rows[m][rjs_list[j - 1]].state == 1:
                    rjs_list[j] = rjs_list[j] + 1
                try:
                    if self.rows[m][rje_list[j + 1]].state == 1:
                        rje_list[j] = rje_list[j] - 1
                except IndexError:
                    continue

            # RULE 2.3



















