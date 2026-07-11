import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = COLS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
#game window
window = tkinter.Tk()   
window.title("Snake Game")
window.resizable(False, False)  

canvas=tkinter.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black" , borderwidth=0, highlightthickness=0  )
canvas.pack()
window.update()

#centre the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))

#format "(w)x(h)+(x)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#initialize game
snake_game = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)  # single tile, snake's head
food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)  # single tile, food
snake_game_body = []  # list to hold the snake's body segments
velocityX = 0
velocityY = 0

def change_direction(event):
    global velocityX, velocityY

    # Map arrow keys to velocity
    if event.keysym == "Up" and velocityY != 1:  # Prevent reversing direction
        velocityX = 0
        velocityY = -1
    elif event.keysym == "Down" and velocityY != -1:  # Prevent reversing direction
        velocityX = 0
        velocityY = 1
    elif event.keysym == "Left" and velocityX != 1:  # Prevent reversing direction
        velocityX = -1
        velocityY = 0
    elif event.keysym == "Right" and velocityX != -1:  # Prevent reversing direction
        velocityX = 1
        velocityY = 0


def move():
    global snake_game, snake_game_body, food, velocityX, velocityY

    # move head
    snake_game.x += velocityX * TILE_SIZE
    snake_game.y += velocityY * TILE_SIZE

    # Keep snake inside the window (wrap around)
    snake_game.x %= WINDOW_WIDTH
    snake_game.y %= WINDOW_HEIGHT

    # collision with food
    if snake_game.x == food.x and snake_game.y == food.y:
        snake_game_body.append(Tile(snake_game.x, snake_game.y))  # add new segment to the snake's body
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE


def draw():
    global snake_game, food

    move()

    canvas.delete("all")  # clear canvas

    # draw snake
    canvas.create_rectangle(
        snake_game.x,
        snake_game.y,
        snake_game.x + TILE_SIZE,
        snake_game.y + TILE_SIZE,
        fill="lime green",
    )

    # draw food
    canvas.create_rectangle(
        food.x,
        food.y,
        food.x + TILE_SIZE,
        food.y + TILE_SIZE,
        fill="red",
    )
    for tile in snake_game_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="lime green")

    window.after(100, draw)  # 100ms=1/10 second, 10 frames/second


draw()

# bind key presses to change direction
window.bind('<Key>', change_direction)

window.mainloop()