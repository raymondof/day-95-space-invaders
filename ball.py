from turtle import Turtle


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("red")
        self.penup()
        self.move_x = 3
        self.move_y = 3

    def move_ball(self):
        new_x = self.xcor() + self.move_x
        new_y = self.ycor() + self.move_y
        self.goto(new_x, new_y)

    def bounce_x(self):
        self.move_x *= -1

    def bounce_y(self):
        self.move_y *= -1

    def paddle_bounce_y(self, position, direction):
        if 10 > position > -10:  # ball has hit middle of the paddle
            self.move_y *= -1  # bounce only in y direction
        elif position < -10 and direction == 0:  # ball is coming from left and hits left side of the paddle
            self.move_y *= -1  # ball is returned to same direction
            self.move_x *= -1
        elif position > 10 and direction == 1:  # ball is coming from right and hits right side of the paddle
            self.move_y *= -1  # ball is returned to same direction
            self.move_x *= -1
        else:  # otherwise the ball is bounced in y direction
            self.move_y *= -1



