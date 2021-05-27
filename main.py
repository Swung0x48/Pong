import turtle


class Entity(object):
    def __init__(self, x_pos, y_pos):
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.shape("square")
        self.turtle.color("white")
        self.turtle.penup()
        self.turtle.goto(x_pos, y_pos)

    def xcor(self):
        return self.turtle.xcor()

    def ycor(self):
        return self.turtle.ycor()

    def setx(self, x):
        self.turtle.setx(x)

    def sety(self, y):
        self.turtle.sety(y)


class Paddle(Entity):
    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos)
        self.turtle.shapesize(stretch_wid=5, stretch_len=1)
        self.vel = 30

    def up(self):
        self.turtle.sety(self.turtle.ycor() + self.vel)

    def down(self):
        self.turtle.sety(self.turtle.ycor() - self.vel)

    def left_boundary(self):
        return self.xcor() - 5

    def right_boundary(self):
        return self.xcor() + 5


class Ball(Entity):
    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos)
        self.turtle.shapesize(stretch_wid=1, stretch_len=1)
        self.x_vel = -3
        self.y_vel = 3

    def left_boundary(self):
        return self.xcor() - 5

    def right_boundary(self):
        return self.xcor() + 5

    def reset(self):
        self.turtle.goto(0, 0)
        self.x_vel *= -1


class Game:
    def __init__(self, width, height):
        self.window = turtle.Screen()
        self.window.title("Pong")
        self.window.bgcolor("black")
        self.width = width
        self.height = height
        self.window.setup(width=width, height=height)
        self.window.tracer(0)
        paddle_x = width / 2 - width / 16
        self.paddles = [Paddle(-paddle_x, 0), Paddle(paddle_x, 0)]
        self.ball = Ball(0, 0)
        self.scoreboard = Entity(0, 260)
        self.scoreboard.turtle.hideturtle()
        self.scoreboard.turtle.write("L: 0    R: 0", align="center", font=("", 24, ""))

        self.window.listen()
        self.window.onkeypress(self.paddles[0].up, 'w')
        self.window.onkeypress(self.paddles[0].down, 's')
        self.window.onkeypress(self.paddles[1].up, 'Up')
        self.window.onkeypress(self.paddles[1].down, 'Down')

        self.score_L = 0
        self.score_R = 0

    def update(self):
        self.window.update()

        # Move the ball
        self.ball.setx(self.ball.xcor() + self.ball.x_vel)
        self.ball.sety(self.ball.ycor() + self.ball.y_vel)

        # Check border & bounce
        if self.ball.ycor() > self.height / 2 - 10:
            self.ball.sety(self.height / 2 - 10)
            self.ball.y_vel *= -1
        if self.ball.ycor() < -(self.height / 2 - 20):
            self.ball.sety(-(self.height / 2 - 20))
            self.ball.y_vel *= -1
        if self.ball.xcor() > self.width / 2 - 20:
            self.ball.reset()
            self.score_L += 1
            self.scoreboard.turtle.clear()
            self.scoreboard.turtle.write("L: {}    R: {}".format(self.score_L, self.score_R), align="center",
                                         font=("", 24, "normal"))
        if self.ball.xcor() < -(self.width / 2 - 10):
            self.ball.reset()
            self.score_R += 1
            self.scoreboard.turtle.clear()
            self.scoreboard.turtle.write("L: {}    R: {}".format(self.score_L, self.score_R), align="center",
                                         font=("", 24, "normal"))

        # Paddle & ball collision
        # Left Paddle
        if self.ball.left_boundary() < self.paddles[0].right_boundary() and \
            self.ball.right_boundary() > self.paddles[0].left_boundary() \
                and \
                self.paddles[0].ycor() - 40 < self.ball.ycor() < self.paddles[0].ycor() + 40:
            self.ball.setx(self.paddles[0].right_boundary() + 10)
            self.ball.x_vel *= -1

        # Right Paddle
        if self.paddles[1].left_boundary() < self.ball.right_boundary() < self.paddles[1].right_boundary() and \
                self.paddles[1].ycor() - 40 < self.ball.ycor() < self.paddles[1].ycor() + 40:
            self.ball.setx(self.paddles[1].left_boundary() - 10)
            self.ball.x_vel *= -1


if __name__ == '__main__':
    game = Game(800, 600)
    while True:
        game.update()
