'''Handle collision according to the surface of contact'''
import config as cg
import random

from Assets import Empty, Block_L, Block_M
from powerups import select_powerup


def create_powerup(v_x, start, y, on_screen_powerups, level):
    if level == 2:
        return

    if random.uniform(0, 1.0) >= 0.5:
        powerup = select_powerup(start + 2, y, v_x)
        on_screen_powerups.append(powerup)


def replace_block_y(Block_List, on_screen_powerups, BALL, X, Y, blocks_left, level, is_ball=True):
    found = False
    points = 0

    if not BALL.is_thruball_active() and is_ball:
        BALL.update_vy(-BALL.v_y)

    for block in Block_List:
        start = block.x_start
        end = block.x_end
        y = block.y
        to_replace = Empty(start, y)

        if BALL.is_thruball_active():
            if start <= X and X <= end and Y == y:
                create_powerup(BALL.v_x, start, y, on_screen_powerups, level)
                Block_List.remove(block)
                found = True
                points = block.points
                if block.strength > 0 and block.strength != 4:
                    blocks_left -= 1
                break
        else:
            if start <= X and X <= end and Y == y and block.strength > 0:
                if block.strength == 1:
                    points = block.points
                    blocks_left -= 1
                    create_powerup(BALL.v_x, start, y,
                                   on_screen_powerups, level)

                elif block.strength == 2:
                    to_replace = Block_L(start, y, block.points)
                elif block.strength == 3:
                    to_replace = Block_M(start, y, block.points)

                Block_List.remove(block)
                found = True
                break

    if found:
        Block_List.append(to_replace)
        return points, blocks_left
    return 0, blocks_left


def replace_block_x(Block_List, on_screen_powerups, BALL, X, Y, blocks_left, level):
    found = False
    points = 0

    if not BALL.is_thruball_active():
        BALL.update_vx(-BALL.v_x)

    for block in Block_List:
        start = block.x_start
        end = block.x_end
        y = block.y
        to_replace = Empty(start, y)

        if BALL.is_thruball_active():
            if start <= X and X <= end and y == Y:
                create_powerup(BALL.v_x, start, y, on_screen_powerups, level)
                Block_List.remove(block)
                found = True
                points = block.points
                if block.strength > 0 and block.strength != 4:
                    blocks_left -= 1
                break
        else:
            if start <= X and X <= end and y == Y and block.strength > 0:
                if block.strength == 1:
                    points = block.points
                    blocks_left -= 1
                    create_powerup(BALL.v_x, start, y,
                                   on_screen_powerups, level)

                elif block.strength == 2:
                    to_replace = Block_L(start, y, block.points)
                elif block.strength == 3:
                    to_replace = Block_M(start, y, block.points)

                Block_List.remove(block)
                found = True
                break

    if found:
        Block_List.append(to_replace)
        return points, blocks_left
    return 0, blocks_left


def replace_block_xy(Block_List, on_screen_powerups, BALL, X, Y, blocks_left, level):
    found = False
    points = 0

    if not BALL.is_thruball_active():
        BALL.update_vx(-BALL.v_x)
        BALL.update_vy(-BALL.v_y)

    for block in Block_List:
        start = block.x_start
        end = block.x_end
        y = block.y
        to_replace = Empty(start, y)

        if BALL.is_thruball_active():
            if start <= X and X <= end and y == Y:
                create_powerup(BALL.v_x, start, y, on_screen_powerups, level)
                Block_List.remove(block)
                found = True
                points = block.points
                if block.strength > 0 and block.strength != 4:
                    blocks_left -= 1
                break
        else:
            if start <= X and X <= end and y == Y and block.strength > 0:
                if block.strength == 1:
                    points = block.points
                    blocks_left -= 1
                    create_powerup(BALL.v_x, start, y,
                                   on_screen_powerups, level)

                elif block.strength == 2:
                    to_replace = Block_L(start, y, block.points)
                elif block.strength == 3:
                    to_replace = Block_M(start, y, block.points)

                Block_List.remove(block)
                found = True
                break

    if found:
        Block_List.append(to_replace)
        return points, blocks_left
    return 0, blocks_left


def ufo_collision_y(X, Y, BALL, BOSS):
    BALL.update_vy(-BALL.v_y)
    BOSS.hit()


