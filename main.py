import tkinter as tk
import random

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 600
PADDLE_Y = 550
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 10
BALL_RADIUS = 10

BRICK_GAP = 5
BRICK_WIDTH = (CANVAS_WIDTH - BRICK_GAP * 9) / 10
BRICK_HEIGHT = 15

BRICK_COLORS = ['red', 'orange', 'yellow', 'green', 'blue']


class BreakoutGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Breakout")
        self.canvas = tk.Canvas(self.root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
        self.canvas.pack()
        self.level = 1

        self.paddle = self.create_paddle()
        self.ball = self.create_ball()
        self.bricks = self.create_bricks()

        self.root.bind("<Left>", lambda event: self.move_paddle_left())
        self.root.bind("<Right>", lambda event: self.move_paddle_right())
        self.root.bind("<KeyPress-s>", lambda event: self.start_game())

    def create_paddle(self):
        paddle_x = CANVAS_WIDTH / 2 - PADDLE_WIDTH / 2
        paddle_y = PADDLE_Y
        paddle = self.canvas.create_rectangle(paddle_x, paddle_y, paddle_x + PADDLE_WIDTH, paddle_y + PADDLE_HEIGHT,
                                              fill="white")
        return paddle

    def create_ball(self):
        ball_x = CANVAS_WIDTH / 2
        ball_y = CANVAS_HEIGHT / 2
        ball = self.canvas.create_oval(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, ball_x + BALL_RADIUS,
                                       ball_y + BALL_RADIUS, fill="white")
        ball_dx = random.choice([-2, 2])
        ball_dy = -2
        return ball, ball_dx, ball_dy

    def create_bricks(self):
        bricks = []
        for row in range(5):
            for col in range(10):
                brick_x = (BRICK_WIDTH + BRICK_GAP) * col
                brick_y = (BRICK_HEIGHT + BRICK_GAP) * row + 50
                brick_color = random.choice(BRICK_COLORS)
                brick = self.canvas.create_rectangle(brick_x, brick_y, brick_x + BRICK_WIDTH, brick_y + BRICK_HEIGHT,
                                                     fill=brick_color, outline="")
                bricks.append(brick)
        return bricks

    def move_paddle_left(self):
        paddle_coords = self.canvas.coords(self.paddle)
        if paddle_coords[0] > 0:
            self.canvas.move(self.paddle, -10, 0)

    def move_paddle_right(self):
        paddle_coords = self.canvas.coords(self.paddle)
        if paddle_coords[2] < CANVAS_WIDTH:
            self.canvas.move(self.paddle, 10, 0)

    def move_ball(self):
        self.canvas.move(self.ball[0], self.ball[1], self.ball[2])
        ball_coords = self.canvas.coords(self.ball[0])

        if ball_coords[0] <= 0 or ball_coords[2] >= CANVAS_WIDTH:
            self.ball = (self.ball[0], -self.ball[1], self.ball[2])
        if ball_coords[1] <= 0 or ball_coords[3] >= CANVAS_HEIGHT:
            self.ball = (self.ball[0], self.ball[1], -self.ball[2])

        if self.check_collision():
            self.ball = (self.ball[0], self.ball[1], -self.ball[2])

        if ball_coords[3] >= CANVAS_HEIGHT:
            self.game_over()
            return

        self.root.after(10, self.move_ball)

    def check_collision(self):
        ball_coords = self.canvas.coords(self.ball[0])
        paddle_coords = self.canvas.coords(self.paddle)

        if ball_coords[2] >= paddle_coords[0] and ball_coords[0] <= paddle_coords[2] and ball_coords[3] >= \
                paddle_coords[1]:
            return True

        brick_collisions = self.canvas.find_overlapping(*ball_coords)
        if brick_collisions and brick_collisions[0] in self.bricks:
            self.canvas.delete(brick_collisions[0])
            self.bricks.remove(brick_collisions[0])
            return True

        return False

    def start_game(self):
        self.canvas.delete("all")
        self.paddle = self.create_paddle()
        self.ball = self.create_ball()
        self.bricks = self.create_bricks()
        self.move_ball()
        self.root.mainloop()

    def game_over(self):
        self.canvas.create_text(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, text="Game Over", fill="white",
                                font=("Helvetica", 24), anchor=tk.CENTER)

    def restart_game(self):
        self.level += 1
        self.canvas.delete("all")
        self.paddle = self.create_paddle()
        self.ball = self.create_ball()
        self.bricks = self.create_bricks()
        self.move_ball()


if __name__ == '__main__':
    game = BreakoutGame()
    game.start_game()
