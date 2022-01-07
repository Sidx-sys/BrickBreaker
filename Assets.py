'''Assets Required for the Game'''
import config as cg
import time
import math


class Block:
    def __init__(self, x, y):
        self.x_start = x
        self.x_end = x + cg.BLOCK_LENGTH
        self.y = y
        self.content = '█'

    def remove_block(self, GRID):
        for x in range(self.x_start, self.x_end):
            GRID[self.y][x] = ' '

    def fall(self, GRID):
        self.remove_block(GRID)
        self.y += 1
        return self.y


class Block_L(Block):
    def __init__(self, x, y, points=1):
        super().__init__(x, y)
        self.type = 'L'
        self.strength = 1
        self.color = '\033[0;36m'
        self.points = points

    def put_block(self, GRID):
        for x in range(self.x_start, self.x_end):
            GRID[self.y][x] = self.color + self.content + cg.COLOR_END


class Block_M(Block):
    def __init__(self, x, y, points=2):
        super().__init__(x, y)
        self.type = 'M'
        self.strength = 2
        self.color = '\033[0;34m'
        self.points = points

    def put_block(self, GRID):
        for x in range(self.x_start, self.x_end):
            GRID[self.y][x] = self.color + self.content + cg.COLOR_END


class Block_H(Block):
    def __init__(self, x, y, points=3):
        super().__init__(x, y)
        self.type = 'H'
        self.strength = 3
        self.color = '\033[0;31m'
        self.points = points

    def put_block(self, GRID):
        for x in range(self.x_start, self.x_end):
            GRID[self.y][x] = self.color + self.content + cg.COLOR_END


class Block_U(Block):
    def __init__(self, x, y, points=5):
        super().__init__(x, y)
        self.type = 'U'
        self.strength = -1
        self.color = '\033[0;35m'
        self.points = points

    def put_block(self, GRID):
        for x in range(self.x_start, self.x_end):
            GRID[self.y][x] = self.color + self.content + cg.COLOR_END


class Block_R(Block):
    def __init__(self, x, y, points=1):
        super().__init__(x, y)
        self.type = 'R'
        self.variant = 1
        self.strength = 1
        self.color = '\033[0;36m'
        self.points = points

    def rotate_variant(self):
        self.variant = 1 + (self.variant % 3)

    def switch_block(self):
        if self.variant == 1:
            self.strength = 1
            self.color = '\033[0;36m'
            self.points = 1
        elif self.variant == 2:
            self.strength = 2
            self.color = '\033[0;34m'
            self.points = 2
        else:
            self.strength = 3
            self.color = '\033[0;31m'
            self.points = 3

    def put_block(self, GRID):
        for x in range(self.x_start, self.x_end):
            GRID[self.y][x] = self.color + self.content + cg.COLOR_END


class Empty(Block):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.content = ' '
        self.type = 'E'
        self.strength = 0
        self.points = 0

    def put_block(self, GRID):
        for x in range(self.x_start, self.x_end):
            GRID[self.y][x] = self.content


class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.v_y = -1
        self.model = '!'

    def passed_limit(self):
        return True if self.y < 2 else False

    def destroy(self, GRID):
        GRID[self.y][self.x] = ' '
        self.v_y = 0

    def move(self, GRID):
        if self.passed_limit():
            self.destroy(GRID)
            return

        GRID[self.y][self.x] = ' '
        self.y += self.v_y
        GRID[self.y][self.x] = self.model


class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.v_y = 1
        self.model = 'B'

    def passed_limit(self):
        return True if self.y > 36 else False

    def destroy(self, GRID):
        GRID[self.y][self.x] = ' '
        self.v_y = 0

    def move(self, GRID):
        if self.passed_limit():
            self.destroy(GRID)
            return

        GRID[self.y][self.x] = ' '
        self.y += self.v_y
        GRID[self.y][self.x] = self.model


