import config as cg
import time
import random
import math
from Assets import Ball


class PowerUp():
    def __init__(self, x, y, v_x):
        self.x = x
        self.counts = y
        self.gravity = 0.2
        self.speed = -0.5
        self.y = y
        self.onScreen = True
        self.active = False
        self.startTime = -1
        self.v_x = v_x
        self.v_y = -0.5

    def activate(self):
        self.onScreen = False
        self.active = True
        self.startTime = time.time()

    def update_vx(self, v_x):
        self.vx = v_x

    def move_pow(self, sign, GRID):
        GRID[self.y][self.x] = ' '

        self.counts += self.v_y
        self.y = math.floor(self.counts)

        if self.speed <= 2:
            self.speed += self.gravity
            self.v_y = math.floor(self.speed)

        if self.v_x <= 0:
            self.x += math.floor(self.v_x / 2)
        else:
            self.x += math.ceil(self.v_x / 2)

        GRID[self.y][self.x] = sign

    def remove_pow(self, GRID):
        GRID[self.y][self.x] = ' '

    def passed_paddle(self, paddle_y):
        return True if self.y + self.v_y > (paddle_y + 1) else False

    def collected(self, paddle_xs, paddle_xe, paddle_y):
        if self.x + self.v_x in range(paddle_xs, paddle_xe) and abs(self.y + self.v_y - paddle_y) <= 1:
            self.activate()
            return True
        return False

    def compare_power(self, sign, powerup_sign):
        return True if sign == powerup_sign else False


class ExpandPaddle(PowerUp):
    def __init__(self, x, y, v_x):
        super().__init__(x, y, v_x)
        self.sign = 'E'
        self.type = 'paddle_size'
        self.display = 'Expand Paddle'

    def move(self, GRID):
        self.move_pow(self.sign, GRID)

    def start_effect(self, BALL, PADDLE, GRID):
        new_vx_list = [-3, -2, -2, -1, -1, 0, 1, 1, 2, 2, 3]
        PADDLE.remove_paddle(GRID)
        PADDLE.update_vx_list(new_vx_list)

    def end_effect(self, BALL, PADDLE, GRID):
        new_vx_list = cg.VX_LIST
        PADDLE.remove_paddle(GRID)
        PADDLE.update_vx_list(new_vx_list)

    def compare(self, powerup_type):
        self.compare_power(self.type, powerup_type)


class ShrinkPaddle(PowerUp):
    def __init__(self, x, y, v_x):
        super().__init__(x, y, v_x)
        self.sign = 'S'
        self.type = 'paddle_size'
        self.display = 'Shrink Paddle'

    def move(self, GRID):
        self.move_pow(self.sign, GRID)

    def start_effect(self, BALL, PADDLE, GRID):
        new_vx_list = [-1, -1, 0, 1, 1]
        PADDLE.remove_paddle(GRID)
        PADDLE.update_vx_list(new_vx_list)

    def end_effect(self, BALL, PADDLE, GRID):
        new_vx_list = cg.VX_LIST
        PADDLE.remove_paddle(GRID)
        PADDLE.update_vx_list(new_vx_list)

    def compare(self, powerup_type):
        self.compare_power(self.type, powerup_type)


class PaddleGrab(PowerUp):
    def __init__(self, x, y, v_x):
        super().__init__(x, y, v_x)
        self.sign = 'G'
        self.type = 'paddle_grab'
        self.display = 'Grab Ball'

    def move(self, GRID):
        self.move_pow(self.sign, GRID)

    def start_effect(self, BALL, PADDLE, GRID):
        PADDLE.can_grab()

    def end_effect(self, BALL, PADDLE, GRID):
        PADDLE.can_grab_revert()

    def compare(self, powerup_type):
        self.compare_power(self.type, powerup_type)


class LaserPaddle(PowerUp):
    def __init__(self, x, y, v_x):
        super().__init__(x, y, v_x)
        self.sign = 'L'
        self.type = 'laser_paddle'
        self.display = 'Laser Paddle'

    def move(self, GRID):
        self.move_pow(self.sign, GRID)

    def start_effect(self, BALL, PADDLE, GRID):
        PADDLE.activate_lasers(self.startTime)

    def end_effect(self, BALL, PADDLE, GRID):
        PADDLE.deactivate_lasers(GRID)

    def compare(self, powerup_type):
        self.compare_power(self.type, powerup_type)


class ThruBall(PowerUp):
    def __init__(self, x, y, v_x):
        super().__init__(x, y, v_x)
        self.sign = 'T'
        self.type = 'thru_ball'
        self.display = 'Thru Ball'

    def move(self, GRID):
        self.move_pow(self.sign, GRID)

    def start_effect(self, BALL, PADDLE, GRID):
        BALL.set_thruball(True)

    def end_effect(self, BALL, PADDLE, GRID):
        BALL.set_thruball(False)

    def compare(self, powerup_type):
        self.compare_power(self.type, powerup_type)


class FastBall(PowerUp):
    def __init__(self, x, y, v_x):
        super().__init__(x, y, v_x)
        self.sign = 'F'
        self.type = 'fast_ball'
        self.factor = 1.5
        self.display = 'Fast Ball'

    def move(self, GRID):
        self.move_pow(self.sign, GRID)

    def start_effect(self, BALL, PADDLE, GRID):
        new_vx_list = [math.floor(x*self.factor) if x > 0 else math.ceil(x*self.factor)
                       for x in PADDLE.vx_list]
        PADDLE.remove_paddle(GRID)
        PADDLE.update_vx_list(new_vx_list)

    def end_effect(self, BALL, PADDLE, GRID):
        new_vx_list = [math.ceil(x/self.factor) if x > 0 else math.floor(x/self.factor)
                       for x in PADDLE.vx_list]
        PADDLE.remove_paddle(GRID)
        PADDLE.update_vx_list(new_vx_list)

    def compare(self, powerup_type):
        self.compare_power(self.type, powerup_type)


class MultiBall(PowerUp):
    def __init__(self, x, y, v_x):
        super().__init__(x, y, v_x)
        self.sign = 'M'
        self.type = 'multi_ball'
        self.factor = 1
        self.display = 'Multi Ball'

    def move(self, GRID):
        self.move_pow(self.sign, GRID)

    def start_effect(self, BALL_LIST):
        new_balls = []
        for ball in BALL_LIST:
            new_ball = Ball(ball.x, ball.y, 0)
            new_ball.launch_ball(ball.v_x, ball.v_y)
            new_balls.append(new_ball)
        BALL_LIST.extend(new_balls)

    def end_effect(self, BALL, PADDLE, GRID):
        pass


def select_powerup(x, y, v_x):
    idx = random.randint(0, len(cg.POWERUPS) - 1)
    if cg.POWERUPS[idx] == 'ExpandPaddle':
        return ExpandPaddle(x, y, v_x)
    if cg.POWERUPS[idx] == 'ShrinkPaddle':
        return ShrinkPaddle(x, y, v_x)
    if cg.POWERUPS[idx] == 'PaddleGrab':
        return PaddleGrab(x, y, v_x)
    if cg.POWERUPS[idx] == 'LaserPaddle':
        return LaserPaddle(x, y, v_x)
    if cg.POWERUPS[idx] == 'FastBall':
        return FastBall(x, y, v_x)
    if cg.POWERUPS[idx] == 'ThruBall':
        return ThruBall(x, y, v_x)
    if cg.POWERUPS[idx] == 'MultiBall':
        return MultiBall(x, y, v_x)
