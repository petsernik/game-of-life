from dataclasses import dataclass

import pygame

from lib.rect import Button, Text, Rect, SaveBox


@dataclass
class UIContext:
    running: bool
    running_screen: int
    keyboard: dict
    shift_info_text_y: int
    buttons1: list
    buttons2: list
    play_box: Button
    eraser: Button
    music_switch: Button
    slow_switch: Button
    info: Button
    save: SaveBox
    s2_inv: Button
    s2_left: Button
    s2_right: Button
    to_s1_text: Text
    surf: pygame.Surface
    info_rect: Rect
    colors: list
    font: pygame.font.Font
    print_info: bool = False
    fake_drawing: bool = False
    left_click_moving_time: float = 0.0
    right_click_moving: bool = False
    slow_mode: bool = False
