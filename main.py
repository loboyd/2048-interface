#!/usr/bin/env python3

import time
from PIL import Image, ImageDraw

import pynput
import mss
import numpy as np

ROWS = [305, 420, 542, 667]
COLS = [90, 214, 333, 454]

TILES = {
    (205, 193, 180): 0,
    (238, 228, 218): 1,
    (237, 224, 200): 2
}

NO_OF_TILES = 3

class GameController():
    def __init__(self):
        self.mouse_ctrl    = pynput.mouse.Controller()
        self.keyboard_ctrl = pynput.keyboard.Controller()

    def focus(self):
        # Set pointer position
        self.mouse_ctrl.position = (759, 762)

        # Press and release
        self.mouse_ctrl.press(pynput.mouse.Button.left)
        self.mouse_ctrl.release(pynput.mouse.Button.left)

        time.sleep(0.02) # maybe make this value smaller

    def click(self, position):
        """position is a tuple"""
        self.mouse_ctrl.position = position
        self.mouse_ctrl.press(pynput.mouse.Button.left)
        self.mouse_ctrl.release(pynput.mouse.Button.left)

    def up(self):
        self.keyboard_ctrl.press(pynput.keyboard.Key.up)
        self.keyboard_ctrl.release(pynput.keyboard.Key.up)

    def down(self):
        self.keyboard_ctrl.press(pynput.keyboard.Key.down)
        self.keyboard_ctrl.release(pynput.keyboard.Key.down)

    def left(self):
        self.keyboard_ctrl.press(pynput.keyboard.Key.left)
        self.keyboard_ctrl.release(pynput.keyboard.Key.left)

    def right(self):
        self.keyboard_ctrl.press(pynput.keyboard.Key.right)
        self.keyboard_ctrl.release(pynput.keyboard.Key.right)


def read_board(no_of_tiles):
    monitor = {'left': 200, 'top': 200, 'width': 550, 'height': 725}

    board = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    with mss.mss() as sct:
        sct_img = sct.grab(monitor)

        im = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        data = np.asarray(im)

        #draw = ImageDraw.Draw(im)

        for r, row in enumerate(ROWS):
            for c, col in enumerate(COLS):
                # draw some circles
                #draw.ellipse((col, row, col+10, row+10), fill=(0, 255, 0),
                    #outline=(0, 0, 0))

                # determine tile value from pixel RGB data
                pixel = tuple(data[row, col])
                if pixel not in TILES:
                    TILES[pixel] = no_of_tiles
                    no_of_tiles += 1

                board[r][c] = TILES[pixel]

    return board

def print_board(board):
    """Print board in a nice way"""
    for row in board:
        print(' '.join([str(2**x if x else 0) for x in row]))

gc = GameController()
gc.focus()

board = read_board(NO_OF_TILES)
print_board(board)


""" notes

(759, 762) point in the 2048 Firefox window

[205 193 180] 2**0 (empty)
[238 228 218] 2**1
[237 224 200] 2**2

"""

