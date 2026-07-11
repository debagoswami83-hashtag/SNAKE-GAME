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

canvas = tkinter.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black", borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()
window.focus_set()

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
grow = 0  # number of segments to grow
velocityX = 0
velocityY = 0
game_over = False
score = 0

def change_direction(event):
    global velocityX, velocityY, grow, game_over, score
    if game_over:
        return  # Ignore input if the game is over

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
    global snake_game, snake_game_body, food, velocityX, velocityY, grow, game_over, score

    if game_over:
        return  # Stop moving if the game is over

    if velocityX == 0 and velocityY == 0:
        return  # Do not move until a direction is chosen

    # remember previous head position
    prev_x = snake_game.x
    prev_y = snake_game.y

    # move head
    snake_game.x += velocityX * TILE_SIZE
    snake_game.y += velocityY * TILE_SIZE

    # boundary collision (game over if touching edge)
    if (snake_game.x < 0 or snake_game.x + TILE_SIZE > WINDOW_WIDTH or
            snake_game.y < 0 or snake_game.y + TILE_SIZE > WINDOW_HEIGHT):
        game_over = True
        return

    # self-collision
    for tile in snake_game_body:
        if snake_game.x == tile.x and snake_game.y == tile.y:
            game_over = True
            return

        # collision with food (after moving)
    if snake_game.x == food.x and snake_game.y == food.y:
        grow += 1
        score += 1
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE

        # avoid spawning food on the snake's body
        while any(tile.x == food.x and tile.y == food.y for tile in snake_game_body) or (food.x == snake_game.x and food.y == snake_game.y):
            food.x = random.randint(0, COLS - 1) * TILE_SIZE
            food.y = random.randint(0, ROWS - 1) * TILE_SIZE

    # update body to follow the head
    snake_game_body.insert(0, Tile(prev_x, prev_y))

    if grow > 0:
        grow -= 1
    elif len(snake_game_body) > 0:
        snake_game_body.pop()


def draw():
    global snake_game, food, score

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

    if game_over:
        canvas.create_text(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            text=f"Game Over! Score: {score}",
            font="Arial 20 bold",
            fill="white",
        )
    else:
        canvas.create_text(
            30,
            20,
            font="Arial 12 bold",
            fill="white",
            text=f"Score: {score}",
        )
        window.after(140, draw)  # 140ms=~7 frames/second, slower movement


draw()

# bind key presses to change direction
window.bind('<Key>', change_direction)

window.mainloop()