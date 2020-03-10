import numpy as np
import click
import pandas as pd

moves = "<>^V"
LEFT, RIGHT, UP, DOWN = tuple(list(moves))
dim = 4
shape = (dim, dim)

init_vals = (2, 4)
init_dist = (0.9, 0.1)


def xy(coord):
    return coord // dim, coord % dim,


def init(num_init=2):
    assert sum(init_dist) == 1, "Dist must be 1"
    assert len(init_dist) == len(init_vals), "Vals and dist must be the same length"
    M : np.array = np.zeros(shape=shape, dtype=int)

    ivs = np.random.choice(a=init_vals, size=num_init, p=init_dist)
    ics = np.random.choice(a=range(M.size), size=num_init, replace=False)

    for c, v in zip(ics, ivs):
        M[xy(c)] = v

    return M


def get_next_full(M, row, col):
    while col < dim:
        if M[row, col] != 0:
            return row, col
        else:
            col += 1
    return row, col - 1


def move_cell(M, row, col):
    next_full = get_next_full(M, row, col + 1)
    curr = row, col
    if M[curr] == 0:
        M[curr] += M[next_full]
        M[next_full] = 0

    next_full = get_next_full(M, row, col + 1)
    # if 0 == M[curr] != M[next_full] or M[next_full] == M[curr]:
    if M[curr] == M[next_full]:
        M[curr] += M[next_full]
        M[next_full] = 0


def move_left(M):
    for row in range(dim):
        for col in range(dim):
            move_cell(M, row, col)
    return M


def flip(M: np.array, move):
    M = M.copy()
    if move is LEFT:
        pass
    if move is RIGHT:
        M = np.flip(m=M, axis=1)
    if move is UP:
        M = M.T
    if move is DOWN:
        M = np.flip(m=M, axis=0)
        M = M.T

    return M


def flop(M, move):
    M = M.copy()
    if move is LEFT:
        pass
    if move is RIGHT:
        M = np.flip(m=M, axis=1)
    if move is UP:
        M = M.T
    if move is DOWN:
        M = M.T
        M = np.flip(m=M, axis=0)
    return M


def get_new_num():
    return np.random.choice(a=init_vals, p=init_dist)


def get_vacant(M):
    n = M.shape[0]
    vacant = [i for i in range(dim ** 2) if i not in np.flatnonzero(M)]
    return xy(np.random.choice(vacant))


def fill(M):
    M[get_vacant(M)] = get_new_num()
    return M


def player_action(M, move):
    M = flip(M, move)
    M = move_left(M)
    M = flop(M, move)
    return M.copy()


def game_done(M):
    ref = M.copy()
    for mv in moves:
        if np.any(np.logical_xor(player_action(M.copy(), mv), ref)):
            return False
    else:
        return True

def pp(M):
    df = pd.DataFrame(M)
    df.replace({0: ""}, inplace=True)
    print(df)


def main():
    click.clear()

    M = init(2)
    pp(M)
    while True:
        click.clear()
        pp(M)
        print("move (" + moves + ") : ")
        # move = click.getchar(echo=True)
        move =input()
        while move not in list(moves):
            print(" -> Illegal Move")
            move = input()
            # move = click.getchar(echo=True)
            continue


        prev = M.copy()
        M = player_action(M, move)
        change = np.logical_xor(M, prev)
        if np.any(change):
            M = fill(M)

        if game_done(M):
            break



    pp(M)

if __name__ == "__main__":
    main()
