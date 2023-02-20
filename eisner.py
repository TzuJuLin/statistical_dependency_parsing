# import numpy as np


# score = np.array([[0.0, 9, 10, 9], [-10000, 0.0, 20, 3],
#                  [-10000, 30, 0.0, 30], [-10000, 11, 0, 0.0]])

# # score = np.array([[0.0, 10, 5, 15], [-10000, 0.0, 20, 15],
# #                  [-10000, 25, 0.0, 25], [-10000, 30, 10, 0.0]])


# class Decoder:

#     def parse(self, score):
#         # pass score matrix
#         # sentence includes  ROOT
#         row, col = score.shape
#         assert col == row, 'must be square matrix'

#         N = row

#         # initialize
#         Or = np.zeros([N, N], dtype=int)
#         Ol = np.zeros([N, N], dtype=int)
#         Cr = np.zeros([N, N], dtype=int)
#         Cl = np.zeros([N, N], dtype=int)

#         # initialize back pointer tables
#         BOr = np.zeros([N, N], dtype=int)
#         BOl = np.zeros([N, N], dtype=int)
#         BCr = np.zeros([N, N], dtype=int)
#         BCl = np.zeros([N, N], dtype=int)

#         for m in range(1, N):
#             for s in range(0, N-m):
#                 t = s+m

#                 for q in range(s, t):
#                     if Cl[s][q] + Cr[q+1][t] + score[t][s] >= Or[s][t]:
#                         Or[s][t] = Cl[s][q] + Cr[q+1][t] + score[t][s]
#                         BOr[s][t] = q
#                     if Cl[s][q] + Cr[q+1][t] + score[t][s] < 0:
#                         Or[s][t] = -10000
#                         BOr[s][t] = 0
#                     if Cl[s][q] + Cr[q+1][t] + score[s][t] >= Ol[s][t]:
#                         Ol[s][t] = Cl[s][q] + Cr[q+1][t] + score[s][t]
#                         BOl[s][t] = q
#                     if Cr[s][q] + Or[q][t] >= Cr[s][t]:
#                         Cr[s][t] = Cr[s][q] + Or[q][t]
#                         BCr[s][t] = q
#                     if Cr[s][q] + Or[q][t] < 0:
#                         Cr[s][t] = -10000
#                         BCr[s][t] = 0
#                 for k in range(s+1, t+1):
#                     if Ol[s][k] + Cl[k][t] >= Cl[s][t]:
#                         Cl[s][t] = Ol[s][k] + Cl[k][t]
#                         BCl[s][t] = k

#                 # for intermediate check
#                 # print("m:" + str(m) + " s: " + str(s) + " t: " + str(t))
#                 # print(Or, Ol, Cr, Cl)
#         return Or, Ol, Cr, Cl, BOr, BOl, BCr, BCl

#     # def backtrack(self, BOr, BOl, BCr, BCl, i, j, tree):
#         # # base case: empty span
#         # if s == t:
#         #     return

#         # # get the split point and add an edge to the tree
#         # q = BOr[s][t]  # or BOl[s][t]
#         # tree[q].append((s, t))

#         # # recursively backtrack over the two halves
#         # self.backtrack(BOr, BOl, BCr, BCl, s, q, tree)
#         # self.backtrack(BOr, BOl, BCr, BCl, q+1, t, tree)
#     def _backtrack(self, i, j, lh, c, BCl, BCr, BOl, BOr, tree):
#         """
#             lh: right head = 0, left head = 1
#             c: complete = 0, incomplete = 1
#         """

#         if i == j:
#             return
#         elif lh == 1 and c == 0:  # comp_lh
#             k = BCl[i][j]
#             tree[k] = i
#             tree[j] = k
#             self._backtrack(i, k, 1, 1, BCl, BCr, BOl, BOr, tree)
#             self._backtrack(k, j, 1, 0, BCl, BCr, BOl, BOr, tree)
#         if lh == 0 and c == 0:  # comp_rh
#             k = BCr[i][j]
#             tree[k] = j
#             tree[i] = k
#             self._backtrack(i, k, 0, 0, BCl, BCr, BOl, BOr, tree)
#             self._backtrack(k, j, 0, 1, BCl, BCr, BOl, BOr, tree)
#         elif lh == 1 and c == 1:  # incomp_lh
#             k = BOl[i][j]
#             tree[j] = i
#             self._backtrack(i, k, 1, 0, BCl, BCr, BOl, BOr, tree)
#             self._backtrack(k + 1, j, 0, 0, BCl, BCr, BOl, BOr, tree)
#         elif lh == 0 and c == 1:  # incomp_rh
#             k = BOr[i][j]
#             tree[i] = j
#             self._backtrack(i, k, 1, 0, BCl, BCr, BOl, BOr, tree)
#             self._backtrack(k + 1, j, 0, 0, BCl, BCr, BOl, BOr, tree)

