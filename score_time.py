import config as cg
import time


def print_score_time(score, life, time):
    lifes_left = '\033[0;31m❤\033[0m '*life
    padding_time = ' '*37
    padding_score = ' '*38
    padding_life = ' '*42
    print()
    print(f'{padding_time}TIME: {time:.2f} mins', end="")
    print(f'{padding_score}SCORE: {score}', end="")
    print(f'{padding_life}LIVES: {lifes_left}', end="")
    print()


def print_active_powerups(active_powerups):
    padding = ' '*75
    print()
    for powerup in active_powerups:
        print(
            f'{padding}{powerup.display} => {cg.POWER_TIME - (time.time() - powerup.startTime)}')


def print_boss_health(health):
    boss_health = '❤ '*health
    padding = ' '*80

    print(f'{padding}BOSS HEALTH: {boss_health}', end="")
    print()
