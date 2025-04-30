import pygame
from time import time
from lib.keyboard import update_key, get_keyboard_key
from lib.rect import blit_text
from globals import Global, UIContext
from lib.cell import CellStorage


def update_screen(context: UIContext) -> None:
    if context.running_screen == 1:
        update_screen1(context)
    elif context.running_screen == 2:
        update_screen2(context)
    else:
        raise "can't handle running screen"


def update_screen1(context: UIContext):
    screen = CellStorage.screen
    screen.fill(CellStorage.colors["white"])
    no_event = True
    for event in pygame.event.get():
        no_event = False
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            context.running = False

        update_key(event, context.keyboard)

        if event.type == pygame.KEYDOWN:
            key = get_keyboard_key(event)
            if key in list('12345'):
                CellStorage.set_color(context.colors[int(key) - 1])
                context.fake_drawing = False
            elif key == '0':
                CellStorage.set_color('fake')
                context.fake_drawing = True
            elif key == 'w':
                context.slow_mode = not context.slow_mode
            elif key == 'r':
                CellStorage.rotate()
            elif key == 't':
                CellStorage.update_transparency_mode()
            elif key == 'i':
                context.s2_inv.action(as_btn=False)
            elif key == 'h':
                Global.hidden_mode = (Global.hidden_mode + 1) % 3
            elif key == 'esc':
                context.running = False
            elif key == 'F1':
                context.info.action(as_btn=False)
            elif key == 'e':
                context.eraser.action(as_btn=False)
            elif key == 'p':
                CellStorage.update_draw_mode()
            elif key == 'g':
                CellStorage.grid_mode = not CellStorage.grid_mode
            elif key == 'space':
                context.play_box.action(as_btn=False)
            elif key == 'left':
                Global.dt = min(2 * Global.dt, 4)
            elif key == 'right':
                Global.dt = max(Global.dt / 2, 1 / 2 ** 7)
            elif key == 'v':
                CellStorage.left_frame()
                context.keyboard['v'].game_pause = context.keyboard['b'].game_pause if context.keyboard[
                    'b'].is_pressed else CellStorage.pause
            elif key == 'b':
                CellStorage.right_frame()
                context.keyboard['b'].game_pause = context.keyboard['v'].game_pause if context.keyboard[
                    'v'].is_pressed else CellStorage.pause

        if context.keyboard['ctrl'].is_pressed:
            if context.keyboard['k'].is_pressed:
                Global.fake_cells.clear()
            if context.keyboard['s'].is_pressed:
                context.save.launch()
            if context.keyboard['z'].is_pressed:
                context.save.upd_by_file(full=False)
        elif context.keyboard['k'].is_pressed:
            CellStorage.clear()

        if event.type == pygame.KEYUP and event.key == pygame.K_v:
            CellStorage.pause = context.keyboard['v'].game_pause
        if event.type == pygame.KEYUP and event.key == pygame.K_b:
            CellStorage.pause = context.keyboard['b'].game_pause

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            CellStorage.set_next_figure()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            CellStorage.set_prev_figure()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            x, y = event.pos
            if context.print_info and context.info_rect.collide_point(x, y):
                context.shift_info_text_y += 10
            else:
                CellStorage.resize(2)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            x, y = event.pos
            if context.print_info and context.info_rect.collide_point(x, y):
                context.shift_info_text_y -= 10
            else:
                CellStorage.resize(1 / 2)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            CellStorage.update_draw_mode()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            __break = False
            for btn in context.buttons1:
                if btn.collide_point(x, y):
                    btn.active = True
                    __break = True
            i, j = CellStorage.get_ij(x, y)
            if not __break:
                if context.fake_drawing:
                    if CellStorage.erase_mode:
                        CellStorage.fake_del_by_figure(i, j, Global.fake_cells)
                    elif CellStorage.draw_mode == CellStorage.point_mode:
                        CellStorage.fake_create_with_del(i, j, Global.fake_cells)
                    else:
                        CellStorage.fake_create(i, j, Global.fake_cells)
                elif CellStorage.erase_mode:
                    CellStorage.del_by_figure(i, j)
                elif CellStorage.draw_mode == CellStorage.point_mode:
                    CellStorage.create_with_del(i, j)
                else:
                    CellStorage.create(i, j)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            context.left_click_moving_time = time()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            context.left_click_moving_time = 0.0
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            context.right_click_moving = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            context.right_click_moving = False

        if event.type == pygame.MOUSEMOTION:
            if context.left_click_moving_time > 0 and time() - context.left_click_moving_time >= 0.1:
                i, j = CellStorage.mouse_cell_coord()
                if not context.fake_drawing:
                    if CellStorage.erase_mode:
                        CellStorage.del_by_figure(i, j)
                    else:
                        CellStorage.create(i, j)
                else:
                    if not CellStorage.erase_mode:
                        CellStorage.fake_create(i, j, Global.fake_cells)
                    else:
                        CellStorage.fake_del_by_figure(i, j, Global.fake_cells)
            if context.right_click_moving:
                CellStorage.x += event.rel[0]
                CellStorage.y += event.rel[1]

    for btn in context.buttons1:
        btn.action()

    if Global.hidden_mode == 0:
        for b in context.buttons1:
            b.hidden = False
    elif Global.hidden_mode == 1:
        context.play_box.hidden = True
    elif Global.hidden_mode == 2:
        for b in context.buttons1:
            b.hidden = True

    if time() - Global.t >= Global.dt:
        if context.keyboard['v'].is_holding():
            CellStorage.left_frame()
            CellStorage.pause = True
            no_event = False
        if context.keyboard['b'].is_holding():
            CellStorage.right_frame()
            CellStorage.pause = True
            no_event = False
        if not CellStorage.pause:
            CellStorage.new_stage()
        Global.t = time()

    if context.slow_mode or time() - Global.t >= Global.dt:
        if context.slow_mode or (no_event and CellStorage.pause):
            CellStorage.extra_stage()
        else:
            Global.t = time()

    for cell in Global.fake_cells.keys():
        CellStorage.s_draw(cell[0], cell[1], CellStorage.colors['fake'])
    for cell in CellStorage.values():
        cell.draw()
    i, j = CellStorage.mouse_cell_coord()
    CellStorage.draw_pale(i, j)
    if CellStorage.grid_mode:
        CellStorage.draw_grid()

    if context.print_info:
        screen.blit(context.surf, (context.play_box.pos()[0], context.play_box.pos()[1] + context.play_box.height()),
                    (0, context.shift_info_text_y, context.surf.get_width(), context.surf.get_height()))

    context.save.dis_light()
    context.s2_inv.set_color("black")
    context.eraser.set_color("red" if CellStorage.erase_mode else "black")
    context.play_box.set_color("black" if CellStorage.pause else "red")
    context.info.set_color("red" if context.print_info else "black")
    context.slow_switch.hidden = not context.slow_mode

    for b in context.buttons1:
        b.blit()

    if Global.hidden_mode == 0:
        blit_text(screen, f'{int(1 / Global.dt) if 1 / Global.dt == int(1 / Global.dt) else 1 / Global.dt} FPS', (
            context.play_box.pos()[0] + context.play_box.width(),
            context.play_box.pos()[1] + context.play_box.height() // 4), pygame.font.SysFont('Courier New', 20))

    pygame.display.update()


def update_screen2(context: UIContext):
    screen = CellStorage.screen
    screen.fill(CellStorage.colors["white"])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            context.running = False

        update_key(event, context.keyboard)

        if event.type == pygame.KEYDOWN:
            key = get_keyboard_key(event)
            if key in list('12345'):
                CellStorage.set_color(context.colors[int(key) - 1])
                context.fake_drawing = False
            elif key == 'g':
                CellStorage.grid_mode = not CellStorage.grid_mode
            elif key == '0':
                CellStorage.set_color('fake')
                context.fake_drawing = True
            elif key == 'h':
                Global.hidden_mode = (Global.hidden_mode + 1) % 3
            elif key == 'r':
                CellStorage.rotate()
            elif key in ('i', 'esc'):
                context.s2_inv.action(as_btn=False)
            elif key == 'F1':
                context.info.action(as_btn=False)
            elif key == 'e':
                context.eraser.action(as_btn=False)
            elif key == 's' and context.keyboard['ctrl'].is_pressed:
                context.save.action(as_btn=False)
            elif key == 'k':
                CellStorage.patterns[CellStorage.pattern_index].clear()
            elif key == 'left':
                CellStorage.set_prev_figure(s2=True)
            elif key == 'right':
                CellStorage.set_next_figure(empty_allow=True, s2=True)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if context.s2_left.collide_point(x, y):
                CellStorage.set_prev_figure(s2=True)
            elif context.s2_right.collide_point(x, y):
                CellStorage.set_next_figure(empty_allow=True, s2=True)
            elif context.to_s1_text.collide_point(x, y) or context.s2_inv.collide_point(x, y):
                context.s2_inv.active = True
            elif context.eraser.collide_point(x, y):
                context.eraser.active = True
            elif context.info.collide_point(x, y):
                context.info.active = True
            elif context.save.collide_point(x, y):
                context.save.launch()
            else:
                i, j = CellStorage.get_ij(x, y, s2=True)
                CellStorage.upd_point(i, j, s2=True)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            context.left_click_moving_time = time()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            context.left_click_moving_time = 0.0

        if event.type == pygame.MOUSEMOTION:
            if context.left_click_moving_time > 0 and time() - context.left_click_moving_time >= 0.1:
                CellStorage.upd_point_by_motion(s2=True)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            x, y = event.pos
            if context.print_info and context.info_rect.collide_point(x, y):
                context.shift_info_text_y += 10
            else:
                CellStorage.resize(2, s2=True)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            x, y = event.pos
            if context.print_info and context.info_rect.collide_point(x, y):
                context.shift_info_text_y -= 10
            else:
                CellStorage.resize(1 / 2, s2=True)

    for btn in context.buttons2:
        btn.action()

    CellStorage.s_draw(0, 0, CellStorage.colors['gray'], s2=True)
    CellStorage.draw_figure(s2=True)
    context.to_s1_text.blit()
    context.s2_inv.set_color("red")
    context.eraser.set_color("red" if CellStorage.erase_mode else "black")
    context.info.set_color("red" if context.print_info else "black")
    context.save.dis_light()
    for btn in context.buttons2:
        btn.blit()
    if CellStorage.grid_mode:
        CellStorage.draw_grid(s2=True)
    if context.print_info:
        screen.blit(context.surf, (context.play_box.pos()[0], context.play_box.pos()[1] + context.play_box.height()),
                    (0, context.shift_info_text_y, context.surf.get_width(), context.surf.get_height()))
    pygame.display.flip()


def screen_quit_1(context: UIContext):
    context.left_click_moving_time, context.right_click_moving, CellStorage.erase_mode = 0.0, False, False
    for _btn in context.buttons1:
        _btn.hidden = False


def screen_quit_2(context: UIContext):
    CellStorage.update_figures()
    screen_quit_1(context)


# def hide_buttons():
#     if Global.hidden_mode == 0:
#         for _btn in buttons1:
#             _btn.hidden = False
#     elif Global.hidden_mode == 1:
#         play_box.hidden = True
#     elif Global.hidden_mode == 2:
#         for _btn in buttons1:
#             _btn.hidden = True

def to_screen(sc: int, context: UIContext):
    if sc == 1:
        CellStorage.update_grid()
    elif sc == 2:
        CellStorage.update_grid(s2=True)

    if context.running_screen == sc:
        if sc == 2:
            screen_quit_2(context)
        CellStorage.update_grid()
        context.running_screen = 1
        CellStorage.enter_s1()
        return
    elif context.running_screen == 1:
        screen_quit_1(context)
    elif context.running_screen == 2:
        screen_quit_2(context)
    context.running_screen = sc

    if sc == 1:
        CellStorage.enter_s1()
    elif sc == 2:
        CellStorage.enter_s2()
