import pygame
import os
import sys
from screeninfo import get_monitors
from time import time

from globals import Global, UIContext
from lib.screens import update_screen, to_screen

from lib.cell import CellStorage
from lib.keyboard import KeyboardKey
from lib.rect import fill, Button, Text, blit_text, Rect, SaveBox


def get_building_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)


def get_img(str_path, k=None, size=None, color=None, can_be_less_size=False):
    img = pygame.image.load(str_path)
    if k:
        img = pygame.transform.scale(img, (img.get_width() * k, img.get_height() * k))
    if size:
        w, h = (min(img.get_width(), size[0]), min(img.get_height(), size[1])) if can_be_less_size else size
        img = pygame.transform.scale(img, (w, h))
    if color:
        fill(img, color)
    return img


def main():
    pygame.init()
    pygame.display.set_caption('Conway\'s game of life')
    monitor = get_monitors()[0]
    width, height = monitor.width, monitor.height
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

    # Initialize core components
    CellStorage.screen = screen
    CellStorage.update_grid()
    CellStorage.x = CellStorage.x2 = (width - CellStorage.size) // 2
    CellStorage.y = CellStorage.y2 = (height - CellStorage.size) // 2

    # Game state initialization
    Global.t, Global.dt = time(), 1 / 4
    Global.fake_cells = {}
    Global.hidden_mode = 0
    Global.use_music = False
    Global.t_music, Global.dt_music = time(), 1 / 2

    __len__icon__ = min(50 * width // 1920, 50 * height // 1080)
    __size__icon__ = (__len__icon__, __len__icon__)
    __doubled__icon__ = (lambda xy: (2 * xy[0], 2 * xy[1]))(__size__icon__)

    # UI Elements
    def create_button(img_name, size=__size__icon__):
        return Button(get_img(
            get_building_path(f'{Global.RESOURCES_PATH}/{img_name}'),
            size=size
        ))

    # Screen 1 elements
    s2_inv = create_button('i.png')
    eraser = create_button('eraser.png')
    info = create_button('info.png', size=__size__icon__)
    play_box = create_button('play.png')
    slow_switch = create_button('turtle.png')
    save = SaveBox('__parameters__', get_img(
        get_building_path(f'{Global.RESOURCES_PATH}/save.png'),
        size=__size__icon__
    ))

    # Position elements
    right_height = 12
    right_x = width - 10
    play_box.upd_pos(10, right_height)
    slow_switch.upd_pos(10, play_box.pos()[1] + play_box.height())
    for btn in [s2_inv, eraser, info]:
        right_x -= btn.width() + 5
        btn.upd_pos(right_x, right_height)
    save.upd_rect(info.pos()[0] - info.width() - 5, right_height, info.width(), info.height())
    save.upd_by_file()

    # Screen 2 elements
    s2_left = create_button('left.png', __doubled__icon__)
    s2_right = create_button('right.png', __doubled__icon__)
    s2_left.upd_pos(10, (height - s2_left.height()) // 2)
    s2_right.upd_pos(width - s2_right.width() - 10, (height - s2_left.height()) // 2)

    # Text elements
    font = pygame.font.Font(None, 48)
    to_s1_text = Text(font.render('Return to the field', True, "black"))
    to_s1_text.upd_pos((width - to_s1_text.width()) // 2 - 10, height - 2 * to_s1_text.height())

    for root, dirs, files in os.walk(Global.GALLERY_PATH):
        for file in files:
            if file.endswith('.png'):
                CellStorage.add_art_by_png(get_img(
                    os.path.join(root, file),
                    size=list(map(lambda _: 2 * _, __size__icon__)),
                    can_be_less_size=True
                ))

    CellStorage.game_pause = CellStorage.pause

    CellStorage.update_figures()
    CellStorage.update_arts()
    CellStorage.update_grid()

    surf = pygame.Surface((3 * width // 10, 3 * height))
    surf.fill(CellStorage.colors["white"])
    blit_text(surf, Global.INFO_TEXT, (0, 0), pygame.font.SysFont('Courier New', 22))

    info_rect = Rect((0, 0, surf.get_width(), height))

    context = UIContext(
        running=True,
        running_screen=1,
        keyboard=dict([(key, KeyboardKey()) for key in KeyboardKey.all_keys()]),
        shift_info_text_y=0,
        buttons1=[s2_inv, eraser, info, save, play_box, slow_switch],
        buttons2=[s2_left, s2_right, s2_inv, eraser, info, save],
        play_box=play_box,
        eraser=eraser,
        slow_switch=slow_switch,
        info=info,
        save=save,
        s2_inv=s2_inv,
        s2_left=s2_left,
        s2_right=s2_right,
        to_s1_text=to_s1_text,
        surf=surf,
        info_rect=info_rect,
        colors=list(CellStorage.colors.keys()),
        font=font
    )

    # Actions depend on context, so initializing after context
    s2_left.set_action(CellStorage.set_prev_figure)
    s2_right.set_action(CellStorage.set_next_figure)
    s2_inv.set_action(lambda: to_screen(2, context))
    save.set_action(save.launch)
    info.set_action(lambda: setattr(context, 'print_info', not context.print_info))
    eraser.set_action(lambda: setattr(CellStorage, 'erase_mode', not CellStorage.erase_mode))
    play_box.set_action(lambda: setattr(CellStorage, 'pause', not CellStorage.pause))
    slow_switch.set_action(lambda: setattr(context, 'slow_mode', not context.slow_mode))

    slow_switch.set_color('red')

    while context.running:
        update_screen(context)

    pygame.quit()


if __name__ == '__main__':
    main()
