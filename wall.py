from turtle import Turtle

layer = [-350, -250, -150, -50, 50, 150, 250, 350]
#layer = [-350, -250, -150, -50, 150, 250, 350]
y_start = 200
layer_thickness = 20
no_layers = 7

class Wall(Turtle):
    def __init__(self):
        super().__init__()
        self.brick_pos = []

    def build_wall(self):
        """Build the wall based on values given above"""
        for round in range(no_layers):
            y_pos = y_start - layer_thickness * round
            #print(y_pos)
            for count, brick in enumerate(layer):
                position = (brick, y_pos)
                self.add_brick(position)
                self.brick_pos.append(position)

    def add_brick(self, position):
        """Add brick to given position"""
        new_brick = Turtle(shape="square")
        new_brick.color("brown")
        new_brick.penup()
        new_brick.shapesize(stretch_wid=0.8, stretch_len=4.8)
        new_brick.goto(position)

    def remove_brick(self, position):
        """Find turtle based on its position and remove it"""
        for brick in self.screen.turtles():
            if brick.pos() == position:
                brick.hideturtle()  # hide the brick
                brick.clear()  # Clear the brick's drawing






