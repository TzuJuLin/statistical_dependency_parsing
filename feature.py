
class FeatureMap():
        
    def __init__(self, corpus) -> None:
            self.corpus = corpus
            self.feature_dict = {}
            self.frozen = False
            self.i = 0
    
    #create the feature map of the passed in corpus
    def create_feat(self):

        for sent in self.corpus.sentences:
            tree = sent.get_full_tree()
            for arc in tree:
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
                    " ".join(("p-w,p-p:", p_w, p_p, dis, dir)),
                    " ".join(("c-w:", c_w, dis, dir)),
                    " ".join(("c-p:", c_p, dis, dir)),
                    " ".join(("c-w,c-p:",c_w, c_p, dis, dir)),
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
                    if arc[0] < arc[1]:
                        betweens = [tok.pos for tok in sent.tokens[arc[0]+1:arc[1]]]
                    else:
                        betweens = [tok.pos for tok in sent.tokens[arc[1]+1:arc[0]]]
                    for between in betweens:
                        feature_template.append(" ".join(("b-w:", between, dis, dir)))

                for feature in feature_template:
                    if feature not in self.feature_dict:
                        self.feature_dict[feature] = self.i
                        self.i += 1

 

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
                                " ".join(("p-w,p-p,c-w,c-p:",p_w, p_p, c_w, c_p, dis, dir)),
                                " ".join(("p-p,c-w,c-p:", p_p, c_w, c_p, dis, dir)),
                                " ".join(("p-w,c-w,c-p:", p_w, c_w, c_p, dis, dir)),
                                " ".join(("p-w,p-p,c-p:",p_w, p_p, c_p, dis, dir)),
                                " ".join(("p-w,p-p,c-w:",p_w, p_p, c_w, dis, dir)),
                                " ".join(("p-w,c-w:",p_w, c_w, dis, dir)),
                                " ".join(("p-p,c-p:",p_p, c_p, dis, dir))
                                ]         
                if arc[0] != 0:
                    p_p_min_1 = sent.tokens[arc[0]-1].pos
                    c_p_min_1 = sent.tokens[arc[1]-1].pos
                    feature_template.append(" ".join(("p-p,p-p-1,c-p-1,c-p:", p_p,p_p_min_1,c_p_min_1, c_p,dis, dir)))
                if arc[0] != len(sent.tokens)-1:
                    p_p_add_1 = sent.tokens[arc[0]+1].pos
                    c_p_min_1 = sent.tokens[arc[1]-1].pos
                    feature_template.append(" ".join(("p-p,p-p+1,c-p-1,c-p:",p_p,p_p_add_1, c_p_min_1, c_p, dis, dir)))
                if arc[0] != len(sent.tokens)-1 and arc[1] != len(sent.tokens)-1:
                    c_p_add_1 = sent.tokens[arc[1]+1].pos
                    feature_template.append(" ".join(("p-p,p-p+1,c-p,c-p+1:",p_p, p_p_add_1, c_p, c_p_add_1, dis, dir)))
                if arc[0] != 0 and arc[1] != len(sent.tokens)-1:
                    c_p_add_1 = sent.tokens[arc[1]+1].pos
                    feature_template.append(" ".join(("p-p-1,p-p,c-p,c-p+1:",p_p_min_1, p_p, c_p, c_p_add_1, dis, dir)))
                if dis != "1":
                    if arc[0] < arc[1]:
                        betweens = [tok.pos for tok in sent.tokens[arc[0]+1:arc[1]]]
                    else:
                        betweens = [tok.pos for tok in sent.tokens[arc[1]+1:arc[0]]]
                    for between in betweens:
                        feature_template.append(" ".join(("b-w:", between, dis, dir)))
                if  not self.frozen:
                    for feature in feature_template:
                        try:
                            feature_id.append(self.feature_dict[feature])
                        except KeyError:
                             continue
                else:    
                    if feature in self.feature_dict:
                        feature_id.append(self.feature_dict[feature])
        
                return feature_id

