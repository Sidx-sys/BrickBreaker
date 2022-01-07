import config as cg
import os
from time import sleep
import random
import time

from input import Input
from Assets import Block_H, Block_L, Block_M, Block_U, Empty, Paddle, Ball
from utils import set_assets, BALL_LIST, render_blocks, PADDLE, print_frame, init_ball_list, finish_balls, fall_blocks, finish_blocks, create_boss_layer_1, create_boss_layer_2
from collisions import collision_handler
from powerups import select_powerup
from handle_powers import *
from score_time import print_score_time, print_active_powerups, print_boss_health


def GameLoop():
    # States
    on_screen_powerups = []
    active_powerups = []
    block_list = []
    life = 5
    timer = time.time()
    score = 0
    level = 0
    blocks_left = 0
    skip_level = False
    max_depth = 0
    boss_enemy = None

    # Initializing the GRID
    GRID, blocks_left, block_list, boss_enemy = set_assets(level)

    # Creating the Input Class
    INPUT = Input()

    os.system("stty -echo")
    os.system('clear')
    while life > 0:
        if skip_level or not blocks_left:
            if level < 2:
                level += 1
                finish_balls()
                finish_blocks()
                blocks_left = 0
            else:
                exit()

        if not len(BALL_LIST):
            for powerup in on_screen_powerups:
                powerup.remove_pow(GRID)
            on_screen_powerups = []
            active_powerups = []
            if skip_level:
                GRID, blocks_left, block_list, boss_enemy = set_assets(level)
                skip_level = False
            else:
                life -= 1
                boss_enemy.reset_bombs(GRID)
                init_ball_list()

        text = INPUT.get_parsed_input(0.06)

        if text == 'quit' or max_depth >= cg.PADDLE_Y:
            exit()
        elif text == 'skip':
            skip_level = True
            continue
        elif text == 'left':
            PADDLE.move_left(GRID)

        elif text == 'right':
            PADDLE.move_right(GRID)

        if level == 0 or level == 1:
            max_depth = fall_blocks(timer)

            for BALL in BALL_LIST:
                score, blocks_left, life = collision_handler(
                    GRID, BALL, PADDLE, on_screen_powerups, score, blocks_left, block_list, boss_enemy, level, life)

                if text == 'space' and not BALL.launched:
                    BALL.launch_ball(PADDLE.vx_list[BALL.offset], cg.VY)

                if not BALL.launched:
                    BALL.update_x(PADDLE.x_start + BALL.offset, GRID)

                render_blocks()

                powerup_movement(GRID, BALL, PADDLE, BALL_LIST,
                                 on_screen_powerups, active_powerups)
                powerup_effect(GRID, BALL, PADDLE, active_powerups)

                BALL.move(GRID, BALL_LIST)

            for laser in PADDLE.lasers:
                laser.move(GRID)

            os.system('clear')
            print_score_time(score, life, (time.time() - timer)/60)
            PADDLE.set_paddle(GRID)
            PADDLE.fire_lasers(GRID)

            print_frame()
            print_active_powerups(active_powerups)

        else:
            score, blocks_left, life = collision_handler(
                GRID, BALL_LIST[0], PADDLE, on_screen_powerups, score, blocks_left, block_list, boss_enemy, level, life)

            health = boss_enemy.return_health()

            if text == 'space' and not BALL_LIST[0].launched:
                BALL_LIST[0].launch_ball(
                    PADDLE.vx_list[BALL_LIST[0].offset], cg.VY)

            if not BALL_LIST[0].launched:
                BALL_LIST[0].update_x(
                    PADDLE.x_start + BALL_LIST[0].offset, GRID)

            if health == 8:
                create_boss_layer_1()
            elif health == 4:
                create_boss_layer_2()
            elif health <= 0:
                exit()

            render_blocks()

            BALL_LIST[0].move(GRID, BALL_LIST)

            os.system('clear')
            print_boss_health(health)
            print_score_time(score, life, (time.time() - timer)/60)

            PADDLE.set_paddle(GRID)
            boss_enemy.reset_boss(PADDLE.x_start, GRID)
            boss_enemy.set_boss(GRID)

            if len(BALL_LIST) and BALL_LIST[0].launched:
                boss_enemy.drop_bomb()

            for bomb in boss_enemy.bombs:
                bomb.move(GRID)

            print_frame()

    os.system("stty echo")


if __name__ == "__main__":
    GameLoop()