#     def get_best_tree(self, score):

#         N = len(score)
#         Or, Ol, Cr, Cl, BOr, BOl, BCr, BCl = self.parse(score)
#         # Backtrack to recover the highest-scoring tree
#         tree = [[] for _ in range(N)]

#         self._backtrack(0, N-1, 1, 0, BCl, BCr, BOl, BOr, tree)

#         # Sort the arcs by their head index and return the tree
#         # tree = sorted(arcs, key=lambda x: x[1])
#         return tree


# # decoder = Decoder()
# # print(decoder.get_best_tree(score))


'''
------------------
'''

import numpy as np
import time


# score = np.array([[0.0, 9, 10, 9], [-10000, 0.0, 20, 3],
#                  [-10000, 30, 0.0, 30], [-10000, 11, 0, 0.0]])

score = np.array([[0.0, 10, 5, 15], [-10000, 0.0, 20, 15],
                 [-10000, 25, 0.0, 25], [-10000, 30, 10, 0.0]])

score100 = np.random.rand(10, 10)
score200 = np.random.rand(200, 200)

L, R = 0, 1
I, C = 0, 1
DIRECTIONS = (L, R)
COMPLETENESS = (I, C)
NEG_INF = -float('inf')


class Span(object):
    def __init__(self, left_idx, right_idx, head_side, complete):
        self.data = (left_idx, right_idx, head_side, complete)

    @property
    def left_idx(self):
        return self.data[0]

    @property
    def right_idx(self):
        return self.data[1]

    @property
    def head_side(self):
        return self.data[2]

    @property
    def complete(self):
        return self.data[3]

    def __str__(self):
        return "({}, {}, {}, {})".format(
            self.left_idx,
            self.right_idx,
            "L" if self.head_side == L else "R",
            "C" if self.complete == C else "I",
        )

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        return isinstance(other, Span) and hash(other) == hash(self)


