'''Defining Configuration File '''

WIDTH = 121
HEIGHT = 40

VX_LIST = [-2, -1, -1, 0, 1, 1, 2]
VY = -1
PADDLE_X = 55
PADDLE_Y = 36

PADDING = ' '*35

BLOCK_LENGTH = 4
PADDLE_LENGTH = 7

UFO_HEIGHT = 4
UFO_WIDTH = 7
UFO_Y = 4

BLOCK_L = '\033[0;36m█\033[0m'  # CYAN
BLOCK_M = '\033[0;34m█\033[0m'  # BLUE
BLOCK_H = '\033[0;31m█\033[0m'  # RED
BLOCK_U = '\033[0;35m█\033[0m'  # MAGENTA

BLOCKS = [BLOCK_L, BLOCK_M, BLOCK_H, BLOCK_U]

UFO = ['_', '\\', '/', '-', '\'', ')', '(']

COLOR_END = '\033[0m'

POWERUPS = ['ExpandPaddle', 'ShrinkPaddle',
            'PaddleGrab', 'FastBall', 'ThruBall', 'MultiBall', 'LaserPaddle']
POWER_TIME = 15
