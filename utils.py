import config as cg
import random
import time
import math
from Assets import Block_H, Block_L, Block_M, Block_U, Block_R, Empty, Paddle, Ball, Boss_Enemy

# Initializing the GRID and utilities
GRID = [[' ']*cg.WIDTH for rows in range(cg.HEIGHT)]
BALL_LIST = []
PADDLE = Paddle(cg.PADDLE_X, cg.PADDLE_Y)
block_list = []

# Falling Bricks Feature
falltime = 30
time_multiplier = 1


def init_ball_list():
    Offset = random.randint(1, cg.PADDLE_LENGTH - 1)
    PADDLE.reset_paddle(GRID)
    BALL_LIST.append(Ball(PADDLE.x_start + Offset, PADDLE.y - 1, Offset))


def finish_balls():
    for ball in BALL_LIST:
        ball.remove_ball(GRID)
        BALL_LIST.remove(ball)


def finish_blocks():
    global block_list
    block_list = []


def CreateFrame():
    # Creating the frame
    GRID[cg.HEIGHT - 1][0] = '╚'
    GRID[cg.HEIGHT - 1][cg.WIDTH - 1] = '╝'
    GRID[0][0] = '╔'
    GRID[0][cg.WIDTH - 1] = '╗'

    for cols in range(1, cg.WIDTH-1):
        GRID[0][cols] = '═'
        GRID[cg.HEIGHT-1][cols] = '═'

    for rows in range(1, cg.HEIGHT-1):
        GRID[rows][0] = '║'
        GRID[rows][cg.WIDTH-1] = '║'

    for cols in range(2, cg.WIDTH-2):
        for rows in range(2, cg.HEIGHT-2):
            GRID[rows][cols] = ' '


def create_boss_layer_1():
    layer_length = 29
    x = 3
    y = 10

    for _ in range(layer_length):
        Blk = Block_L(x, y)

        block_list.append(Blk)
        x += cg.BLOCK_LENGTH


def create_boss_layer_2():
    layer_length = 29
    x = 3
    y = 10

    for _ in range(layer_length):
        Blk = Block_M(x, y)

        block_list.append(Blk)
        x += cg.BLOCK_LENGTH


def render_blocks():
    for block in block_list:
        if block.type == 'R':
            block.rotate_variant()
            block.switch_block()
        block.put_block(GRID)


def fall_blocks(start_time):
    global time_multiplier
    max_depth = 0
    cur_time = math.floor(time.time())
    if cur_time - math.floor(start_time) >= falltime * time_multiplier:
        for block in block_list:
            depth = block.fall(GRID)
            max_depth = max(max_depth, depth)
        time_multiplier += 1

    return max_depth


def return_level(level):
    if level == 0:
        with open("./Levels/Level_0.txt") as file:
            model = file.read()
    elif level == 1:
        with open("./Levels/Level_1.txt") as file:
            model = file.read()
    elif level == 2:
        with open("./Levels/Level_2.txt") as file:
            model = file.read()
    return model


def set_assets(level):
    CreateFrame()
    init_ball_list()

    level_model = None
    layer_length = 20
    layer_depth = 9

    num_blocks = 0

    # Boss for level 2
    boss_enemy = Boss_Enemy(PADDLE.x_start, cg.UFO_Y)

    # Creating the Block List
    level_model = return_level(level)

    for i in range(layer_depth):
        x = 19
        y = 5 + i
        layer = level_model[i*layer_length: (i+1)*layer_length]
        for block in layer:
            Blk = None
            if(block == '0'):
                Blk = Empty(x, y)
            elif(block == '1'):
                Blk = Block_L(x, y)
            elif(block == '2'):
                Blk = Block_M(x, y)
            elif(block == '3'):
                Blk = Block_H(x, y)
            elif(block == '4'):
                Blk = Block_U(x, y)
            else:
                Blk = Block_R(x, y)

            if(block != '0' or block != '4'):
                num_blocks += 1

            block_list.append(Blk)
            x += cg.BLOCK_LENGTH

    # Putting the Block
    render_blocks()

    # Placing the BOSS
    if level == 2:
        boss_enemy.set_boss(GRID)

    BALL_LIST[0].set_ball(GRID)
    PADDLE.set_paddle(GRID)

    return GRID, num_blocks, block_list, boss_enemy


def print_frame():
    # Printing the Frame
    for i in range(cg.HEIGHT):
        print(cg.PADDING, end="")
        for j in range(cg.WIDTH):
            print(GRID[i][j], end="")
        print()
