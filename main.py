import pygame
import os
import sys
import ast
from screeninfo import get_monitors
from time import time
from pathlib import Path

from lib.cell import CellStorage, Cell, prepare_color
from lib.keyboard import KeyboardKey, update_key, get_keyboard_key
from lib.rect import fill, Button, Text, blit_text


def get_building_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)


def get_img(str_path, k=None, size=None, color=None, can_be_less_size=False):
    img = pygame.image.load(str_path)
    if k is not None:
        img = pygame.transform.scale(
            img, (img.get_width() * k,
                  img.get_height() * k))
    if size is not None:
        if can_be_less_size:
            img = pygame.transform.scale(img, (min(img.get_width(), size[0]), min(img.get_height(), size[1])))
        else:
            img = pygame.transform.scale(img, (size[0], size[1]))
    if color is not None:
        fill(img, color)
    return img


def main():
    pygame.init()
    monitor = get_monitors()[0]
    width, height = monitor.width, monitor.height
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    CellStorage.screen = screen
    CellStorage.update_grid()
    resource_path = 'resources'
    saves_path = 'saves'
    gallery_path = 'gallery'

    class SaveBox(Button):
        def __init__(self, prefix, image, text=''):
            super().__init__(image)
            self.prefix = prefix
            self.text = text
            self.timer = time()
            self.light = False

        def make_file(self):
            f = open(self.prefix + self.text, 'w')
            if self.prefix == '__parameters__':
                f.write(f'{CellStorage.x} {CellStorage.y} {CellStorage.size}\n')
                f.write(str(list(CellStorage.keys())) + '\n' + str(CellStorage.cell_colors()) + '\n')
                CellStorage.upd_figures()
                f.write(f'{CellStorage.get_figure_i()}\n')
                f.write(str(list(CellStorage.patterns)) + '\n')
                f.write(f'{dt}\n')
                f.write(str(list(fake_cells.keys())) + '\n')
                f.write(f'{CellStorage.color_name}\n')
                f.write(f'{hidden_mode}\n')
                # f.write(f'{CellStorage.frames()}\n')
            f.close()

        def upd_by_file(self, full=True):
            my_file = Path(self.prefix + self.text)
            if my_file.is_file():
                f = open(self.prefix + self.text, 'r')
                try:

                    if self.prefix == '__parameters__':
                        _x, _y, z = map(float, f.readline().split())
                        if full:
                            CellStorage.x, CellStorage.y, CellStorage.size = _x, _y, z
                        cords = ast.literal_eval(f.readline())
                        _colors = ast.literal_eval(f.readline())
                        CellStorage.clear()
                        for _i in range(len(cords)):
                            Cell(cords[_i][0], cords[_i][1], prepare_color(_colors[_i]))
                        _x, _y, z = int(f.readline()), ast.literal_eval(f.readline()), float(f.readline())
                        if full:
                            nonlocal dt
                            CellStorage.set_figure_i(_x)
                            CellStorage.upd_figures(_y)
                            dt = z
                        line = f.readline()
                        if full:
                            fake_cells.clear()
                            for _cell in ast.literal_eval(line):
                                fake_cells[_cell] = 1
                        color = f.readline().split()[0]
                        if full:
                            CellStorage.set_color(color)
                        line = f.readline()
                        if full:
                            nonlocal hidden_mode
                            hidden_mode = int(line)
                        # CellStorage.read_frames(f.read line())
                except Exception as exc:
                    print(exc)
                finally:
                    f.close()

        def launch(self):
            self.timer = time()
            self.make_file()
            self.set_color('red')
            self.light = True

        def dis_light(self):
            if time() - self.timer >= 0.16:
                self.light = False
            if not self.light:
                self.set_color('black')

    def screen_quit_1():
        nonlocal left_click_moving_time, right_click_moving
        left_click_moving_time, right_click_moving, CellStorage.erase_mode = 0.0, False, False
        for _btn in buttons1:
            _btn.hidden = False

    def screen_quit_2():
        CellStorage.upd_figures()
        s2_inv.set_color('black')
        screen_quit_1()

    def screen_quit_3():
        s3_info.set_color('black')
        screen_quit_1()

    def hide_buttons():
        if hidden_mode == 0:
            for _btn in buttons1:
                _btn.hidden = False
        elif hidden_mode == 1:
            play_box.hidden = True
        elif hidden_mode == 2:
            for _btn in buttons1:
                _btn.hidden = True

    def to_screen(sc):
        nonlocal running_screen
        if sc == 1:
            CellStorage.update_grid()
        elif sc == 2:
            CellStorage.update_grid(s2=True)

        if running_screen == sc:
            if sc == 2:
                screen_quit_2()
            elif sc == 3:
                screen_quit_3()
            CellStorage.update_grid()
            running_screen = 1
            CellStorage.enter_s1()
            return
        elif running_screen == 1:
            screen_quit_1()
        elif running_screen == 2:
            screen_quit_2()
        elif running_screen == 3:
            screen_quit_3()
        running_screen = sc

        if sc == 1:
            CellStorage.enter_s1()
        elif sc == 2:
            CellStorage.enter_s2()

    pygame.display.set_caption('Conway\'s game of life')
    running = True
    left_click_moving_time, right_click_moving = 0.0, False
    CellStorage.x, CellStorage.y = (width - CellStorage.size) // 2, (height - CellStorage.size) // 2
    CellStorage.x2, CellStorage.y2 = CellStorage.x, CellStorage.y
    t, dt = time(), 1 / 4
    running_screen = 0
    to_screen(1)
    fake_drawing = False
    colors = list(CellStorage.colors.keys())
    fake_cells = {}
    keyboard = dict([(key, KeyboardKey()) for key in KeyboardKey.all_keys()])
    hidden_mode = 0

    t_extra, dt_extra = time(), 1 / 2
    slow_mode = False

    __len__icon__ = min(50 * width // 1920, 50 * height // 1080)
    __size__icon__ = (__len__icon__, __len__icon__)
    s2_left = Button(get_img(get_building_path(f'{resource_path}/left.png'), size=(lambda xy: (2 * xy[0], 2 * xy[1]))(__size__icon__)))
    s2_left.upd_pos(10, (height - s2_left.height()) // 2)
    s2_right = Button(
        get_img(get_building_path(f'{resource_path}/right.png'), size=(lambda xy: (2 * xy[0], 2 * xy[1]))(__size__icon__)))
    s2_right.upd_pos(width - s2_right.width() - 10, (height - s2_left.height()) // 2)
    s2_inv = Button(get_img(get_building_path(f'{resource_path}/i.png'), size=__size__icon__))
    __right_height = 12
    s2_inv.upd_pos(width - 10 - s2_inv.width() - 5, __right_height)
    eraser = Button(get_img(get_building_path(f'{resource_path}/eraser.png'), size=__size__icon__))
    eraser.upd_pos(s2_inv.pos()[0] - eraser.width() - 5, __right_height)
    s3_info = Button(get_img(get_building_path(f'{resource_path}/info.png'), size=__size__icon__, color='black'))
    s3_info.upd_pos(eraser.pos()[0] - s3_info.width() - 5, __right_height)
    font = pygame.font.Font(None, 48)
    to_s1_text = Text(font.render('Return to the field', True, "black"))
    to_s1_text.upd_pos((width - to_s1_text.width()) // 2 - 10, height - 2 * to_s1_text.height())
    s3_info_text = ('The "Game of Life" by John Conway. \n'
                    'You place living cells on a grid, and then in each step the following happens: \n'
                    '1) A live cell survives if it has two or three live neighbors (out of 8). \n'
                    '2) Otherwise, a live cell dies. \n'
                    '3) A dead cell becomes alive if it has exactly 3 live neighbors. \n'
                    'Now about the controls: \n'
                    'Left mouse button (LMB) - place/remove a live cell. \n'
                    'LMB (held down) - draw a line of live cells. \n'
                    'Right mouse button (RMB, held down) - move around the field. \n'
                    'Space key - start/pause Conway\'s game. \n'
                    'Left/right arrow keys - slow down/speed up the game by a factor of two. \n'
                    'Mouse wheel - zoom in/out the field. \n'
                    'Key p or middle mouse button (MMB) - switch pattern mode. \n'
                    'Up/down arrow keys - switch between patterns. \n'
                    'Key r - rotate pattern 90 degrees clockwise. \n'
                    'Key e or button in the top-right corner - toggle eraser mode. \n'
                    'Key g - toggle grid mode on/off. \n'
                    'Key t - toggle transparent mode on/off. \n'
                    '1, 2, 3, 4, 5, 0 - drawing colors (0 is fake: i.e. does not participate in the game). \n'
                    'Key k - clear the field, ctrl+k - clear fake color cells. \n'
                    'Key i or the button in the top-right corner - you also have the option to create/delete patterns and select them from the inventory '
                    '(the last opened pattern is used). \n'
                    'Ctrl+s or the button in the top-right corner - save the field and patterns. \n'
                    'Ctrl+z - revert to the last saved state. \n'
                    'v, b - time travel (not saved). \n'
                    'Key h - toggle icon visibility mode (in the field). \n'
                    'Esc key - exit the current window (in the field: exit the application). \n')
    save = SaveBox('__parameters__', get_img(get_building_path(f'{resource_path}/save.png'), size=__size__icon__))
    save.upd_rect(s3_info.pos()[0] - s3_info.width() - 5, __right_height, s3_info.width(), s3_info.height())
    save.upd_by_file()
    play_box = Button(get_img(get_building_path(f'{resource_path}/play.png'), size=__size__icon__))
    play_box.upd_pos(10, __right_height)
    slow_switch = Button(get_img(get_building_path(f'{resource_path}/turtle.png'), size=__size__icon__))
    slow_switch.upd_pos(10, play_box.pos()[1] + play_box.height())
    buttons1 = [s2_inv, eraser, s3_info, save, play_box, slow_switch]
    buttons2 = [s2_left, s2_right, s2_inv, eraser, s3_info, save]
    buttons3 = [s2_inv, eraser, s3_info, save]
    s2_left.set_action(CellStorage.set_prev_figure)
    s2_right.set_action(CellStorage.set_next_figure)
    s2_inv.set_action(lambda: to_screen(2))
    s3_info.set_action(lambda: to_screen(3))
    save.set_action(save.launch)

    def __upd_pause():
        CellStorage.pause = not CellStorage.pause

    def __upd_erase_mode():
        CellStorage.erase_mode = not CellStorage.erase_mode

    def __upd_slow_mode():
        nonlocal slow_mode
        slow_mode = not slow_mode

    eraser.set_action(__upd_erase_mode)
    play_box.set_action(__upd_pause)
    slow_switch.set_action(__upd_slow_mode)

    slow_switch.set_color('red')

    for root, dirs, files in os.walk(gallery_path):
        for file in files:
            if file.endswith('.png'):
                CellStorage.add_art_by_png(get_img(
                    os.path.join(root,file),
                    size=list(map(lambda _: 2 * _, __size__icon__)),
                    can_be_less_size=True
                ))

    CellStorage.game_pause = CellStorage.pause

    CellStorage.upd_figures()
    CellStorage.upd_arts()
    CellStorage.update_grid()

    while running:
        screen.fill(CellStorage.colors["white"])
        if running_screen == 1:
            no_event = True
            for event in pygame.event.get():
                no_event = False
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False

                update_key(event, keyboard)

                if event.type == pygame.KEYDOWN:
                    key = get_keyboard_key(event)
                    if key in list('12345'):
                        CellStorage.set_color(colors[int(key) - 1])
                        fake_drawing = False
                    elif key == '0':
                        CellStorage.set_color('fake')
                        fake_drawing = True
                    elif key == 'w':
                        slow_mode = not slow_mode
                    elif key == 'r':
                        CellStorage.rotate()
                    elif key == 't':
                        CellStorage.update_transparency_mode()
                    elif key == 'i':
                        s2_inv.action(as_btn=False)
                    elif key == 'h':
                        hidden_mode = (hidden_mode + 1) % 3
                    elif key == 'esc':
                        running = False
                    elif key == 'F1':
                        s3_info.action(as_btn=False)
                    elif key == 'e':
                        eraser.action(as_btn=False)
                    elif key == 'p':
                        CellStorage.update_draw_mode()
                    elif key == 'g':
                        CellStorage.grid_mode = not CellStorage.grid_mode
                    elif key == 'space':
                        play_box.action(as_btn=False)
                    elif key == 'left':
                        dt = min(2 * dt, 4)
                    elif key == 'right':
                        dt = max(dt / 2, 1 / 2 ** 7)
                    elif key == 'v':
                        CellStorage.left_frame()
                        keyboard['v'].game_pause = keyboard['b'].game_pause if keyboard['b'].is_pressed \
                            else CellStorage.pause
                    elif key == 'b':
                        CellStorage.right_frame()
                        keyboard['b'].game_pause = keyboard['v'].game_pause if keyboard['v'].is_pressed \
                            else CellStorage.pause

                if keyboard['ctrl'].is_pressed:
                    if keyboard['k'].is_pressed:
                        fake_cells.clear()
                    if keyboard['s'].is_pressed:
                        save.launch()
                    if keyboard['z'].is_pressed:
                        save.upd_by_file(full=False)
                elif keyboard['k'].is_pressed:
                    CellStorage.clear()

                if event.type == pygame.KEYUP and event.key == pygame.K_v:
                    CellStorage.pause = keyboard['v'].game_pause
                if event.type == pygame.KEYUP and event.key == pygame.K_b:
                    CellStorage.pause = keyboard['b'].game_pause

                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    CellStorage.set_next_figure()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    CellStorage.set_prev_figure()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                    CellStorage.resize(2)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                    CellStorage.resize(1 / 2)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                    CellStorage.update_draw_mode()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    __break = False
                    for btn in buttons1:
                        if btn.collide_point(x, y):
                            btn.active = True
                            __break = True
                    i, j = CellStorage.get_ij(x, y)
                    if __break:
                        pass
                    elif fake_drawing:
                        if CellStorage.erase_mode:
                            CellStorage.fake_del_by_figure(i, j, fake_cells)
                        elif CellStorage.draw_mode == CellStorage.point_mode:
                            CellStorage.fake_create_with_del(i, j, fake_cells)
                        else:
                            CellStorage.fake_create(i, j, fake_cells)
                    elif CellStorage.erase_mode:
                        CellStorage.del_by_figure(i, j)
                    elif CellStorage.draw_mode == CellStorage.point_mode:
                        CellStorage.create_with_del(i, j)
                    else:
                        CellStorage.create(i, j)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    left_click_moving_time = time()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    left_click_moving_time = 0.0
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    right_click_moving = True
                if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    right_click_moving = False

                if event.type == pygame.MOUSEMOTION:
                    if left_click_moving_time > 0 and time() - left_click_moving_time >= 0.1:
                        i, j = CellStorage.mouse_cell_coord()
                        if not fake_drawing:
                            if CellStorage.erase_mode:
                                CellStorage.del_by_figure(i, j)
                            else:
                                CellStorage.create(i, j)
                        else:
                            if not CellStorage.erase_mode:
                                CellStorage.fake_create(i, j, fake_cells)
                            else:
                                CellStorage.fake_del_by_figure(i, j, fake_cells)
                    if right_click_moving:
                        CellStorage.x += event.rel[0]
                        CellStorage.y += event.rel[1]

            for btn in buttons1:
                btn.action()

            if running_screen != 1:
                continue

            hide_buttons()

            if time() - t >= dt:
                if keyboard['v'].is_holding():
                    CellStorage.left_frame()
                    CellStorage.pause = True
                    no_event = False

                if keyboard['b'].is_holding():
                    CellStorage.right_frame()
                    CellStorage.pause = True
                    no_event = False

                if not CellStorage.pause:
                    CellStorage.new_stage()

                t = time()

            if slow_mode or time() - t_extra >= dt:
                if slow_mode or (no_event and CellStorage.pause):
                    CellStorage.extra_stage()
                else:
                    t_extra = time()

            for cell in fake_cells.keys():
                CellStorage.s_draw(cell[0], cell[1], CellStorage.colors["fake"])

            for cell in CellStorage.values():
                cell.draw()

            i, j = CellStorage.mouse_cell_coord()
            CellStorage.draw_pale(i, j)

            if CellStorage.grid_mode:
                CellStorage.draw_grid()

            save.dis_light()
            eraser.set_color("red") if CellStorage.erase_mode else eraser.set_color("black")
            play_box.set_color("black") if CellStorage.pause else play_box.set_color("red")
            slow_switch.hidden = False if slow_mode else True
            for btn in buttons1:
                btn.blit()
            if hidden_mode == 0:
                blit_text(screen, f' {int(1 / dt) if 1 / dt == int(1 / dt) else 1 / dt} FPS',
                          (play_box.pos()[0] + play_box.width(), play_box.pos()[1] + play_box.height() // 4),
                          pygame.font.SysFont('Courier New', 20))
            pygame.display.update()
        if running_screen == 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                update_key(event, keyboard)

                if event.type == pygame.KEYDOWN:
                    key = get_keyboard_key(event)
                    if key in list('12345'):
                        colors = list(CellStorage.colors.keys())
                        CellStorage.set_color(colors[int(key) - 1])
                        fake_drawing = False
                    elif key == 'g':
                        CellStorage.grid_mode = not CellStorage.grid_mode
                    elif key == '0':
                        CellStorage.set_color('fake')
                        fake_drawing = True
                    elif key == 'h':
                        hidden_mode = (hidden_mode + 1) % 3
                    elif key == 'r':
                        CellStorage.rotate()
                    elif key == 'i' or key == 'esc':
                        s2_inv.action(as_btn=False)
                    elif key == 'F1':
                        s3_info.action(as_btn=False)
                    elif key == 'e':
                        eraser.action(as_btn=False)
                    elif key == 's' and keyboard['ctrl'].is_pressed:
                        save.action(as_btn=False)
                    elif key == 'k':
                        CellStorage.patterns[CellStorage.pattern_index].clear()
                    elif key == 'left':
                        CellStorage.set_prev_figure(s2=True)
                    elif key == 'right':
                        CellStorage.set_next_figure(empty_allow=True, s2=True)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos[0], event.pos[1]
                    if s2_left.collide_point(x, y):
                        CellStorage.set_prev_figure(s2=True)
                    elif s2_right.collide_point(x, y):
                        CellStorage.set_next_figure(empty_allow=True, s2=True)
                    elif to_s1_text.collide_point(x, y) or s2_inv.collide_point(x, y):
                        to_screen(1)
                    elif eraser.collide_point(x, y):
                        CellStorage.erase_mode = not CellStorage.erase_mode
                    elif s3_info.collide_point(x, y):
                        to_screen(3)
                    elif save.collide_point(x, y):
                        save.make_file()
                        save.set_color('red')
                    else:
                        i, j = CellStorage.get_ij(x, y, s2=True)
                        CellStorage.upd_point(i, j, s2=True)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    left_click_moving_time = time()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    left_click_moving_time = 0.0

                if event.type == pygame.MOUSEMOTION:
                    if left_click_moving_time > 0 and time() - left_click_moving_time >= 0.1:
                        CellStorage.upd_point_by_motion(s2=True)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                    CellStorage.resize(2, s2=True)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                    CellStorage.resize(1 / 2, s2=True)
            for btn in buttons2:
                btn.action()
            if running_screen != 2:
                continue
            CellStorage.s_draw(0, 0, CellStorage.colors["gray"], s2=True)
            CellStorage.draw_figure(s2=True)
            to_s1_text.blit()
            s2_inv.set_color("red")
            eraser.set_color("red") if CellStorage.erase_mode else eraser.set_color("black")
            save.dis_light()
            for btn in buttons2:
                btn.blit()
            if CellStorage.grid_mode:
                CellStorage.draw_grid(s2=True)
            pygame.display.flip()
        if running_screen == 3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                update_key(event, keyboard)

                if event.type == pygame.KEYDOWN:
                    key = get_keyboard_key(event)
                    if key == 'i':
                        to_screen(2)
                    elif key == 'F1' or key == 'esc':
                        to_screen(1)
                    elif key == 's' and keyboard['ctrl'].is_pressed:
                        save.launch()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if to_s1_text.collide_point(x, y) or s3_info.collide_point(x, y):
                        screen_quit_3()
                        running_screen = 1
                    elif s2_inv.collide_point(x, y):
                        screen_quit_3()
                        running_screen = 2
                    elif save.collide_point(x, y):
                        save.launch()
            for btn in buttons3:
                btn.action()
            if running_screen != 3:
                continue
            eraser.set_color("red") if CellStorage.erase_mode else eraser.set_color("black")
            to_s1_text.blit()
            save.dis_light()
            s3_info.set_color("red")
            blit_text(screen, s3_info_text, (20, 15), pygame.font.SysFont('Courier New', 24))
            for btn in buttons3:
                btn.blit()
            pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
