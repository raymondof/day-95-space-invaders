from turtle import Turtle
import turtle

initial_x_coords = [-350, -310, -270, -230, -190, -150, -110, -70]
y_start = 250
layer_thickness = 25
no_layers = 3


class Aliens(Turtle):
    def __init__(self):
        super().__init__()
        self.ufos = []
        self.ammo_pos = []

    def place_ships(self):
        """Place spaceships on the screen based on the values given above"""
        for layer in range(no_layers):
            y_pos = y_start - layer_thickness * layer
            for count, ufo in enumerate(initial_x_coords):
                position = (ufo, y_pos)
                self.add_ufo(position)

    def add_ufo(self, position):
        """Place alien in given position"""
        new_ufo = Turtle(shape="classic")
        new_ufo.color("red")
        new_ufo.penup()
        new_ufo.shapesize(stretch_wid=3, stretch_len=2)
        new_ufo.right(90)
        new_ufo.goto(position)

        self.ufos.append(new_ufo)

    def remove_ufo(self, ufo):
        """Find ufo based on its position and remove it"""
        self.ufos.remove(ufo)
        ufo.hideturtle()
        ufo.clear()
        print(f"ufoja jäljellä {len(self.ufos)}")

    def move_ufos_sideways(self, direction):
        for ufo in self.ufos:
            ufo_to_move = ufo
            current_x = ufo_to_move.xcor()
            new_x = current_x + 2 * direction
            current_y = ufo_to_move.ycor()
            ufo_to_move.goto(new_x, current_y)

    def move_ufos_lower(self):
        for ufo in self.ufos:
            # current_y = ufo.ycor()
            # new_y = current_y - 5
            ufo.forward(5)

    def shoot(self, ufo):
        ufo_x = ufo.xcor()
        ufo_y = ufo.ycor()
        ammo = turtle.Turtle()
        ammo.shape("triangle")
        ammo.penup()
        ammo.color("red")
        ammo.right(90)
        ammo.shapesize(stretch_wid=0.2, stretch_len=1)
        ammo.goto(ufo_x, ufo_y - 7)

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