class Paddle:
    def __init__(self, x, y):
        self.paddle_length = 7
        self.shoot_lasers = False
        self.lasers = []
        self.laser_timer = 0
        self.counter = 0
        self.x_start = x
        self.x_end = x + self.paddle_length
        self.y = y
        self.vx_list = [-2, -1, -1, 0, 1, 1, 2]
        self.grab = False
        self.content = '▀'

    def update_vx_list(self, new_vx_list):
        self.vx_list = new_vx_list
        self.paddle_length = len(new_vx_list)
        self.x_end = self.x_start + self.paddle_length

    def set_paddle(self, GRID):
        if self.shoot_lasers:
            GRID[self.y][self.x_start] = 'L'
            for step in range(self.x_start + 1, self.x_end - 1):
                GRID[self.y][step] = self.content
            GRID[self.y][self.x_end - 1] = '⅃'
        else:
            for step in range(self.x_start, self.x_end):
                GRID[self.y][step] = self.content

    def remove_paddle(self, GRID):
        for step in range(self.x_start, self.x_end):
            GRID[self.y][step] = ' '

    def reset_paddle(self, GRID):
        self.remove_paddle(GRID)
        self.paddle_length = cg.PADDLE_LENGTH
        self.vx_list = cg.VX_LIST
        self.x_start = cg.PADDLE_X
        self.x_end = self.x_start + cg.PADDLE_LENGTH
        self.laser = []
        self.counter = 0
        self.shoot_lasers = False
        self.grab = False

    def can_grab(self):
        self.grab = True

    def can_grab_revert(self):
        self.grab = False

    def activate_lasers(self, start_time):
        self.shoot_lasers = True
        self.laser_timer = start_time

    def deactivate_lasers(self, GRID):
        self.shoot_lasers = False
        for laser in self.lasers:
            laser.destroy(GRID)
        self.lasers = []
        self.counter = 0

    def fire_lasers(self, GRID):
        if self.shoot_lasers and time.time() - self.laser_timer >= self.counter:
            laser_l = Laser(self.x_start, self.y)
            laser_r = Laser(self.x_end - 1, self.y)

            self.lasers.append(laser_l)
            self.lasers.append(laser_r)
            self.counter += 2

    def move_left(self, GRID):
        if self.x_start <= 2:
            self.x_start = 1
            self.x_end = self.x_start + self.paddle_length
            return
        self.remove_paddle(GRID)
        self.x_start -= 2
        self.x_end -= 2
        self.set_paddle(GRID)

    def move_right(self, GRID):
        if self.x_end >= cg.WIDTH - 2:
            self.x_end = cg.WIDTH - 1
            self.x_start = self.x_end - self.paddle_length
            return
        self.remove_paddle(GRID)
        self.x_start += 2
        self.x_end += 2
        self.set_paddle(GRID)


class Ball:
    def __init__(self, x, y, offset):
        self.x = x
        self.y = y
        self.v_x = 0
        self.v_y = 0
        self.launched = False
        self.model = 'o'
        self.offset = offset
        self.thru = False

    def set_ball(self, GRID):
        GRID[self.y][self.x] = self.model

    def launch_ball(self, v_x, v_y):
        self.launched = True
        self.update_vx(v_x)
        self.update_vy(v_y)

    def grab_ball(self, x, y, paddle_x, GRID):
        self.launched = False
        self.update_vx(0)
        self.update_vy(0)
        self.update_x(x, GRID)
        self.update_y(y, GRID)
        self.offset = x - paddle_x

    def remove_ball(self, GRID):
        GRID[self.y][self.x] = ' '

    def update_vx(self, v_x):
        self.v_x = v_x

    def update_vy(self, v_y):
        self.v_y = v_y

    def update_x(self, x, GRID):
        self.remove_ball(GRID)
        self.x = x
        self.set_ball(GRID)

    def update_y(self, y, GRID):
        self.remove_ball(GRID)
        self.y = y
        self.set_ball(GRID)

    def move(self, GRID, BALL_LIST):
        if self.y <= cg.PADDLE_Y:
            self.remove_ball(GRID)
            self.x += self.v_x
            self.y += self.v_y
            self.set_ball(GRID)
        else:
            self.remove_ball(GRID)
            BALL_LIST.remove(self)

    def is_thruball_active(self):
        return self.thru

    def set_thruball(self, val):
        self.thru = val


class Boss_Enemy:
    def __init__(self, x, y):
        self.model = [
            list("   _   "),
            list("__/ \\__"),
            list("( \\_/ )"),
            list("'--_--'")
        ]
        self.x_start = x
        self.x_end = self.x_start + cg.UFO_WIDTH
        self.y = y
        self.health = 12
        self.vx = 2
        # Bombs
        self.start_time = time.time()
        self.counter = 0
        self.bombs = []

    def set_boss(self, GRID):
        for i in range(cg.UFO_HEIGHT):
            for j in range(cg.UFO_WIDTH):
                GRID[self.y + i][self.x_start + j] = self.model[i][j]

    def remove_boss(self, GRID):
        for i in range(cg.UFO_HEIGHT):
            for j in range(cg.UFO_WIDTH):
                GRID[self.y + i][self.x_start + j] = " "

    def move_left(self, GRID):
        if self.x_start <= 2:
            self.x_start = 1
            self.x_end = self.x_start + cg.UFO_WIDTH
            return
        self.remove_boss(GRID)
        self.x_start -= self.vx
        self.x_end -= self.vx
        self.set_boss(GRID)

    def move_right(self, GRID):
        if self.x_end >= cg.WIDTH - 2:
            self.x_end = cg.WIDTH - 1
            self.x_start = self.x_end - cg.UFO_WIDTH
            return
        self.remove_boss(GRID)
        self.x_start += self.vx
        self.x_end += self.vx
        self.set_boss(GRID)

    def hit(self):
        self.health -= 1

    def return_health(self):
        return self.health

    def reset_boss(self, x, GRID):
        self.remove_boss(GRID)
        self.x_start = x
        self.set_boss(GRID)

    def reset_bombs(self, GRID):
        for bomb in self.bombs:
            GRID[bomb.y + bomb.v_y][bomb.x] = ' '
            self.bombs.remove(bomb)
        self.bombs = []

    def drop_bomb(self):
        if time.time() - self.start_time >= self.counter:
            bomb = Bomb(self.x_start + 3, self.y + cg.UFO_HEIGHT - 1)
            self.bombs.append(bomb)
            self.counter += 3