def ufo_collision_x(X, Y, BALL, BOSS):
    BALL.update_vx(-BALL.v_x)
    BOSS.hit()


def ufo_collision_xy(X, Y, BALL, BOSS):
    BALL.update_vy(-BALL.v_y)
    BALL.update_vx(-BALL.v_x)
    BOSS.hit()


def collision_handler(GRID, BALL, PADDLE, on_screen_powerups, score, blocks_left, block_list, boss_enemy, level, life):
    # Frame Collision
    if BALL.x + BALL.v_x >= cg.WIDTH - 1:
        BALL.update_vx(-BALL.v_x)
    elif BALL.x + BALL.v_x < 2:
        BALL.update_vx(-BALL.v_x)

    if BALL.y <= 1:
        BALL.update_vy(-BALL.v_y)

    # Paddle Collision
    if GRID[BALL.y + BALL.v_y][BALL.x] == PADDLE.content and BALL.launched:
        if PADDLE.grab:
            BALL.grab_ball(BALL.x, PADDLE.y - 1, PADDLE.x_start, GRID)
        else:
            BALL.update_vy(-BALL.v_y)
            BALL.update_vx(PADDLE.vx_list[BALL.x - PADDLE.x_start])
    elif GRID[BALL.y + BALL.v_y][BALL.x + BALL.v_x] == PADDLE.content and BALL.launched:
        if PADDLE.grab:
            BALL.grab_ball(BALL.x + BALL.v_x, PADDLE.y -
                           1, PADDLE.x_start, GRID)
        else:
            BALL.update_vy(-BALL.v_y)
            BALL.update_vx(PADDLE.vx_list[BALL.x + BALL.v_x - PADDLE.x_start])

    # Block Collision Horizontal
    left = blocks_left
    for BLOCK in cg.BLOCKS:
        if GRID[BALL.y + BALL.v_y][BALL.x] == BLOCK:
            points, left = replace_block_y(block_list, on_screen_powerups,
                                           BALL, BALL.x, BALL.y + BALL.v_y, blocks_left, level)
            score += points
            break

    # Block Collision Vertical
        elif GRID[BALL.y][BALL.x + BALL.v_x] == BLOCK:
            points, left = replace_block_x(block_list, on_screen_powerups,
                                           BALL, BALL.x + BALL.v_x, BALL.y, blocks_left, level)
            score += points
            break

        elif GRID[BALL.y + BALL.v_y][BALL.x + BALL.v_x] == BLOCK:
            points, left = replace_block_xy(block_list, on_screen_powerups,  BALL, BALL.x +
                                            BALL.v_x, BALL.y + BALL.v_y, blocks_left, level)
            score += points
            break

    if level < 2:
        # Laser collisions with the blocks
        for laser in PADDLE.lasers:
            for BLOCK in cg.BLOCKS:
                if GRID[laser.y + laser.v_y][laser.x] == BLOCK:
                    points, left = replace_block_y(block_list, on_screen_powerups,
                                                   BALL, laser.x, laser.y + laser.v_y, blocks_left, level, False)
                    score += points
                    laser.destroy(GRID)
                    PADDLE.lasers.remove(laser)
                    break

    # Boss Enemy Collision
    if level == 2:
        for ufo_sect in cg.UFO:
            if GRID[BALL.y + BALL.v_y][BALL.x] == ufo_sect:
                ufo_collision_y(BALL.x, BALL.y + BALL.v_y, BALL, boss_enemy)

            elif GRID[BALL.y][BALL.x + BALL.v_x] == ufo_sect:
                ufo_collision_x(BALL.x + BALL.v_x, BALL.y, BALL, boss_enemy)

            elif GRID[BALL.y + BALL.v_y][BALL.x + BALL.v_x] == ufo_sect:
                ufo_collision_xy(BALL.x + BALL.v_x, BALL.y +
                                 BALL.v_y, BALL, boss_enemy)

        # Bomb Collision
        for bomb in boss_enemy.bombs:
            if GRID[bomb.y + bomb.v_y][bomb.x] == PADDLE.content:
                life -= 1
                bomb.destroy(GRID)
                boss_enemy.bombs.remove(bomb)

    return score, left, life
