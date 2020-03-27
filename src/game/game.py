#!/usr/bin/env python3.7
import numpy as np
import pandas as pd
import pygame

"""
https://github.com/TheAILearner/Training-Snake-Game-With-Genetic-Algorithm
"""

legal_moves = "<>^v"
LEFT, RIGHT, UP, DOWN = tuple(list(legal_moves))
DIM = 4
shape = (DIM, DIM)

init_vals = (2, 4)
init_dist = (0.9, 0.1)


def xy(coord):
    return coord // DIM, coord % DIM,


def init(num_init=2):
    assert sum(init_dist) == 1, "Dist must be 1"
    assert len(init_dist) == len(init_vals), "Vals and dist must be the same length"
    grid: np.array = np.zeros(shape=shape, dtype=int)

    ivs = np.random.choice(a=init_vals, size=num_init, p=init_dist)
    ics = np.random.choice(a=range(grid.size), size=num_init, replace=False)

    for c, v in zip(ics, ivs):
        grid[divmod(c, DIM)] = v

    return grid


def get_next_full(grid: np.array, row: int, col: int):
    while col < DIM:
        if grid[row, col] != 0:
            return row, col
        else:
            col += 1
    return row, col - 1


def move_cell(grid: np.array, row: int, col: int):
    next_full = get_next_full(grid, row, col + 1)
    curr = row, col
    if grid[curr] == 0:
        grid[curr] += grid[next_full]
        grid[next_full] = 0

    next_full = get_next_full(grid, row, col + 1)
    # if 0 == M[curr] != M[next_full] or M[next_full] == M[curr]:
    if grid[curr] == grid[next_full]:
        grid[curr] += grid[next_full]
        grid[next_full] = 0


def move_left(normalized_grid):
    for row in range(DIM):
        for col in range(DIM):
            move_cell(normalized_grid, row, col)
    return normalized_grid


def flip(grid: np.array, move):
    if move is LEFT:
        pass
    if move is RIGHT:
        grid = np.flip(m=grid, axis=1)
    if move is UP:
        grid = grid.T
    if move is DOWN:
        grid = np.flip(m=grid, axis=0)
        grid = grid.T
    return grid


def flop(grid, move):
    if move is LEFT:
        pass
    if move is RIGHT:
        grid = np.flip(m=grid, axis=1)
    if move is UP:
        grid = grid.T
    if move is DOWN:
        grid = grid.T
        grid = np.flip(m=grid, axis=0)
    return grid


def get_new_num():
    return np.random.choice(a=init_vals, p=init_dist)


def get_vacant(partially_filled_grid):
    # n = partially_filled_grid.shape[0]
    vacant = [i for i in range(DIM ** 2) if i not in np.flatnonzero(partially_filled_grid)]
    return divmod(np.random.choice(vacant), DIM)


def fill(grid):
    grid[get_vacant(grid)] = get_new_num()
    return grid


def player_action(grid, move):
    grid = flip(grid, move)
    grid = move_left(grid)
    grid = flop(grid, move)
    return grid


def game_done(grid):
    for move in legal_moves:
        if np.any(
                np.logical_xor(
                    player_action(grid.copy(), move),
                    grid
                )
        ):
            return False
    else:
        print("Game Done!")
        return True


def pp(matrix):
    df = pd.DataFrame(matrix)
    df.style.hide_index()
    df.style.hide_columns(df.columns)
    df.replace({0: ""}, inplace=True)
    print(df)


def get_input() -> str:
    print("move (" + legal_moves + ") : ")
    move = input()
    assert move in legal_moves, "Illegal Move"
    return move


def game():
    grid = init(2)
    while not game_done(grid):
        pp(grid)
        try:
            move = get_input()
        except AssertionError as e:
            print(e)
            continue

        prev = grid.copy()
        grid = player_action(grid, move)
        change = np.logical_xor(grid, prev)
        if np.any(change):
            grid = fill(grid)
            pass

    pp(grid)


class Game(object):
    """docstring for Game"""

    def __init__(self, dim=4, num_init=2):
        super(Game, self).__init__()
        self.dim = dim


if __name__ == "__main__":
    game()
