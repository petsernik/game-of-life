import math
from itertools import product
from typing import Optional

import pygame

from lib.music import play_note


def prepare_color(color):
    if len(color) == 4:
        return color
    if len(color) == 3:
        return color[0], color[1], color[2], 255
    raise "unexpected color"


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def colorless(color):
    return color[0], color[1], color[2], color[3] // 3


def color_set_alpha(color, alpha=255):
    return color[0], color[1], color[2], alpha


def update_mode(mode, cur_mode, number_of_modes):
    if mode is None:
        return cur_mode + 1 if cur_mode + 1 < number_of_modes else 0
    else:
        return mode


def number_by_bits(booleans: list[bool]) -> int:
    num = 0
    deg = 0
    for boolean in booleans:
        num += boolean * (1 << deg)
        deg += 1
    return num


class CellStorage:
    x, y = 0, 0
    x2, y2 = 0, 0
    size = 64
    size2 = 64
    extra = 2 ** 20
    pause = True
    point_mode, figure_mode, art_mode = 0, 1, 2
    draw_mode = point_mode
    number_of_draw_modes = 3
    erase_mode = False
    grid_mode = False
    transparency_init, transparency_max = 0, 1
    transparency_mode = transparency_init
    number_of_transparency_modes = 2
    frames = [{}]
    frames_medium_colors = [(230, 0, 0, 255)]
    frames_music_cells = [[]]
    frame = 0
    dict_cell = {}
    new_cells_positions = {}
    del_cells_positions = {}
    was_new_cells = []
    colors = {
        "red": (230, 0, 0, 255),
        "green": (0, 200, 0, 255),
        "blue": (0, 0, 200, 255),
        "yellow": (255, 255, 0, 255),
        "black": (0, 0, 0, 255),
        "fake": (190, 190, 190, 255),
        "gray": (222, 222, 222, 255),
        "white": (255, 255, 255, 255),
    }
    color = colors["red"]
    transparency = 255
    neigh = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    point = [(0, 0, None)]
    figure = point
    pattern_index = 0
    patterns = [
        [
            (0, 1, None),
            (1, 0, None),
            (-1, -1, None), (0, -1, None), (1, -1, None)
        ],
        [
            (0, 1, None),
            (-1, 0, None), (0, 0, None), (1, 0, None),
            (-1, -1, None), (1, -1, None)
        ],
        [(i, j, None) for i in range(-1, 2) for j in range(-1, 2)],
        []
    ]
    art_index = 0
    arts = [[]]
    screen = None
    grid = None
    running_screen = 1

    @staticmethod
    def update_transparency_mode(mode=None):
        CellStorage.transparency_mode = \
            update_mode(mode, CellStorage.transparency_mode, CellStorage.number_of_transparency_modes)

    @staticmethod
    def update_draw_mode(mode=None):
        CellStorage.draw_mode = update_mode(mode, CellStorage.draw_mode, CellStorage.number_of_draw_modes)
        if (
                mode is None
                and
                (CellStorage.draw_mode == CellStorage.figure_mode and CellStorage.patterns[0] == []
                 or
                 CellStorage.draw_mode == CellStorage.art_mode and CellStorage.arts[0] == [])
        ):
            CellStorage.update_draw_mode()
            return
        if CellStorage.draw_mode == CellStorage.point_mode:
            CellStorage.figure = CellStorage.point
        elif CellStorage.draw_mode == CellStorage.figure_mode:
            CellStorage.figure = CellStorage.patterns[CellStorage.pattern_index]
        elif CellStorage.draw_mode == CellStorage.art_mode:
            CellStorage.figure = CellStorage.arts[CellStorage.art_index]

    @staticmethod
    def update_grid(s2=False):
        cs_size = CellStorage.size2 if s2 else CellStorage.size

        a, b = CellStorage.screen.get_size()
        a += cs_size
        b += cs_size

        CellStorage.grid = pygame.Surface((a, b))
        CellStorage.grid.set_alpha(40)
        CellStorage.grid.fill((255, 255, 255))

        for i in range(int(a / cs_size) + 1):
            pygame.draw.aaline(CellStorage.grid,
                               CellStorage.colors['black'],
                               [i * cs_size, 0],
                               [i * cs_size, b])

        for j in range(int(b / cs_size) + 1):
            pygame.draw.aaline(CellStorage.grid,
                               CellStorage.colors['black'],
                               [0, j * cs_size],
                               [a, j * cs_size])

    @staticmethod
    def update_collection_by_figure(fig=None):
        if fig is None:
            fig = CellStorage.figure
        if CellStorage.draw_mode == CellStorage.figure_mode:
            CellStorage.patterns[CellStorage.pattern_index] = fig
        elif CellStorage.draw_mode == CellStorage.art_mode:
            CellStorage.arts[CellStorage.art_index] = fig

    @staticmethod
    def rotate():
        CellStorage.figure = [(j, -i, c) for i, j, c in CellStorage.figure]
        CellStorage.update_collection_by_figure()

    @staticmethod
    def update_by_frame(frame=None):
        if frame is None:
            return CellStorage.update_by_frame(CellStorage.frame)
        CellStorage.dict_cell = CellStorage.frames[frame]

    @staticmethod
    def left_frame():
        if CellStorage.frame >= 1:
            CellStorage.frame -= 1
            CellStorage.update_by_frame()

    @staticmethod
    def increase_default_transparency():
        CellStorage.transparency = min(CellStorage.transparency+10, 255)
        CellStorage.color = color_set_alpha(CellStorage.color, CellStorage.transparency)

    @staticmethod
    def decrease_default_transparency():
        CellStorage.transparency = max(CellStorage.transparency-10, 0)
        CellStorage.color = color_set_alpha(CellStorage.color, CellStorage.transparency)

    @staticmethod
    def right_frame():
        if CellStorage.frame == len(CellStorage.frames) - 1:
            CellStorage.new_stage()
        else:
            CellStorage.frame += 1
            CellStorage.update_by_frame()

    @staticmethod
    def on_screen_with_rect(i, j, s2=False) -> (bool, (int, int, int, int)):
        cs_size = CellStorage.size if not s2 else CellStorage.size2
        cs_x, cs_y = (CellStorage.x, CellStorage.y) if not s2 else (CellStorage.x2, CellStorage.y2)
        x, y = cs_x + i * cs_size, cs_y - j * cs_size
        a, b = CellStorage.screen.get_size()
        on_screen, rect = -cs_size <= x <= a and -cs_size <= y <= b, (x, y, cs_size, cs_size)
        return on_screen, rect

    @staticmethod
    def s_draw(i, j, color=None, s2=False, ignore_t_mode=False):
        if color is None:
            color = CellStorage.color
        on_screen, rect = CellStorage.on_screen_with_rect(i, j, s2)
        if on_screen:
            if CellStorage.transparency_mode == CellStorage.transparency_max and not ignore_t_mode:
                draw_rect_alpha(CellStorage.screen, color_set_alpha(color, 255), rect)
            else:
                draw_rect_alpha(CellStorage.screen, color, rect)

    @staticmethod
    def draw_pale(i, j):
        if CellStorage.draw_mode == CellStorage.figure_mode:
            for x, y, color in CellStorage.figure:
                CellStorage.s_draw(x + i, y + j, colorless(CellStorage.color),
                                   ignore_t_mode=True)
        elif CellStorage.draw_mode == CellStorage.art_mode:
            for x, y, color in CellStorage.arts[CellStorage.art_index]:
                CellStorage.s_draw(x + i, y + j, colorless(color), ignore_t_mode=True)

    @staticmethod
    def draw_grid(s2=False):
        cs_size = CellStorage.size2 if s2 else CellStorage.size
        cs_x, cs_y = (CellStorage.x2, CellStorage.y2) if s2 else (CellStorage.x, CellStorage.y)

        CellStorage.screen.blit(CellStorage.grid, (cs_x % cs_size - cs_size, cs_y % cs_size - cs_size))

    @staticmethod
    def set_color(color):
        if isinstance(color, str):
            if CellStorage.transparency_mode == CellStorage.transparency_max:
                CellStorage.color = CellStorage.colors[color]
            else:
                CellStorage.color = color_set_alpha(CellStorage.colors[color], CellStorage.transparency)


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
        return CellStorage.medium_color(lst)

    @staticmethod
    def medium_color(lst=None):
        if lst is None:
            return CellStorage.medium_color(CellStorage.dict_cell.values())

        r, g, b, a = 0, 0, 0, 0
        for cell in lst:
            r += cell.color[0] ** 2
            g += cell.color[1] ** 2
            b += cell.color[2] ** 2
            a += cell.color[3] ** 2
        if len(lst):
            r, g, b, a = map(lambda x: math.ceil((x // len(lst)) ** 0.5), [r, g, b, a])
        return r, g, b, a

    @staticmethod
    def step_stage():
        for cell in CellStorage.dict_cell.values():
            cell.update()
        for pos in CellStorage.del_cells_positions:
            CellStorage.delitem(pos)
        for pos, cell in CellStorage.new_cells_positions.items():
            CellStorage.dict_cell[pos] = cell
        CellStorage.was_new_cells = CellStorage.new_cells_positions.values()
        CellStorage.del_cells_positions, CellStorage.new_cells_positions = {}, {}

    @staticmethod
    def append_frame():
        CellStorage.frames.append(CellStorage.dict_cell.copy())
        lst = CellStorage.was_new_cells
        CellStorage.frames_medium_colors.append(CellStorage.medium_color(lst))
        CellStorage.frames_music_cells.append(lst)
        CellStorage.was_new_cells = []

    @staticmethod
    def extra_stage():
        if len(CellStorage.frames) < CellStorage.frame + CellStorage.extra:
            if CellStorage.frame == len(CellStorage.frames) - 1:
                CellStorage.frames[CellStorage.frame] = CellStorage.dict_cell.copy()
            else:
                CellStorage.dict_cell = CellStorage.frames[-1].copy()
            CellStorage.step_stage()
            CellStorage.append_frame()
            CellStorage.update_by_frame()

    @staticmethod
    def new_stage():
        if CellStorage.frame != len(CellStorage.frames) - 1:
            CellStorage.frame += 1
            CellStorage.update_by_frame()
        else:
            CellStorage.frames[CellStorage.frame] = CellStorage.dict_cell.copy()
            CellStorage.step_stage()
            CellStorage.frame += 1
            CellStorage.append_frame()

    @staticmethod
    def play_music(note_dur: float):
        color = CellStorage.frames_medium_colors[CellStorage.frame]
        booleans = [color[i] >= 128 for i in range(3)]
        tonality_index = number_by_bits(booleans)

        n = 8
        # was[r][c] = True if there is a cell at row r, col c
        was = [[[False for _ in range(n)] for _ in range(n)] for _ in range(256)]

        for cell in CellStorage.frames_music_cells[CellStorage.frame]:
            on_screen, _ = CellStorage.on_screen_with_rect(cell.i, cell.j)
            if on_screen:
                r = int(cell.i) % n
                c = int(cell.j) % n
                alpha = cell.color[3]
                was[alpha][r][c] = True

        # rightmost[alpha][r] will hold the largest column index in row r, or None
        rightmost: list[list[Optional[int]]] = [[None for _ in range(n)] for _ in range(256)]

        # scan each row r and column c
        for r, c, alpha in product(range(n), range(n), range(256)):
            if was[alpha][r][c]:
                # if first hit in this row, or c is greater than current
                if rightmost[alpha][r] is None or c > rightmost[alpha][r]:
                    rightmost[alpha][r] = c


        for alpha in range(256):
            p_dur = 2 - alpha/255
            # play a note for each row where we found at least one cell
            for r, c in enumerate(rightmost[alpha]):
                if c is not None:
                    play_note(tonality_index, c, r, note_dur=p_dur * note_dur)

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
                CellStorage.update_grid(s2)
        else:
            if 1 <= CellStorage.size2 * k <= 64:
                CellStorage.size2 *= k
                CellStorage.update_grid(s2)

    @staticmethod
    def cut():
        CellStorage.frames = CellStorage.frames[:CellStorage.frame + 1]

    @staticmethod
    def create(i, j):
        for x, y, color in CellStorage.figure:
            Cell(x + i, y + j, color)
        CellStorage.cut()

    @staticmethod
    def fake_create(i, j, fake_cells):
        for x, y, color in CellStorage.figure:
            fake_cells[(x + i, y + j)] = 1

    @staticmethod
    def create_with_del(i, j):
        if (i, j) in CellStorage.dict_cell:
            CellStorage.delitem(i, j)
        else:
            Cell(i, j)
        CellStorage.cut()

    @staticmethod
    def fake_create_with_del(i, j, fake_cells):
        if (i, j) in fake_cells:
            fake_cells.pop((i, j))
        else:
            fake_cells[(i, j)] = 1

    @staticmethod
    def del_by_figure(i, j):
        for x, y, color in CellStorage.figure:
            CellStorage.delitem(x + i, y + j)
        CellStorage.cut()

    @staticmethod
    def fake_del_by_figure(i, j, fake_cells):
        for x, y, color in CellStorage.figure:
            fake_cells.pop((x + i, y + j), None)

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
    def set_prev_figure(s2=False):
        if CellStorage.draw_mode == CellStorage.figure_mode or s2:
            CellStorage.pattern_index = max(CellStorage.pattern_index - 1, 0)
            CellStorage.figure = CellStorage.patterns[CellStorage.pattern_index]
        elif CellStorage.draw_mode == CellStorage.art_mode:
            CellStorage.art_index = max(CellStorage.art_index - 1, 0)
            CellStorage.figure = CellStorage.arts[CellStorage.art_index]

    @staticmethod
    def set_next_figure(empty_allow=False, s2=False):
        if CellStorage.draw_mode == CellStorage.figure_mode or s2:
            index = CellStorage.pattern_index
            collection = CellStorage.patterns
        elif CellStorage.draw_mode == CellStorage.art_mode:
            index = CellStorage.art_index
            collection = CellStorage.arts
        else:
            return

        if index == len(collection) - 1 and len(collection[index]) > 0:
            collection.append([])
        index = min(index + 1, len(collection) - 1)
        if not empty_allow and len(collection[index]) == 0 and index > 0:
            index -= 1

        if CellStorage.draw_mode == CellStorage.figure_mode or s2:
            CellStorage.pattern_index = index
            CellStorage.figure = CellStorage.patterns[index]
        elif CellStorage.draw_mode == CellStorage.art_mode:
            CellStorage.art_index = index
            CellStorage.figure = CellStorage.arts[CellStorage.art_index]

    @staticmethod
    def art_by_png(img):
        art = []
        w, h = img.get_width(), img.get_height()
        colors = [[img.get_at((i, j)) for j in range(h)] for i in range(w)]
        for i in range(w):
            for j in range(h):
                if colors[i][j][3]:
                    art.append((i - (w >> 1), (h >> 1) - j, colors[i][j]))
        return art

    @staticmethod
    def add_art_by_png(img):
        CellStorage.arts.append(CellStorage.art_by_png(img))

    @staticmethod
    def upd_point(i, j, s2=False):
        if s2:
            if (i, j, None) in CellStorage.patterns[CellStorage.pattern_index]:
                CellStorage.patterns[CellStorage.pattern_index].remove((i, j, None))
            else:
                if not CellStorage.erase_mode:
                    CellStorage.patterns[CellStorage.pattern_index].append((i, j, None))

    @staticmethod
    def upd_point_by_motion(s2=False):
        i, j = CellStorage.mouse_cell_coord(s2)
        if (i, j, None) not in CellStorage.patterns[CellStorage.pattern_index]:
            if not CellStorage.erase_mode:
                CellStorage.patterns[CellStorage.pattern_index].append((i, j, None))
        if CellStorage.erase_mode:
            if (i, j, None) in CellStorage.patterns[CellStorage.pattern_index]:
                CellStorage.patterns[CellStorage.pattern_index].remove((i, j, None))

    @staticmethod
    def update_figures(new_figures=None):
        if new_figures is None:
            figure = CellStorage.patterns[CellStorage.pattern_index]
            CellStorage.patterns = list(filter(lambda x: len(x) > 0, CellStorage.patterns))
            CellStorage.patterns.append([])
            CellStorage.pattern_index = CellStorage.patterns.index(figure)
        else:
            CellStorage.patterns = new_figures

    @staticmethod
    def update_arts(new_arts=None):
        if new_arts is None:
            # art = CellStorage.arts[CellStorage.art_index]
            CellStorage.arts = list(filter(lambda x: len(x) > 0, CellStorage.arts))
            CellStorage.arts.append([])
            # CellStorage.art_index = CellStorage.arts.index(art)
        else:
            CellStorage.arts = new_arts

    @staticmethod
    def enter_s1():
        if CellStorage.draw_mode == CellStorage.point_mode:
            CellStorage.figure = CellStorage.point
        elif CellStorage.draw_mode == CellStorage.figure_mode:
            if len(CellStorage.figure) == 0:
                CellStorage.pattern_index = max(CellStorage.pattern_index - 1, 0)
            CellStorage.figure = CellStorage.patterns[CellStorage.pattern_index]
        elif CellStorage.draw_mode == CellStorage.art_mode:
            if len(CellStorage.figure) == 0:
                CellStorage.art_index = max(CellStorage.art_index - 1, 0)
            CellStorage.figure = CellStorage.arts[CellStorage.art_index]

    @staticmethod
    def enter_s2():
        CellStorage.figure = CellStorage.patterns[CellStorage.pattern_index]

    @staticmethod
    def draw_figure(s2=False):
        for i, j, color in CellStorage.figure:
            CellStorage.s_draw(i, j, color, s2)


class Cell:
    def __init__(self, i=0, j=0, color=None, add_to_storage=True):
        self.i, self.j = i, j
        if color is None:
            self.color = CellStorage.color
        else:
            self.color = color
        if add_to_storage:
            CellStorage.dict_cell[(i, j)] = self

    def draw(self):
        CellStorage.s_draw(self.i, self.j, self.color)

    def update(self):
        i, j = self.i, self.j
        for p in CellStorage.neigh:
            x, y = i + p[0], j + p[1]
            if CellStorage.count_neigh(x, y) == 3:
                if (x, y) not in CellStorage.new_cells_positions and (x, y) not in CellStorage.dict_cell:
                    color = CellStorage.medium_neigh_color(x, y)
                    CellStorage.new_cells_positions[(x, y)] = Cell(x, y, color, False)
        cnt = CellStorage.count_neigh(i, j)
        if cnt < 2 or cnt > 3:
            CellStorage.del_cells_positions[(i, j)] = True
