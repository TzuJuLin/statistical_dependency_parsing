import numpy as np


score = np.array([[0.0, 9, 10, 9], [-10000, 0.0, 20, 3],
                 [-10000, 30, 0.0, 30], [-10000, 11, 0, 0.0]])

# score = np.array([[0.0, 10, 5, 15], [-10000, 0.0, 20, 15],
#                  [-10000, 25, 0.0, 25], [-10000, 30, 10, 0.0]])


class Decoder:

    def parse(self, score):
        # pass score matrix
        # sentence includes  ROOT
        row, col = score.shape
        assert col == row, 'must be square matrix'

        N = row

        # initialize
        Or = np.zeros([N, N], dtype=int)
        Ol = np.zeros([N, N], dtype=int)
        Cr = np.zeros([N, N], dtype=int)
        Cl = np.zeros([N, N], dtype=int)

        # initialize back pointer tables
        BOr = np.zeros([N, N], dtype=int)
        BOl = np.zeros([N, N], dtype=int)
        BCr = np.zeros([N, N], dtype=int)
        BCl = np.zeros([N, N], dtype=int)

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
                    if Cl[s][q] + Cr[q+1][t] + score[s][t] >= Ol[s][t]:
                        Ol[s][t] = Cl[s][q] + Cr[q+1][t] + score[s][t]
                        BOl[s][t] = q
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
        return Or, Ol, Cr, Cl, BOr, BOl, BCr, BCl

    # def backtrack(self, BOr, BOl, BCr, BCl, i, j, tree):
        # # base case: empty span
        # if s == t:
        #     return

        # # get the split point and add an edge to the tree
        # q = BOr[s][t]  # or BOl[s][t]
        # tree[q].append((s, t))

        # # recursively backtrack over the two halves
        # self.backtrack(BOr, BOl, BCr, BCl, s, q, tree)
        # self.backtrack(BOr, BOl, BCr, BCl, q+1, t, tree)
    def _backtrack(self, i, j, lh, c, BCl, BCr, BOl, BOr, tree):
        """
            lh: right head = 0, left head = 1
            c: complete = 0, incomplete = 1
        """

        if i == j:
            return
        elif lh == 1 and c == 0:  # comp_lh
            k = BCl[i][j]
            tree[k] = i
            tree[j] = k
            self._backtrack(i, k, 1, 1, BCl, BCr, BOl, BOr, tree)
            self._backtrack(k, j, 1, 0, BCl, BCr, BOl, BOr, tree)
        if lh == 0 and c == 0:  # comp_rh
            k = BCr[i][j]
            tree[k] = j
            tree[i] = k
            self._backtrack(i, k, 0, 0, BCl, BCr, BOl, BOr, tree)
            self._backtrack(k, j, 0, 1, BCl, BCr, BOl, BOr, tree)
        elif lh == 1 and c == 1:  # incomp_lh
            k = BOl[i][j]
            tree[j] = i
            self._backtrack(i, k, 1, 0, BCl, BCr, BOl, BOr, tree)
            self._backtrack(k + 1, j, 0, 0, BCl, BCr, BOl, BOr, tree)
        elif lh == 0 and c == 1:  # incomp_rh
            k = BOr[i][j]
            tree[i] = j
            self._backtrack(i, k, 1, 0, BCl, BCr, BOl, BOr, tree)
            self._backtrack(k + 1, j, 0, 0, BCl, BCr, BOl, BOr, tree)

    def get_best_tree(self, score):

        N = len(score)
        Or, Ol, Cr, Cl, BOr, BOl, BCr, BCl = self.parse(score)
        # Backtrack to recover the highest-scoring tree
        tree = [[] for _ in range(N)]

        self._backtrack(0, N-1, 1, 0, BCl, BCr, BOl, BOr, tree)

        # Sort the arcs by their head index and return the tree
        # tree = sorted(arcs, key=lambda x: x[1])
        return tree


# decoder = Decoder()
# print(decoder.get_best_tree(score))
