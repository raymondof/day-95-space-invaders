import time
import random
import turtle
from turtle import Screen
from spaceship import Spaceship
from obstacle import Obstacle
from scoreboard import Scoreboard
from aliens import Aliens


screen = Screen()
screen.setup(width=800, height=600, startx=550, starty=250)
screen.bgcolor("black")
screen.title("Space Invaders")
# turns turtle animation off, making things appear immediately on the screen
screen.tracer(0)

paddle_start_coordinates = (0, -200)
spaceship = Spaceship(paddle_start_coordinates)

wall = Obstacle()

scoreboard = Scoreboard()
aliens = Aliens()


game_is_on = False


def wait_for_enter():
    turtle.textinput("Next Level", "Press Enter to continue...")
    start_game()


def start_game():
    global game_is_on
    # if not game_is_on:
    game_is_on = True
    wall.build_wall()
    game_loop()


screen.listen()
screen.onkey(fun=start_game, key="Return")

screen.onkey(spaceship.move_left, "Left")
screen.onkey(spaceship.move_right, "Right")
screen.onkey(spaceship.shoot, key="space")
scoreboard.write_instructions()

ufo_ammos = 50  # the smaller the value, the more ammo ufos will shoot start with 50


def game_loop():
    global game_is_on, ufo_ammos
    screen.listen()

    unique_brick = []
    ufo_x_coords = []
    direction = 1
    ships = 3

    scoreboard.make_line()
    scoreboard.available_ships(ships)
    scoreboard.write_score()
    aliens.place_ships()

    while game_is_on:

        screen.update()
        spaceship.move_ammo()
        aliens.move_ammo()

        # Move ufos and change their direction when on edge
        for ufo in aliens.ufos:
            ufo_x_coords.append(ufo.xcor())
            if max(ufo_x_coords) >= 380:
                direction = -1
                ufo_x_coords.clear()
                aliens.move_ufos_lower()
            elif min(ufo_x_coords) <= -380:
                direction = 1
                ufo_x_coords.clear()
                aliens.move_ufos_lower()

            # Aliens shoot when close to players ship
            spaceship_x = spaceship.xcor()
            x_abs_player_ufo = abs(ufo.xcor() - spaceship_x)

            if x_abs_player_ufo <= 100 and random.randint(0, ufo_ammos) == 7:
                aliens.shoot(ufo)
        aliens.move_ufos_sideways(direction)

        # Detect brick collision
        for brick in wall.brick_pos:
            x, y = brick  # bricks coordinates
            if brick not in unique_brick:  # check if brick has already been hit, thus removed

                # For player ammos
                for ammo in spaceship.ammo_pos:
                    # calculate absolute vertical and horizontal distance from ball to brick
                    x_abs_to_ammo = abs(ammo.xcor() - x)
                    y_abs_to_ammo = abs(ammo.ycor() - y)
                    # if both of the aforementioned distances are smaller than the size
                    # of the brick (100 x 20), measured from the middle, the ball has hit the brick
                    if x_abs_to_ammo < 25 and y_abs_to_ammo < 5:
                        unique_brick.append(brick)  # # add the brick to list of unique bricks
                        wall.remove_brick(brick)  # and remove it so that it can't be hit again
                        spaceship.remove_ammo(ammo.pos())
                        spaceship.ammo_pos.remove(ammo)
                        scoreboard.score += 25  # add score
                        scoreboard.write_score()  # write it on the screen

                    # Remove players ammos when they get out of the screen
                    if ammo.ycor() > 300:
                        spaceship.remove_ammo(ammo.pos())
                        spaceship.ammo_pos.remove(ammo)

                # For ufo ammos
                for ufo_ammo in aliens.ammo_pos:
                    # calculate absolute vertical and horizontal distance from ball to brick
                    x_abs_to_ufo_ammo = abs(ufo_ammo.xcor() - x)
                    y_abs_to_ufo_ammo = abs(ufo_ammo.ycor() - y)
                    # if both of the aforementioned distances are smaller than the size
                    # of the brick (100 x 20), measured from the middle, the ball has hit the brick
                    if x_abs_to_ufo_ammo < 25 and y_abs_to_ufo_ammo < 5:
                        unique_brick.append(brick)  # # add the brick to list of unique bricks
                        wall.remove_brick(brick)  # and remove it so that it can't be hit again
                        aliens.remove_ammo(ufo_ammo.pos())
                        aliens.ammo_pos.remove(ufo_ammo)

                    # Remove ufos ammos when they get out of the screen
                    if ufo_ammo.ycor() < -300:
                        aliens.remove_ammo(ufo_ammo.pos())
                        aliens.ammo_pos.remove(ufo_ammo)

        # Detect ammo - ufo collision
        for ufo in aliens.ufos:
            ufo_x, ufo_y = ufo.pos()
            for ammo in spaceship.ammo_pos:
                # calculate absolute vertical and horizontal distance from ammo to ufo
                x_abs_ammo_ufo = abs(ammo.xcor() - ufo_x)
                y_abs_ammo_ufo = abs(ammo.ycor() - ufo_y)
                if x_abs_ammo_ufo < 12 and y_abs_ammo_ufo < 2:
                    aliens.remove_ufo(ufo)
                    spaceship.remove_ammo(ammo.pos())
                    spaceship.ammo_pos.remove(ammo)
                    scoreboard.score += 50  # add score
                    scoreboard.write_score()  # write it on the screen

                    # Detect defeated ufos
                    if len(aliens.ufos) == 0:
                        scoreboard.finish()
                        ufo_ammos -= 5
                        game_is_on = False

                        # Wait for the user to press Enter
                        wait_for_enter()

        # Detect ufo ammo - player collision
        for ammo in aliens.ammo_pos:
            ammo_x, ammo_y = ammo.pos()

            # calculate absolute vertical and horizontal distance from ufo ammo to player
            x_abs_ufo_ammo_player = abs(ammo_x - spaceship.xcor())
            y_abs_ufo_ammo_player = abs(ammo_y - spaceship.ycor())

            if x_abs_ufo_ammo_player < 12 and y_abs_ufo_ammo_player < 2:
                if ships > 1:
                    ships -= 1
                    scoreboard.remove_ship()
                else:
                    scoreboard.end_game()
                    game_is_on = False
                    break

        time.sleep(0.01)


screen.exitonclick()
