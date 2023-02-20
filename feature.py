from reader import Corpus
import numpy as np
import time


class FeatureMap():

    def __init__(self, corpus) -> None:
        self.corpus = corpus
        self.feature_dict = {}
        self.frozen = False
        self.i = 0

    def feature_mapping(self, arc, sent):
        # only one sentence passed in

        feature_id = []
        if arc[0] > arc[1]:
            dir = 'L'
        else:
            dir = 'R'
        dis = str(abs(arc[0]-arc[1]))
        p_w = sent.tokens[arc[0]].form
        p_p = sent.tokens[arc[0]].pos
        c_w = sent.tokens[arc[1]].form
        c_p = sent.tokens[arc[1]].pos

        feature_template = [
            " ".join(("p-w:", p_w, dis, dir)),
            " ".join(("p-p:", p_p, dis, dir)),
            " ".join(("p-w,p-p:",
                      p_w, p_p, dis, dir)),
            " ".join(("c-w:", c_w, dis, dir)),
            " ".join(("c-p:", c_p, dis, dir)),
            " ".join(("c-w,c-p:",
                      c_w, c_p, dis, dir)),
            " ".join(("p-w,p-p,c-w,c-p:", p_w, p_p, c_w, c_p, dis, dir)),
            " ".join(("p-p,c-w,c-p:", p_p, c_w, c_p, dis, dir)),
            " ".join(("p-w,c-w,c-p:", p_w, c_w, c_p, dis, dir)),
            " ".join(("p-w,p-p,c-p:", p_w, p_p, c_p, dis, dir)),
            " ".join(("p-w,p-p,c-w:", p_w, p_p, c_w, dis, dir)),
            " ".join(("p-w,c-w:", p_w, c_w, dis, dir)),
            " ".join(("p-p,c-p:", p_p, c_p, dis, dir))
        ]

        if arc[0] != 0:
            p_p_min_1 = sent.tokens[arc[0]-1].pos
            c_p_min_1 = sent.tokens[arc[1]-1].pos
            feature_template.append(
                " ".join(("p-p,p-p-1,c-p-1,c-p:", p_p, p_p_min_1, c_p_min_1, c_p)))
        if arc[0] != len(sent.tokens)-1:
            p_p_add_1 = sent.tokens[arc[0]+1].pos
            c_p_min_1 = sent.tokens[arc[1]-1].pos
            feature_template.append(
                " ".join(("p-p,p-p+1,c-p-1,c-p:", p_p, p_p_add_1, c_p_min_1, c_p, dis, dir)))
        if arc[0] != len(sent.tokens)-1 and arc[1] != len(sent.tokens)-1:
            c_p_add_1 = sent.tokens[arc[1]+1].pos
            feature_template.append(
                " ".join(("p-p,p-p+1,c-p,c-p+1:", p_p, p_p_add_1, c_p, c_p_add_1, dis, dir)))
        if arc[0] != 0 and arc[1] != len(sent.tokens)-1:
            c_p_add_1 = sent.tokens[arc[1]+1].pos
            feature_template.append(
                " ".join(("p-p-1,p-p,c-p,c-p+1:", p_p_min_1, p_p, c_p, c_p_add_1, dis, dir)))
        if dis != "1":
            betweens = sent.tokens[arc[0]+1:arc[1]
                                   ] if arc[0] < arc[1] else sent.tokens[arc[1]+1:arc[0]]
            feature_template.append(
                " ".join(("b-w:", between.pos, dis, dir)) for between in betweens)

        for feature in feature_template:
            if feature in self.feature_dict:
                feature_id.append(self.feature_dict[feature])
            else:
                if not self.frozen:
                    self.feature_dict[feature] = self.i
                    self.i += 1

        return np.array(feature_id, dtype=int)
