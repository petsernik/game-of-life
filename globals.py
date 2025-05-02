from dataclasses import dataclass
import pygame
import os

from get_building_path import get_building_path


class Global:
    hidden_mode = None
    dt_ui = None
    t_ui = None
    use_music = False
    dt = 1 / 4
    dt_music = 1 / 2
    RESOURCES_PATH = 'resources'
    SAVES_PATH = 'saves'
    GALLERY_PATH = 'gallery'

    with open(get_building_path(os.path.join(RESOURCES_PATH, 'info.txt')), 'r', encoding='utf-8') as f:
        INFO_TEXT = f.read()
    fake_cells = {}



