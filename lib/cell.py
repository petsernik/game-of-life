import math

import pygame


class CellStorage:
    x, y = 0, 0
    x2, y2 = 0, 0
    size = 64
    size2 = 64
    pause = True
    point_mode = True
    erase_mode = False
    grid_mode = False
    frames = [{}]
    frame = 0
    dict_cell = {}
    new_cells = {}
    del_cells = {}
    colors = {
        "red": (230, 0, 0),
        "green": (0, 200, 0),
        "blue": (0, 0, 200),
        "yellow": (255, 255, 0),
        "black": (0, 0, 0),
        "fake": (190, 190, 190),
        "pale red": (255, 180, 180),
        "pale green": (152, 251, 152),
        "pale blue": (175, 238, 238),
        "pale yellow": (255, 255, 102),
        "pale black": (181, 184, 177),
        "pale fake": (225, 225, 225),
    }
    color_name = "red"
    neigh = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    point = [(0, 0)]
    figure = [(0, 0)]
    pattern_index = 0
    patterns = [
        [
            (0, 1),
            (1, 0),
            (-1, -1), (0, -1), (1, -1)
        ],
        [
            (0, 1),
            (-1, 0), (0, 0), (1, 0),
            (-1, -1), (1, -1)
        ],
        [(i, j) for i in range(-1, 2) for j in range(-1, 2)],
        []
    ]
    screen = None
    grid = None
    running_screen = 1

    @staticmethod
    def update_grid(s2 = False):
        size = CellStorage.screen.get_size()

        CellStorage.grid = pygame.Surface(size)
        CellStorage.grid.set_alpha(40)
        CellStorage.grid.fill((255, 255, 255))

        a, b = size
        cs_size = CellStorage.size if not s2 else CellStorage.size2
        cs_x, cs_y = (CellStorage.x, CellStorage.y) if not s2 else (CellStorage.x2, CellStorage.y2)

        start_x = cs_x % cs_size - cs_size
        start_y = cs_y % cs_size - cs_size

        for i in range(int(a / cs_size) + 1):
            pygame.draw.aaline(CellStorage.grid,
                               CellStorage.colors['black'],
                               [start_x + i * cs_size, 0],
                               [start_x + i * cs_size, b])

        for j in range(int(b / cs_size) + 1):
            pygame.draw.aaline(CellStorage.grid,
                               CellStorage.colors['black'],
                               [0, start_y + j * cs_size],
                               [a, start_y + j * cs_size])

    @staticmethod
    def rotate(figure=None):
        if figure is None:
            x = CellStorage.patterns[CellStorage.pattern_index]
            x = [(j, -i) for i, j in x]
            CellStorage.patterns[CellStorage.pattern_index] = x
            CellStorage.figure = x
        else:
            return [(j, -i) for i, j in figure]

    @staticmethod
    def left_frame():
        if CellStorage.frame >= 1:
            CellStorage.frame -= 1
            CellStorage.dict_cell = CellStorage.frames[CellStorage.frame]

    @staticmethod
    def right_frame():
        if CellStorage.frame == len(CellStorage.frames) - 1:
            CellStorage.new_stage()
        else:
            CellStorage.frame += 1
            CellStorage.dict_cell = CellStorage.frames[CellStorage.frame]

    @staticmethod
    def s_draw(i, j, color, s2=False):
        cs_size = CellStorage.size if not s2 else CellStorage.size2
        cs_x, cs_y = (CellStorage.x, CellStorage.y) if not s2 else (CellStorage.x2, CellStorage.y2)

        x, y = cs_x + i * cs_size, cs_y - j * cs_size
        a, b = CellStorage.screen.get_size()
        if -cs_size <= x <= a and -cs_size <= y <= b:
            pygame.draw.rect(CellStorage.screen, color,
                             (x, y, cs_size, cs_size))

    @staticmethod
    def draw_pale(i, j):
        if "pale " + CellStorage.color_name in CellStorage.colors:
            for x, y in CellStorage.figure:
                CellStorage.s_draw(x + i, y + j, CellStorage.colors["pale " + CellStorage.color_name])
        else:
            for x, y in CellStorage.figure:
                CellStorage.s_draw(x + i, y + j, CellStorage.color_name)

    @staticmethod
    def draw_grid(s2 = False):
        CellStorage.update_grid(s2)
        CellStorage.screen.blit(CellStorage.grid, (0, 0))

    @staticmethod
    def set_color(color):
        if isinstance(color, str):
            CellStorage.color_name = color

    @staticmethod
    def set_figure_i(i):
        CellStorage.pattern_index = i

    @staticmethod
    def get_figure_i():
        return CellStorage.pattern_index

    @staticmethod
    def count_neigh(i, j):
        cnt = 0
        for di, dj in CellStorage.neigh:
            cnt += (i + di, j + dj) in CellStorage.dict_cell
        return cnt

    @staticmethod
    def medium_neigh_color(i, j):
        lst = []
        for p in CellStorage.neigh:
            if (i + p[0], j + p[1]) in CellStorage.dict_cell:
                lst.append(CellStorage.dict_cell[(i + p[0], j + p[1])])
        r, g, b = 0, 0, 0
        for cell in lst:
            r += cell.color[0] ** 2
            g += cell.color[1] ** 2
            b += cell.color[2] ** 2
        if len(lst):
            r, g, b = map(lambda x: math.ceil((x // len(lst)) ** 0.5), [r, g, b])
        return r, g, b

    @staticmethod
    def new_stage():
        if CellStorage.frame != len(CellStorage.frames) - 1:
            CellStorage.frame += 1
            CellStorage.dict_cell = CellStorage.frames[CellStorage.frame]
        else:
            CellStorage.frames[CellStorage.frame] = CellStorage.dict_cell.copy()
            for cell in CellStorage.dict_cell.values():
                cell.update()
            for cell in CellStorage.del_cells:
                CellStorage.delitem(cell)
            for cell, color in CellStorage.new_cells.items():
                Cell(cell[0], cell[1], color)
            CellStorage.del_cells, CellStorage.new_cells = {}, {}
            CellStorage.frame += 1
            CellStorage.frames.append(CellStorage.dict_cell.copy())

    @staticmethod
    def mouse_cell_coord(s2=False):
        x, y = pygame.mouse.get_pos()
        i, j = CellStorage.get_ij(x, y, s2)
        return i, j

    @staticmethod
    def resize(k, s2=False):
        if not s2:
            if 1 <= CellStorage.size * k <= 64:
                x, y = pygame.mouse.get_pos()
                i, j = CellStorage.mouse_cell_coord()
                CellStorage.size *= k
                CellStorage.x = x - i * CellStorage.size
                CellStorage.y = y + j * CellStorage.size
        else:
            if 1 <= CellStorage.size2 * k <= 64:
                CellStorage.size2 *= k

    @staticmethod
    def create(i, j):
        for x, y in CellStorage.figure:
            Cell(x + i, y + j)
        CellStorage.frames = CellStorage.frames[:CellStorage.frame + 1]

    @staticmethod
    def create_with_del(i, j):
        for x, y in CellStorage.figure:
            if (x + i, y + j) in CellStorage.dict_cell:
                CellStorage.delitem(x + i, y + j)
            else:
                Cell(x + i, y + j)
        CellStorage.frames = CellStorage.frames[:CellStorage.frame + 1]

    @staticmethod
    def del_by_figure(i, j):
        for x, y in CellStorage.figure:
            CellStorage.delitem(x + i, y + j)
        CellStorage.frames = CellStorage.frames[:CellStorage.frame + 1]

    @staticmethod
    def delitem(key, j=None):
        if j is not None:
            key = (key, j)
        if key in CellStorage.dict_cell:
            CellStorage.dict_cell.pop(key)

    @staticmethod
    def get_ij(x, y, s2=False):
        if not s2:
            i = (x - CellStorage.x) // CellStorage.size
            j = (CellStorage.y - y) // CellStorage.size + 1
            return i, j
        else:
            i = (x - CellStorage.x2) // CellStorage.size2
            j = (CellStorage.y2 - y) // CellStorage.size2 + 1
            return i, j

    @staticmethod
    def keys():
        return CellStorage.dict_cell.keys()

    @staticmethod
    def values():
        return CellStorage.dict_cell.values()

    @staticmethod
    def cell_colors():
        return [cell.color for cell in CellStorage.dict_cell.values()]

    @staticmethod
    def clear():
        CellStorage.dict_cell.clear()
        CellStorage.frames = CellStorage.frames[:CellStorage.frame + 1]

    @staticmethod
    def set_point():
        CellStorage.figure = CellStorage.point

    @staticmethod
    def set_figure(i=None, f=None):
        if i is None:
            CellStorage.figure = CellStorage.patterns[CellStorage.pattern_index]
        elif f is None:
            if isinstance(i, list):
                CellStorage.figure = i
            if isinstance(i, int):
                CellStorage.figure = CellStorage.patterns[i]
        else:
            CellStorage.patterns[i] = f

    @staticmethod
    def set_prev_figure():
        CellStorage.pattern_index = max(CellStorage.pattern_index - 1, 0)
        if not CellStorage.point_mode:
            CellStorage.figure = CellStorage.patterns[CellStorage.pattern_index]

    @staticmethod
    def set_next_figure(empty_allow=True):
        fi = CellStorage.pattern_index
        fs = CellStorage.patterns
        if fi == len(fs) - 1 and len(fs[fi]) > 0:
            CellStorage.patterns.append([])
        fi = min(fi + 1, len(CellStorage.patterns) - 1)
        if not empty_allow and len(CellStorage.patterns[fi]) == 0 and fi > 0:
            fi -= 1
        if not CellStorage.point_mode:
            CellStorage.figure = CellStorage.patterns[fi]
        CellStorage.pattern_index = fi

    @staticmethod
    def get_figure(i=None):
        if i is None:
            return CellStorage.figure
        else:
            return CellStorage.patterns[i]

    @staticmethod
    def upd_point(i, j, s2=False):
        if s2:
            if (i, j) in CellStorage.patterns[CellStorage.pattern_index]:
                CellStorage.patterns[CellStorage.pattern_index].remove((i, j))
            else:
                if not CellStorage.erase_mode:
                    CellStorage.patterns[CellStorage.pattern_index].append((i, j))

    @staticmethod
    def upd_point_by_motion(s2=False):
        i, j = CellStorage.mouse_cell_coord(s2)
        if (i, j) not in CellStorage.patterns[CellStorage.pattern_index]:
            if not CellStorage.erase_mode:
                CellStorage.patterns[CellStorage.pattern_index].append((i, j))
        if CellStorage.erase_mode:
            if (i, j) in CellStorage.patterns[CellStorage.pattern_index]:
                CellStorage.patterns[CellStorage.pattern_index].remove((i, j))

    @staticmethod
    def upd_figures(new_figures=None):
        if new_figures is None:
            figure = CellStorage.patterns[CellStorage.pattern_index]
            CellStorage.patterns = list(filter(lambda x: len(x) > 0, CellStorage.patterns))
            CellStorage.patterns.append([])
            CellStorage.pattern_index = CellStorage.patterns.index(figure)
        else:
            CellStorage.patterns = new_figures

    @staticmethod
    def draw_figure(s2=False):
        for i, j in CellStorage.patterns[CellStorage.pattern_index]:
            CellStorage.s_draw(i, j, CellStorage.colors[CellStorage.color_name], s2)


class Cell:
    def __init__(self, i=0, j=0, color=None):
        self.i, self.j = i, j
        if color is None:
            self.color = CellStorage.colors[CellStorage.color_name]
        else:
            self.color = color
        CellStorage.dict_cell[(i, j)] = self

    def draw(self):
        CellStorage.s_draw(self.i, self.j, self.color)

    def update(self):
        i, j = self.i, self.j
        for p in CellStorage.neigh:
            x, y = i + p[0], j + p[1]
            if CellStorage.count_neigh(x, y) == 3:
                if (x, y) not in CellStorage.new_cells and (x, y) not in CellStorage.dict_cell:
                    CellStorage.new_cells[(x, y)] = CellStorage.medium_neigh_color(x, y)
        cnt = CellStorage.count_neigh(i, j)
        if cnt < 2 or cnt > 3:
            CellStorage.del_cells[(i, j)] = True