class Decoder:

    def parse(self, score):
        # pass score matrix
        # sentence includes  ROOT
        N = score.shape[0]
        btp = {}
        dp_s = {}
        # Init
        for i in range(N):
            for j in range(i + 1, N):
                for dir in DIRECTIONS:
                    for comp in COMPLETENESS:
                        dp_s[Span(i, j, dir, comp)] = NEG_INF

        # base case
        for i in range(N):
            for dir in DIRECTIONS:
                dp_s[Span(i, i, dir, C)] = 0.
                btp[Span(i, i, dir, C)] = None

        rules = [
            # span_shape_tuple := (span_direction, span_completeness),
            # rule := (span_shape, (left_subspan_shape, right_subspan_shape))
            ((L, I), ((R, C), (L, C))),
            ((R, I), ((R, C), (L, C))),
            ((L, C), ((L, C), (L, I))),
            ((R, C), ((R, I), (R, C))),
        ]

        for size in range(1, N):
            for i in range(0, N - size):
                j = i + size
                for rule in rules:
                    ((dir, comp), ((l_dir, l_comp), (r_dir, r_comp))) = rule

                    if comp == I:
                        edge_score = score[i, j] if (dir == R) else score[j, i]
                        k_start, k_end = (i, j)
                        offset = 1
                    else:
                        edge_score = 0.
                        k_start, k_end = (i + 1, j + 1) if dir == R else (i, j)
                        offset = 0

                    span = Span(i, j, dir, comp)
                    for k in range(k_start, k_end):
                        l_span = Span(i, k, l_dir, l_comp)
                        r_span = Span(k + offset, j, r_dir, r_comp)
                        s = edge_score + dp_s[l_span] + dp_s[r_span]
                        if s > dp_s[span]:
                            dp_s[span] = s
                            btp[span] = (l_span, r_span)

        # recover tree
        return self.back_track(btp, Span(0, N - 1, R, C), set())

    def back_track(self, btp, span, edge_set):
        if span.complete == I:
            if span.head_side == L:
                edge = (span.right_idx, span.left_idx)
            else:
                edge = (span.left_idx, span.right_idx)
            edge_set.add(edge)

        if btp[span] is not None:
            l_span, r_span = btp[span]

            self.back_track(btp, l_span, edge_set)
            self.back_track(btp, r_span, edge_set)
        else:
            return

        return edge_set

        # # initialize
        # Or = np.zeros([N, N], dtype=int)
        # Ol = np.zeros([N, N], dtype=int)
        # Cr = np.zeros([N, N], dtype=int)
        # Cl = np.zeros([N, N], dtype=int)

        # # initialize back pointer tables
        # BOr = np.zeros([N, N], dtype=int)
        # BOl = np.zeros([N, N], dtype=int)
        # BCr = np.zeros([N, N], dtype=int)
        # BCl = np.zeros([N, N], dtype=int)

        # for m in range(1, N):
        #     for s in range(0, N-m):
        #         t = s+m

        #         for q in range(s, t):
        #             if Cl[s][q] + Cr[q+1][t] + score[t][s] >= Or[s][t]:
        #                 Or[s][t] = Cl[s][q] + Cr[q+1][t] + score[t][s]
        #                 BOr[s][t] = q
        #             if Cl[s][q] + Cr[q+1][t] + score[t][s] < 0:
        #                 Or[s][t] = -10000
        #                 BOr[s][t] = 0
        #             if Cl[s][q] + Cr[q+1][t] + score[s][t] >= Ol[s][t]:
        #                 Ol[s][t] = Cl[s][q] + Cr[q+1][t] + score[s][t]
        #                 BOl[s][t] = q
        #             if Cr[s][q] + Or[q][t] >= Cr[s][t]:
        #                 Cr[s][t] = Cr[s][q] + Or[q][t]
        #                 BCr[s][t] = q
        #             if Cr[s][q] + Or[q][t] < 0:
        #                 Cr[s][t] = -10000
        #                 BCr[s][t] = 0
        #         for k in range(s+1, t+1):
        #             if Ol[s][k] + Cl[k][t] >= Cl[s][t]:
        #                 Cl[s][t] = Ol[s][k] + Cl[k][t]
        #                 BCl[s][t] = k

        # return BOr, BOl, BCr, BCl

    # def _backtrack(self, i, j, lh, c, BCl, BCr, BOl, BOr, tree):
    #     """
    #         lh: right head = 0, left head = 1
    #         c: complete = 0, incomplete = 1
    #     """
    #     if c == 0:
    #         if lh == 1:
    #             k = BOl[i][j]
    #             tree[k] = i
    #         else:
    #             k = BOr[i][j]
    #             tree[k] = j
    #         if
        # if i == j:
        #     return
        # elif lh == 1 and c == 0:  # Cl
        #     k = BCl[i][j]
        #     tree[k] = i
        #     tree[j] = k
        #     self._backtrack(i, k, 1, 1, BCl, BCr, BOl, BOr, tree)
        #     self._backtrack(k, j, 1, 0, BCl, BCr, BOl, BOr, tree)
        # if lh == 0 and c == 0:  # Cr
        #     k = BCr[i][j]
        #     tree[k] = j
        #     tree[i] = k
        #     self._backtrack(i, k, 0, 0, BCl, BCr, BOl, BOr, tree)
        #     self._backtrack(k, j, 0, 1, BCl, BCr, BOl, BOr, tree)
        # elif lh == 1 and c == 1:  # Ol
        #     k = BOl[i][j]
        #     tree[j] = i
        #     self._backtrack(i, k, 1, 0, BCl, BCr, BOl, BOr, tree)
        #     self._backtrack(k + 1, j, 0, 0, BCl, BCr, BOl, BOr, tree)
        # elif lh == 0 and c == 1:  # Or
        #     k = BOr[i][j]
        #     tree[i] = j
        #     self._backtrack(i, k, 1, 0, BCl, BCr, BOl, BOr, tree)
        #     self._backtrack(k + 1, j, 0, 0, BCl, BCr, BOl, BOr, tree)

    def get_best_tree(self, score):

        N = len(score)
    #     BOr, BOl, BCr, BCl = self.parse(score)
    #     # Backtrack to recover the highest-scoring tree
    #     tree = [[] for _ in range(N)]
    #     #lefthead, complete
    #     self._backtrack(0, N-1, 0, 1, BCl, BCr, BOl, BOr, tree)
        start = time.time()
        edge_set = self.parse(score)
        end = time.time()
        # print("執行時間8:%f 秒" % (end - start))
        # print(edge_set)
        # tree = [[]for _ in range(N)]
        # for edge in edge_set:
        #     tree[edge[1]] = edge[0]
        return edge_set

    #     return tree


# decoder = Decoder()
# print(decoder.get_best_tree(score100))

# start = time.time()

# decoder.get_best_tree(score100)
# end = time.time()
# print("執行時間：%f 秒" % (end - start))
# print(decoder.get_best_tree(score100))
# start = time.time()

# decoder.get_best_tree(score200)
# end = time.time()
# print("執行時間：%f 秒" % (end - start))
