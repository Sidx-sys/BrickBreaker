import time
import config as cg


def powerup_movement(GRID, BALL, PADDLE, BALL_LIST, on_screen_powerups, active_powerups):
    for powerup in on_screen_powerups:
        # Check collisions with Walls
        if powerup.x + powerup.v_x >= cg.WIDTH - 1:
            powerup.update_vx(-powerup.v_x)
        elif powerup.x + powerup.v_x < 2:
            powerup.update_vx(-powerup.v_x)

        # Collision with the Paddle
        is_collected = powerup.collected(
            PADDLE.x_start, PADDLE.x_end, PADDLE.y)
        if is_collected:
            for power in active_powerups:
                if power.type == powerup.type:
                    active_powerups.remove(power)
            active_powerups.append(powerup)
            on_screen_powerups.remove(powerup)
            if powerup.sign == 'M':
                powerup.start_effect(BALL_LIST)
            else:
                powerup.start_effect(BALL, PADDLE, GRID)
            powerup.remove_pow(GRID)
        else:
            if not powerup.passed_paddle(PADDLE.y):
                powerup.move(GRID)
            else:
                on_screen_powerups.remove(powerup)
                powerup.remove_pow(GRID)


def powerup_effect(GRID, BALL, PADDLE, active_powerups):
    for powerup in active_powerups:
        if time.time() - powerup.startTime >= cg.POWER_TIME:
            powerup.end_effect(BALL, PADDLE, GRID)
            active_powerups.remove(powerup)
