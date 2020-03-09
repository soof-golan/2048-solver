import numpy as np

moves = "<>^v"
dim = 4
shape = (dim, dim)
M = np.zeros(shape=shape, dtype=int)
num_init = 2
iv = [2, 4]
id = [0.9, 0.1]

ivs = np.random.choice(a=iv, size=num_init, p=id)
ics = np.random.choice(a=range(M.size), size=num_init, replace=False)
xys = [(c//dim, c % dim) for c in ics]


def xy(coord):
    return coord % dim, coord // dim


for c, v in zip(ics, ivs):
    M[xy(c)] = v


print(M.size, ics, ivs, xys)
while True:
    print(M)
    inp = input("move (" + moves + ") : ")
    if inp not in list(moves):
        print("FU")
        continue

    for row in range(dim):
        for col in range(dim):
            next = col + 1
            if M[row, col] == 0:
                while next < dim and M[row, next] == 0:
                    next += 1
                if next == dim:
                    continue
                if M[row, next] == M[row, col]:
                    M[row, col] += M[row, next]
                    M[row, next] = 0

            while next < dim and M[row, next] == 0:
                next += 1
            if next == dim:
                continue

            if M[row, next] == M[row, col]:
                M[row, col] += M[row, next]
                M[row, next] = 0

    # MOVE LEFT
    # for row in range(dim):
    #     # full = empty = (row, 0)
    #     for col in range(dim):
    #         curr = row, col
    #         next = col + 1
    #         if M[curr] == 0:
    #             while next < dim and M[row, next] == 0:
    #                 next += 1
    #             if next == dim:
    #                 continue
    #             if M[row, next] == M[curr]:
    #                 M[curr] += M[row, next]
    #                 M[row, next] = 0
    #
    #         while next < dim and M[row, next] == 0:
    #             next += 1
    #         if next == dim:
    #             continue

            # if M[row, next] == M[row, col]:
            #     M[row, col] += M[row, next]
            #     M[row, next] = 0
            # if M[curr] != 0:
            #     if empty != curr:
            #         M[empty] = M[curr]
            #         M[curr] = 0
            #     else:
            #         pass
            #     pass
            # print("\dim\ncurr", curr)
            # print("empty", empty)
            # print("full", full)

