import turtle
from turtle import Turtle
FONT = ("Courier", 18, "normal")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.color("green")
        self.hideturtle()
        self.penup()
        self.goto(0, -280)
        self.space_pos = 0
        self.available_ship_positions = []

    def write_score(self):
        self.clear()
        self.setposition(280, -280)
        self.write(f"Score: {self.score}",
                   move=False, align="center", font=FONT)

    def write_instructions(self):
        self.clear()
        self.setposition(0, 0)
        self.write(f"Your task is to destroy aliens as soon as\npossible "
                   f"start the game by pressing ENTER\n"
                   f"Move with arrows and shoot with SPACE",
                   move=False, align="center", font=FONT)

    def game_on_pause(self):
        self.clear()
        self.write(f"Game is on pause\ncontinue by pressing SPACE",
                   move=False, align="center", font=FONT)
        if self.space_pos == 0:
            self.space_pos = 1
            print(f"space {self.space_pos}")
        else:
            self.space_pos = 0
            print(f"space {self.space_pos}")

    def finish(self):
        self.setposition(0, 0)
        self.write(f"You have finished the level with {self.score} points",
                   move=False, align="center", font=FONT)

    def end_game(self):
        self.setposition(0, 0)
        self.write(f"Game over! Better luck next time!",
                   move=False, align="center", font=FONT)

    def update_high_score(self):
        with open("data.txt", mode="w") as data:
            data.write(str(self.best_score))

    def make_line(self):
        line = turtle.Turtle()
        line.hideturtle()
        line.goto(-400, -240)
        line.color("green")
        line.pendown()
        line.forward(800)
        line.penup()

    def available_ships(self, ships):
        ship_x = -360
        ship_y = -260

        for _ in range(ships - 1):
            new_ship = turtle.Turtle()
            new_ship.penup()
            new_ship.goto(ship_x, ship_y)
            new_ship.shapesize(stretch_wid=5, stretch_len=2)
            new_ship.settiltangle(90)
            new_ship.color("green")
            new_ship.shape("classic")
            new_ship.showturtle()
            ship_x += 60

            self.available_ship_positions.append(new_ship)

    def remove_ship(self):
        removable_ship = self.available_ship_positions.pop()
        removable_ship.hideturtle()
        removable_ship.clear()
