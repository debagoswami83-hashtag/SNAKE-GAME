import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = COLS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE

#game window
window = tkinter.Tk()   
window.title("Snake Game")
window.resizable(False, False)  

window.mainloop()