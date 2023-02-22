import numpy as np
'''
inspired by "https://github.com/daandouwe/perceptron-dependency-parser/blob/master/eisner.py"
'''

# score = np.array([[0.0, 9, 10, 9], [-10000, 0.0, 20, 3],
#                  [-10000, 30, 0.0, 30], [-10000, 11, 0, 0.0]])

# score = np.array([[0.0, 10, 5, 15], [-10000, 0.0, 20, 15],
#                  [-10000, 25, 0.0, 25], [-10000, 30, 10, 0.0]])


class Decoder:

    def parse(self, score):
        # pass in score matrix
        # sentence includes  ROOT
        N = score.shape[0]

        # initialize the tables, third dim represents the head side
        open = np.zeros([N, N, 2])  # right = 1
        close = np.zeros([N, N, 2])  # right = 1

        # initialize back pointer tables
        open_bt = -np.ones([N, N, 2], dtype=int)  # right = 1
        close_bt = -np.ones([N, N, 2], dtype=int)  # right = 1

        # fill in the score of arcs
        for m in range(1, N):
            for s in range(0, N-m):
                t = s+m
                # open tables
                # left head
                open_val0 = close[s, s:t, 1] + \
                    close[(s+1):(t+1), t, 0] + score[t, s]
                open[s, t, 0] = np.max(open_val0)
                open_bt[s][t][0] = s + np.argmax(open_val0)
                # right head
                open_val1 = close[s, s:t, 1] + \
                    close[(s+1):(t+1), t, 0] + score[s, t]
                open[s, t, 1] = np.max(open_val1)
                open_bt[s][t][1] = s + np.argmax(open_val1)

                # closed tables
                # left head
                close_val0 = close[s, s:t, 0] + open[s:t, t, 0]
                close[s, t, 0] = np.max(close_val0)
                close_bt[s, t, 0] = s + np.argmax(close_val0)
                # right head
                close_val1 = open[s, (s+1):(t+1), 1] + close[(s+1):(t+1), t, 1]
                close[s, t, 1] = np.max(close_val1)
                close_bt[s, t, 1] = s + 1 + np.argmax(close_val1)

        # initial a list to represent the tree
        tree = -np.ones(N, dtype=int)
        self.backtrack(open_bt, close_bt, 0, N-1, 1, 1, tree)

        edge_set = []
        for i, head in enumerate(tree):
            if i == 0:
                continue
            else:
                edge_set.append((head, i))

        return edge_set

    def backtrack(self, open_bt, close_bt, s, t, direction, complete, tree):

        if s == t:
            return
        if complete:
            r = close_bt[s][t][direction]
            if direction == 0:
                self.backtrack(open_bt, close_bt, s, r, 0, 1, tree)
                self.backtrack(open_bt, close_bt, r, t, 0, 0, tree)
                return
            else:
                self.backtrack(open_bt, close_bt, s, r, 1, 0, tree)
                self.backtrack(open_bt, close_bt, r, t, 1, 1, tree)
                return
        else:
            r = open_bt[s][t][direction]
            if direction == 0:
                tree[s] = t
                self.backtrack(open_bt, close_bt, s, r, 1, 1, tree)
                self.backtrack(open_bt, close_bt, r+1, t, 0, 1, tree)
                return
            else:
                tree[t] = s
                self.backtrack(open_bt, close_bt, s, r, 1, 1, tree)
                self.backtrack(open_bt, close_bt, r+1, t, 0, 1, tree)
                return


# decoder = Decoder()
# print(decoder.parse(score))
