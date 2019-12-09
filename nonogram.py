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

    def solve_nonogram(self, screen, clock):
        initial = True
        rjs = []
        rje = []
        k_list = []
        for m in range(len(self.rowzies)):
            # INITIAL RUN: Range Estimating
            rls = 0
            n = len(self.rowzies[m])
            k = len(self.row_numbers[m])
            rjs_list = [rls]
            rje_list = []
            for j in range(1, k):
                items = [(self.row_numbers[m][i] + 1) for i in range(0, j)]
                rjs_1 = sum(items)
                rjs_list.append(rjs_1)
            for j in range(0, k - 1):
                items = [(self.row_numbers[m][i] + 1) for i in range(j + 1, k)]
                rje_1 = n - sum(items)
                rje_list.append(rje_1)
            rke = n
            rje_list.append(rke)
            rjs.append(rjs_list)
            rje.append(rje_list)
            k_list.append(k)
        print(k_list)
        while True:
            for m in range(len(self.rowzies)):
                # RULE 1.1
                for j in range(k_list[m]):
                    for i in range(n):
                        if rje[m][j] - self.row_numbers[m][j] <= i < rjs[m][j] + self.row_numbers[m][j]:
                            self.rows[m][i].update_cell(screen, (0, 0, 0))
                            self.rows[m][i].state = 1
                            clock.tick(20)

                # RULE 1.2
                for i in range(n):
                    if 0 <= i < rls or rke < i < n or self.row_numbers[m][0] == 0:
                        self.rows[m][i].cross(screen)
                        self.rows[m][i].state = 0
                        clock.tick(20)
                    for j in range(k_list[m] - 1):
                        if rje[m][j] <= i < rjs[m][j + 1]:
                            self.rows[m][i].cross(screen)
                            self.rows[m][i].state = 0
                            clock.tick(20)

                # RULE 1.3
                for j in range(k_list[m]):
                    rjs_1 = rjs[m][j]
                    if self.rows[m][rjs_1].state == 1:
                        preempt = True
                        for i in range(k_list[m]):
                            if rjs[m][i] <= rjs_1 < rje[m][i] and i != j and self.row_numbers[i] != 1:
                                preempt = False
                        if preempt:
                            self.rows[m][rjs_1 - 1].cross(screen)
                            self.rows[m][rjs_1 - 1].state = 0
                            clock.tick(20)
                # RULE 1.4
                for i in range(1, n - 1):
                    if self.rows[m][i - 1].state == 1 and self.rows[m][i + 1].state == 1 and self.rows[m][i].state == -1:
                        maxl = 0
                        for j in range(k_list[m]):
                            if rjs[m][j] <= i < rje[m][j]:
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
                            clock.tick(20)
                        else:
                            self.rows[m][i].state = -1

                # RULE 1.5
                for i in range(1, n):
                    if self.rows[m][i - 1] != 1 and self.rows[m][i] == 1:
                        minl = 1000
                        for j in range(k_list[m]):
                            if rjs[m][j] <= i < rje[m][j]:
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
                                clock.tick(20)
                                print("aaa")
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
                                clock.tick(20)
                                print("bbb")
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
                        for j in range(k_list[m]):
                            if rjs[m][j] <= i < rje[m][j]:
                                if self.row_numbers[m][j] != segmentl:
                                    enabled = 0
                        if enabled:
                            self.rows[m][start - 1].cross(screen)
                            self.rows[m][start - 1].state = 0
                            self.rows[m][end].cross(screen)
                            self.rows[m][end].state = 0
                            clock.tick(20)
                            print("ccc")

                # RULE 2.1
                for j in range(k_list[m]):
                    if j != 0 and rjs[m][j] <= rjs[m][j - 1]:
                        rjs[m][j] = rjs[m][j - 1] + self.row_numbers[m][j - 1] + 1
                        print("changed")
                    try:
                        if rje[m][j] >= rje[m][j + 1]:
                            rje[m][j] = rje[m][j + 1] - self.row_numbers[m][j + 1] - 1
                            print("changed")
                    except IndexError:
                        continue

                # RULE 2.2
                for j in range(k_list[m]):
                    if j != 0 and self.rows[m][rjs[m][j] - 1].state == 1:
                        rjs[m][j] = rjs[m][j] + 1
                        print("change at", j, m)
                    try:
                        if self.rows[m][rje[m][j]].state == 1:
                            rje[m][j] = rje[m][j] - 1
                            print("change at", j, m)
                    except IndexError:
                        continue

                # RULE 2.3
                for j in range(k_list[m]):
                    B = []
                    enabled = 0
                    started = 0
                    counter = 0
                    segmentl = 0
                    start = 0
                    end = 0
                    for i in range(rjs[m][j], rje[m][j]):
                        if self.rows[m][i].state == 1:
                            if not started:
                                start = i
                            started = 1
                        else:
                            if started:
                                end = i
                                B.append((start, end))
                            started = 0
                    print(B, j, m)
                    for start, end in B:
                        if end - start > self.row_numbers[m][j]:
                            if j != 0 and rje[m][j - 1] > start:
                                rjs[m][j] = end + 1
                            elif j != k_list[m] - 1 and rjs[m][j+1] < end:
                                rje[m][j] = start - 1

                # RULE 3.1
                for j in range(1, k_list[m] - 1):
                    enabled = 0
                    for i in range(rje[m][j-1], rjs[m][j+1]):
                        if not enabled and self.rows[m][i].state == 1:
                            c_m = i
                            enabled = 1
                    enabled = 0
                    for i in reversed(range(rje[m][j-1], rjs[m][j+1])):
                        if not enabled and self.rows[m][i].state == 1:
                            c_n = i
                            enabled = 1
                    if enabled:
                        for idf in range(c_m, c_n):
                            self.rows[m][idf].update_cell(screen, (0, 0, 0))
                            self.rows[m][idf].state = 1
                            clock.tick(20)
                        c_u = self.row_numbers[m][j]
                        rjs[m][j] = c_n - c_u
                        rje[m][j] = c_m + c_u
            break

    def solve_nonogram_col(self, screen, clock):
        initial = True
        rjs = []
        rje = []
        k_list = []
        for m in range(len(self.cowzies)):
            # INITIAL RUN: Range Estimating
            rls = 0
            n = len(self.cowzies[m])
            k = len(self.column_numbers[m])
            rjs_list = [rls]
            rje_list = []
            for j in range(1, k):
                items = [(self.column_numbers[m][i] + 1) for i in range(0, j)]
                rjs_1 = sum(items)
                rjs_list.append(rjs_1)
            for j in range(0, k - 1):
                items = [(self.column_numbers[m][i] + 1) for i in range(j + 1, k)]
                rje_1 = n - sum(items)
                rje_list.append(rje_1)
            rke = n
            rje_list.append(rke)
            rjs.append(rjs_list)
            rje.append(rje_list)
            k_list.append(k)
        print(k_list)
        for m in range(len(self.cowzies)):
            # RULE 1.1
            for j in range(k_list[m]):
                for i in range(n):
                    if rje[m][j] - self.column_numbers[m][j] <= i < rjs[m][j] + self.column_numbers[m][j]:
                        self.columns[m][i].update_cell(screen, (0, 0, 0))
                        self.columns[m][i].state = 1
                        clock.tick(20)

            # RULE 1.2
            for i in range(n):
                if 0 <= i < rls or rke < i < n or self.column_numbers[m][0] == 0:
                    self.columns[m][i].cross(screen)
                    self.columns[m][i].state = 0
                    clock.tick(20)
                for j in range(k_list[m] - 1):
                    if rje[m][j] <= i < rjs[m][j + 1]:
                        self.columns[m][i].cross(screen)
                        self.columns[m][i].state = 0
                        clock.tick(20)

            # RULE 1.3
            for j in range(k_list[m]):
                rjs_1 = rjs[m][j]
                if self.columns[m][rjs_1].state == 1:
                    preempt = True
                    for i in range(k_list[m]):
                        if rjs[m][i] <= rjs_1 < rje[m][i] and i != j and self.row_numbers[i] != 1:
                            preempt = False
                    if preempt:
                        self.columns[m][rjs_1 - 1].cross(screen)
                        self.columns[m][rjs_1 - 1].state = 0
                        clock.tick(20)
            # RULE 1.4
            for i in range(1, n - 1):
                if self.columns[m][i - 1].state == 1 and self.columns[m][i + 1].state == 1 and self.columns[m][i].state == -1:
                    maxl = 0
                    for j in range(k_list[m]):
                        if rjs[m][j] <= i < rje[m][j]:
                            if self.column_numbers[m][j] > maxl:
                                maxl = self.column_numbers[m][j]
                    started = 0
                    enabled = 0
                    segmentl = 0
                    self.columns[m][i].state = 1
                    for cell in self.columns[m]:
                        if cell == self.columns[m][i]:
                            enabled = 1
                        if cell.state == 1:
                            started += 1
                        else:
                            if enabled:
                                segmentl = started
                            started = 0
                    if segmentl > maxl:
                        self.columns[m][i].cross(screen)
                        self.columns[m][i].state = 0
                        clock.tick(20)
                    else:
                        self.columns[m][i].state = -1

            # RULE 1.5
            for i in range(1, n):
                if self.columns[m][i - 1] != 1 and self.columns[m][i] == 1:
                    minl = 1000
                    for j in range(k_list[m]):
                        if rjs[m][j] <= i < rje[m][j]:
                            if self.column_numbers[m][j] < minl:
                                minl = self.column_numbers[m][j]
                    distance = 1000
                    closest = 1000
                    for t in range(i - minl + 1, i):
                        if self.columns[m][t].state == 0:
                            if (i - t) < distance:
                                distance = i - t
                                closest = t
                    if distance != 1000:
                        for p in range(i + 1, closest + minl):
                            self.columns[m][p].update_cell(screen, (0, 0, 0))
                            self.columns[m][p].state = 1
                            clock.tick(20)
                            print("aaa")
                    distance = 1000
                    closest = 1000
                    for t in range(i + 1, i + minl):
                        if self.columns[m][t].state == 0:
                            if (i - t) < distance:
                                distance = i - t
                                closest = t
                    if distance != 1000:
                        for p in range(n - minl, i - 1):
                            self.columns[m][p].update_cell(screen, (0, 0, 0))
                            self.columns[m][p].state = 1
                            clock.tick(20)
                            print("bbb")
                    enabled = 0
                    started = 0
                    counter = 0
                    segmentl = 0
                    start = 0
                    end = 0
                    for cell in self.columns[m]:
                        if cell == self.columns[m][i]:
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
                    for j in range(k_list[m]):
                        if rjs[m][j] <= i < rje[m][j]:
                            if self.column_numbers[m][j] != segmentl:
                                enabled = 0
                    if enabled:
                        self.columns[m][start - 1].cross(screen)
                        self.columns[m][start - 1].state = 0
                        self.columns[m][end].cross(screen)
                        self.columns[m][end].state = 0
                        clock.tick(20)
                        print("ccc")

            # RULE 2.1
            for j in range(k_list[m]):
                if j != 0 and rjs[m][j] <= rjs[m][j - 1]:
                    rjs[m][j] = rjs[m][j - 1] + self.column_numbers[m][j - 1] + 1
                    print("changed")
                try:
                    if rje[m][j] >= rje[m][j + 1]:
                        rje[m][j] = rje[m][j + 1] - self.column_numbers[m][j + 1] - 1
                        print("changed")
                except IndexError:
                    continue

            # RULE 2.2
            for j in range(k_list[m]):
                if j != 0 and self.columns[m][rjs[m][j] - 1].state == 1:
                    rjs[m][j] = rjs[m][j] + 1
                    print("change at", j, m)
                try:
                    if self.columns[m][rje[m][j]].state == 1:
                        rje[m][j] = rje[m][j] - 1
                        print("change at", j, m)
                except IndexError:
                    continue

            # RULE 2.3
            for j in range(k_list[m]):
                B = []
                enabled = 0
                started = 0
                counter = 0
                segmentl = 0
                start = 0
                end = 0
                for i in range(rjs[m][j], rje[m][j]):
                    if self.columns[m][i].state == 1:
                        if not started:
                            start = i
                        started = 1
                    else:
                        if started:
                            end = i
                            B.append((start, end))
                        started = 0
                print(B, j, m)
                for start, end in B:
                    if end - start > self.column_numbers[m][j]:
                        if j != 0 and rje[m][j - 1] > start:
                            rjs[m][j] = end + 1
                        elif j != k_list[m] - 1 and rjs[m][j+1] < end:
                            rje[m][j] = start - 1

            # RULE 3.1
            for j in range(1, k_list[m] - 1):
                enabled = 0
                for i in range(rje[m][j-1], rjs[m][j+1]):
                    if not enabled and self.columns[m][i].state == 1:
                        c_m = i
                        enabled = 1
                enabled = 0
                for i in reversed(range(rje[m][j-1], rjs[m][j+1])):
                    if not enabled and self.columns[m][i].state == 1:
                        c_n = i
                        enabled = 1
                if enabled:
                    for idf in range(c_m, c_n):
                        self.columns[m][idf].update_cell(screen, (0, 0, 0))
                        self.columns[m][idf].state = 1
                        clock.tick(20)
                    c_u = self.column_numbers[m][j]
                    rjs[m][j] = c_n - c_u
                    rje[m][j] = c_m + c_u





















