import turtle
from turtle import Turtle


class Spaceship(Turtle):
    def __init__(self, coordinates):
        super().__init__()
        self.shape("classic")
        self.color("green")
        self.shapesize(stretch_wid=5, stretch_len=2)
        self.settiltangle(90)
        self.penup()
        self.goto(coordinates)
        self.ammo_pos = []

    def move_left(self):
        new_x = self.xcor() - 20
        if self.xcor() > -350:
            self.goto(new_x, self.ycor())

    def move_right(self):
        new_x = self.xcor() + 20
        if self.xcor() < 350:
            self.goto(new_x, self.ycor())

    def shoot(self):
        ammo = turtle.Turtle()
        ammo.shape("triangle")
        ammo.penup()
        ammo.color("green")
        ammo.left(90)
        ammo.shapesize(stretch_wid=0.2, stretch_len=1)
        ammo.goto(self.xcor(), self.ycor() + 7)

        self.ammo_pos.append(ammo)

    def move_ammo(self):
        for ammo in self.ammo_pos:
            ammo_to_move = ammo
            ammo_to_move.forward(3)

    def remove_ammo(self, position):
        for ammo in self.ammo_pos:
            if ammo.pos() == position:
                ammo.hideturtle()
                ammo.clear()
