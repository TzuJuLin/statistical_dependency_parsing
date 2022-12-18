import numpy as np


score = np.array([[0.0, 9, 10, 9], [-10000, 0.0, 20, 3],
                 [-10000, 30, 0.0, 30], [-10000, 11, 0, 0.0]])

# score = np.array([[0.0, 10, 5, 15], [-10000, 0.0, 20, 15],
#                  [-10000, 25, 0.0, 25], [-10000, 30, 10, 0.0]])


def eisner(score):
    # pass score matrix
    # sentence includes  ROOT
    row, col = score.shape
    assert col == row, 'must be square matrix'

    N = row

    # initialize
    Or = np.zeros([N, N])
    Ol = np.zeros([N, N])
    Cr = np.zeros([N, N])
    Cl = np.zeros([N, N])

    # initialize back pointer tables
    BOr = np.zeros([N, N])
    BOl = np.zeros([N, N])
    BCr = np.zeros([N, N])
    BCl = np.zeros([N, N])

    for m in range(1, N):
        for s in range(0, N-m):
            t = s+m

            for q in range(s, t):
                if Cl[s][q] + Cr[q+1][t] + score[t][s] >= Or[s][t]:
                    Or[s][t] = Cl[s][q] + Cr[q+1][t] + score[t][s]
                    BOr[s][t] = q
                if Cl[s][q] + Cr[q+1][t] + score[t][s] < 0:
                    Or[s][t] = -10000
                    BOr[s][t] = 0
            for q in range(s, t):
                if Cl[s][q] + Cr[q+1][t] + score[s][t] >= Ol[s][t]:
                    Ol[s][t] = Cl[s][q] + Cr[q+1][t] + score[s][t]
                    BOl[s][t] = q
            for q in range(s, t):
                if Cr[s][q] + Or[q][t] >= Cr[s][t]:
                    Cr[s][t] = Cr[s][q] + Or[q][t]
                    BCr[s][t] = q
                if Cr[s][q] + Or[q][t] < 0:
                    Cr[s][t] = -10000
                    BCr[s][t] = 0
            for k in range(s+1, t+1):
                if Ol[s][k] + Cl[k][t] >= Cl[s][t]:
                    Cl[s][t] = Ol[s][k] + Cl[k][t]
                    BCl[s][t] = k
            # for intermediate check
            # print("m:" + str(m) + " s: " + str(s) + " t: " + str(t))
            # print(Or, Ol, Cr, Cl)
    print(Or, Ol, Cr, Cl)
    print(BOr, BOl, BCr, BCl)
    return Cl[0][N-1]


print(eisner(score))
