import time
import random
from turtle import Screen
from spaceship import Spaceship
from ball import Ball
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

# ball = Ball()
wall = Obstacle()
wall.build_wall()
scoreboard = Scoreboard()
aliens = Aliens()

game_is_on = False
is_paused = False


def start_or_pause_game():
    global game_is_on, is_paused
    if not game_is_on:
        game_is_on = True
        game_loop()
    else:
        is_paused = not is_paused

screen.listen()
screen.onkey(spaceship.move_left, "Left")
screen.onkey(spaceship.move_right, "Right")

screen.onkey(fun=start_or_pause_game, key="Return")
screen.onkey(spaceship.shoot, key="space")
scoreboard.write_instructions()

ships = 3
unique_brick = []
balls_2_last_x = []
ufo_x_coords = []
direction = 1


def game_loop():
    global ships, ball, direction
    #TODO: integrate pause functionality
    scoreboard.make_line()
    scoreboard.available_ships(ships)
    scoreboard.write_score()
    aliens.place_ships()
    while game_is_on:
        # if scoreboard.space_pos == 0:
        #     game_is_on = True
        # elif scoreboard.space_pos == 1:
        #     game_is_on = False

        screen.update()
        # ball.move_ball()
        spaceship.move_ammo()
        aliens.move_ammo()

        # Move ufos and change their direction when on edge
        for ufo in aliens.ufos:
            ufo_x_coords.append(ufo.xcor())
            if max(ufo_x_coords) >= 380:
                direction = -1
                ufo_x_coords.clear()
            elif min(ufo_x_coords) <= -380:
                direction = 1
                ufo_x_coords.clear()

            # Aliens shoot when close to players ship
            spaceship_x = spaceship.xcor()
            x_abs_player_ufo = abs(ufo.xcor() - spaceship_x)

            if x_abs_player_ufo <= 100 and random.randint(0, 20) == 7:
                aliens.shoot(ufo)
        aliens.move_ufos(direction)



        #aliens.shoot()

        # # Detect floor "collision"
        # if ball.ycor() < -290:
        #     ships -= 1
        #     ball.hideturtle()
        #     ball.clear()
        #     if ships > 0:
        #         ball = Ball()
        #         scoreboard.remove_ship()
        #     else:
        #         scoreboard.end_game()
        #         break

        # # Detect roof collision
        # if ball.ycor() > 290:
        #     # ball.bounce_y()
        #     scoreboard.finish()
        #     break

        # # Detect paddle collision
        # if ball.ycor() < -230 and ball.distance(spaceship) < 50:
        #     # Determine the ball trajectory
        #     if balls_2_last_x[0] < balls_2_last_x[1]:
        #         direction = 0  # ball is coming from left to right
        #     else:
        #         direction = 1  # ball is coming from right to left
        #     # calculate balls relative position to the paddle
        #     # negative value means on the left and positive on the right
        #     paddle_ball_x = ball.xcor() - spaceship.xcor()
        #     ball.paddle_bounce_y(position=paddle_ball_x, direction=direction)

        # Detect brick collision
        for brick in wall.brick_pos:
            x, y = brick  # bricks coordinates
            if brick not in unique_brick:  # check if brick has already been hit, thus removed
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

        time.sleep(0.01)


screen.exitonclick()
