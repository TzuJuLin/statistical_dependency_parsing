from reader import Corpus, Sentence


class FeatureMap():

    def __init__(self, corpus) -> None:
        self.corpus = corpus
        self.feature_dict = {}
        self.gold_arc = []
        self.frozen = False
    '''
    get the arcs of the sentence
    # argument
    sent: one entry(sentence) in the corpus
    '''

    def get_arc(self, sent):
        arc_set = []
        for token in sent.tokens:
            if token.rel != "P" and token.form != "ROOT":
                arc_set.append((int(token.head), int(token.id)))
        return arc_set
    '''
    {feature1:0, feature2:1 }
    key is the feature, value is the feature_id, which is also unique and will later be used as the index of the feature in the weight vector
    '''

    def get_all_features(self):
        # a list of lists, each inner list represents a sentence and the entries are tuples that are the golden arcs

        i = 0
        for sent in self.corpus.sentences:
            arc_set = self.get_arc(sent)
            self.gold_arc.append(arc_set)
            for arc in arc_set:
                '''
                unigram features
                every index has to be -1 since the corpus do not include ROOT
                '''
                # p-word
                if "p-w:" + sent.tokens[arc[0]].form not in self.feature_dict:
                    self.feature_dict["p-w:" +
                                      sent.tokens[arc[0]].form] = i
                    i += 1

                # p-pos
                if "p-p:" + sent.tokens[arc[0]].pos not in self.feature_dict:
                    self.feature_dict["p-p:" + sent.tokens[arc[0]].pos] = i
                    i += 1

                # (p-word,p-pos)
                if "(p-w,p-p):" + str((
                        sent.tokens[arc[0]].form, sent.tokens[arc[0]].pos)) not in self.feature_dict:
                    self.feature_dict["(p-w,p-p):" + str((
                        sent.tokens[arc[0]].form, sent.tokens[arc[0]].pos))] = i
                    i += 1
                # c-word
                if "c-w:" + sent.tokens[arc[1]].form not in self.feature_dict:
                    self.feature_dict["c-w:" +
                                      sent.tokens[arc[1]].form] = i
                    i += 1

                # c-pos
                if "c-p:" + sent.tokens[arc[1]].pos not in self.feature_dict:
                    self.feature_dict["c-p:" + sent.tokens[arc[1]].pos] = i
                    i += 1

                # (c-word, c-pos)
                if "(c-w,c-p):" + str((
                        sent.tokens[arc[1]].form, sent.tokens[arc[1]].pos)) not in self.feature_dict:
                    self.feature_dict["(c-w,c-p):" + str(
                        (sent.tokens[arc[1]].form, sent.tokens[arc[1]].pos))] = i
                    i += 1
                '''
                basic bigram features
                '''
                # (p-word, p-pos, c-word, c-pos)
                if "(p-w,p-p,c-w,c-p):" + str((sent.tokens[arc[0]].form, sent.tokens[arc[0]].pos, sent.tokens[arc[1]].form, sent.tokens[arc[1]].pos))not in self.feature_dict:
                    self.feature_dict["(p-w,p-p,c-w,c-p):" + str((sent.tokens[arc[0]].form,
                                                                  sent.tokens[arc[0]].pos, sent.tokens[arc[1]].form, sent.tokens[arc[1]].pos))] = i
                    i += 1

                # (p-pos, c-word, c-pos)
                if "(p-p,c-w,c-p):" + str((
                        sent.tokens[arc[0]].pos, sent.tokens[arc[1]].form, sent.tokens[arc[1]].pos)) not in self.feature_dict:
                    self.feature_dict["(p-p,c-w,c-p):" + str((
                        sent.tokens[arc[0]].pos, sent.tokens[arc[1]].form, sent.tokens[arc[1]].pos))] = i
                    i += 1
                # (p-word, c-word, c-pos)
                if "(p-w,c-w,c-p):" + str((
                        sent.tokens[arc[0]].form, sent.tokens[arc[1]].form, sent.tokens[arc[1]].pos)) not in self.feature_dict:
                    self.feature_dict["(p-w,c-w,c-p):" + str((
                        sent.tokens[arc[0]].form, sent.tokens[arc[1]].form, sent.tokens[arc[1]].pos))] = i
                    i += 1

                # (p-word, p-pos, c-pos)
                if "(p-w,p-p,c-p):" + str((sent.tokens[arc[0]].form, sent.tokens[arc[0]].pos, sent.tokens[arc[1]].pos)) not in self.feature_dict:
                    self.feature_dict["(p-w,p-p,c-p):" + str(
                        (sent.tokens[arc[0]].form, sent.tokens[arc[0]].pos, sent.tokens[arc[1]].pos))] = i
                    i += 1
                # (p-word, p-pos, c-word)
                if "(p-w,p-p,c-w):" + str((sent.tokens[arc[0]].form, sent.tokens[arc[0]].pos, sent.tokens[arc[1]].form)) not in self.feature_dict:
                    self.feature_dict["(p-w,p-p,c-w):" + str((sent.tokens[arc[0]].form,
                                                              sent.tokens[arc[0]].pos, sent.tokens[arc[1]].form))] = i
                    i += 1
                # (p-word, c-word)
                if "(p-w,c-w):" + str((sent.tokens[arc[0]].form, sent.tokens[arc[1]].form)) not in self.feature_dict:
                    self.feature_dict["(p-w,c-w):" + str(
                        (sent.tokens[arc[0]].form, sent.tokens[arc[1]].form))] = i
                    i += 1

                # (p-pos, c-pos)
                if "(p-p,c-p):" + str((
                        sent.tokens[arc[0]].pos, sent.tokens[arc[1]].pos)) not in self.feature_dict:
                    self.feature_dict["(p-p,c-p):" + str((
                        sent.tokens[arc[0]].pos, sent.tokens[arc[1]].pos))] = i
                    i += 1

                '''
                In between POS features
                get all the POS tag between the head and child
                '''
                # (p-pod, b-pos, c-pos)
                # check if  the parent and child are immediate neighbors
                if abs(arc[1]-arc[0]) != 1:
                    # initialize a list that has the p-pos as first entry
                    # if child is at the right of parent
                    if arc[0] < arc[1]:
                        for i in range(arc[0]+1, arc[1]):
                            if "b-w:" + sent.tokens[i].form not in self.feature_dict:
                                self.feature_dict["b-w:" +
                                                  sent.tokens[i].form] = i
                                i += 1
                    # if child is at the left (bigger index than parent)
                    else:
                        for i in range(arc[1]-1, arc[0]):
                            if "b-w:" + sent.tokens[i].form not in self.feature_dict:
                                self.feature_dict["b-w:" +
                                                  sent.tokens[i].form] = i
                                i += 1

                    '''
                    surrounding word POS features
                    '''
                    # (p-pos, p-pos+1, c-pos-1, c-pos)
                    if "p-p,p-p+1,c-p-1,c-p" + str((sent.tokens[arc[0]].pos, sent.tokens[arc[0]+1].pos, sent.tokens[arc[1]-1].pos, sent.tokens[arc[1]].pos)) not in self.feature_dict:
                        self.feature_dict["p-p,p-p+1,c-p-1,c-p" + str(
                            (sent.tokens[arc[0]].pos, sent.tokens[arc[0]+1].pos, sent.tokens[arc[1]-1].pos, sent.tokens[arc[1]].pos))] = i
                        i += 1

                    # (p-pos, p-pos-1, c-pos-1, c-pos)
                    if "p-p,p-p-1,c-p-1,c-p" + str((sent.tokens[arc[0]].pos, sent.tokens[arc[0]-1].pos, sent.tokens[arc[1]-1].pos, sent.tokens[arc[1]].pos)) not in self.feature_dict:
                        self.feature_dict["p-p,p-p-1,c-p-1,c-p" + str(
                            (sent.tokens[arc[0]].pos, sent.tokens[arc[0]-1].pos, sent.tokens[arc[1]-1].pos, sent.tokens[arc[1]].pos))] = i
                        i += 1
                    # (p-pos, p-pos+1, c-pos, c-pos+1)
                    if "p-p,p-p+1,c-p,c-p+1" + str((sent.tokens[arc[0]].pos, sent.tokens[arc[0]+1].pos, sent.tokens[arc[1]].pos, sent.tokens[arc[1]+1].pos)) not in self.feature_dict:
                        self.feature_dict["p-p,p-p+1,c-p,c-p+1" + str(
                            (sent.tokens[arc[0]].pos, sent.tokens[arc[0]+1].pos, sent.tokens[arc[1]].pos, sent.tokens[arc[1]+1].pos))] = i
                        i += 1

                     # (p-pos-1, p-pos, c-pos, c-pos+1)
                    if "p-p-1,p-p,c-p,c-p+1" + str((sent.tokens[arc[0]-1].pos, sent.tokens[arc[0]].pos, sent.tokens[arc[1]].pos, sent.tokens[arc[1]+1].pos)) not in self.feature_dict:
                        self.feature_dict["p-p,p-p+1,c-p,c-p+1" + str(
                            (sent.tokens[arc[0]-1].pos, sent.tokens[arc[0]].pos, sent.tokens[arc[1]].pos, sent.tokens[arc[1]+1].pos))] = i
                        i += 1
        return self.feature_dict

        '''
        extract the features from an arc
        returns a list of existed feature ids
        '''

    def extract(self, arc, sent):
        # only one sentence passed in

        feature_id = []
        if "p-w:" + sent.tokens[arc[0]].form in self.feature_dict:
            feature_id.append(
                self.feature_dict["p-w:" + sent.tokens[arc[0]].form])
        if "p-p:" + sent.tokens[arc[0]].pos in self.feature_dict:
            feature_id.append(
                self.feature_dict["p-w:" + sent.tokens[arc[0]].pos])
        if "(p-w,p-p):" + str((
                sent.tokens[arc[0]].form, sent.tokens[arc[0]].pos)) in self.feature_dict:
            feature_id.append(self.feature_dict["(p-w,p-p):" + str((
                sent.tokens[arc[0]].form, sent.tokens[arc[0]].pos))])
        if "c-w:" + sent.tokens[arc[1]].form in self.feature_dict:
            feature_id.append(
                self.feature_dict["c-w:" + sent.tokens[arc[1]].form])
        if "c-p:" + sent.tokens[arc[1]].pos in self.feature_dict:
            feature_id.append(
                self.feature_dict["c-p:" + sent.tokens[arc[1]].pos])
        if "(c-w,c-p):" + str((
                sent.tokens[arc[1]].form, sent.tokens[arc[1]].pos)) in self.feature_dict:
            feature_id.append(self.feature_dict["(c-w,c-p):" + str((
                sent.tokens[arc[1]].form, sent.tokens[arc[1]].pos))])
        if "(p-w,p-p,c-w,c-p):" + str((sent.tokens[arc[0]].form, sent.tokens[arc[0]].pos, sent.tokens[arc[1]].form, sent.tokens[arc[1]].pos)) in self.feature_dict:
            feature_id.append(self.feature_dict["(p-w,p-p,c-w,c-p):" + str(
                (sent.tokens[arc[0]].form, sent.tokens[arc[0]].pos, sent.tokens[arc[1]].form, sent.tokens[arc[1]].pos))])
        if "(p-p,c-w,c-p):" + str((
                sent.tokens[arc[0]].pos, sent.tokens[arc[1]].form, sent.tokens[arc[1]].pos)) in self.feature_dict:
            feature_id.append(self.feature_dict["(p-p,c-w,c-p):" + str((
                sent.tokens[arc[0]].pos, sent.tokens[arc[1]].form, sent.tokens[arc[1]].pos))])
        if "(p-w,c-w,c-p):" + str((
                sent.tokens[arc[0]].form, sent.tokens[arc[1]].form, sent.tokens[arc[1]].pos)) in self.feature_dict:
            feature_id.append(self.feature_dict["(p-w,c-w,c-p):" + str((
                sent.tokens[arc[0]].form, sent.tokens[arc[1]].form, sent.tokens[arc[1]].pos))])
        if "(p-w,p-p,c-p):" + str((sent.tokens[arc[0]].form, sent.tokens[arc[0]].pos, sent.tokens[arc[1]].pos)) in self.feature_dict:
            feature_id.append(self.feature_dict["(p-w,p-p,c-p):" + str(
                (sent.tokens[arc[0]].form, sent.tokens[arc[0]].pos, sent.tokens[arc[1]].pos))])
        if "(p-w,p-p,c-w):" + str((sent.tokens[arc[0]].form, sent.tokens[arc[0]].pos, sent.tokens[arc[1]].form)) in self.feature_dict:
            feature_id.append(self.feature_dict["(p-w,p-p,c-w):" + str(
                (sent.tokens[arc[0]].form, sent.tokens[arc[0]].pos, sent.tokens[arc[1]].form))])
        if "(p-w,c-w):" + str((sent.tokens[arc[0]].form, sent.tokens[arc[1]].form)) in self.feature_dict:
            feature_id.append(
                self.feature_dict["(p-w,c-w):" + str((sent.tokens[arc[0]].form, sent.tokens[arc[1]].form))])
        if "(p-p,c-p):" + str((
                sent.tokens[arc[0]].pos, sent.tokens[arc[1]].pos)) in self.feature_dict:
            feature_id.append(self.feature_dict["(p-p,c-p):" + str((
                sent.tokens[arc[0]].pos, sent.tokens[arc[1]].pos))])
        if "b-w:" + sent.tokens[i].form in self.feature_dict:
            feature_id.append(
                self.feature_dict["b-w:" + sent.tokens[i].form])
        if "p-p,p-p+1,c-p-1,c-p" + str((sent.tokens[arc[0]].pos, sent.tokens[arc[0]+1].pos, sent.tokens[arc[1]-1].pos, sent.tokens[arc[1]].pos)) in self.feature_dict:
            feature_id.append(self.feature_dict["p-p,p-p+1,c-p-1,c-p" + str(
                (sent.tokens[arc[0]].pos, sent.tokens[arc[0]+1].pos, sent.tokens[arc[1]-1].pos, sent.tokens[arc[1]].pos))])
        if "p-p,p-p-1,c-p-1,c-p" + str((sent.tokens[arc[0]].pos, sent.tokens[arc[0]-1].pos, sent.tokens[arc[1]-1].pos, sent.tokens[arc[1]].pos)) in self.feature_dict:
            feature_id.append(self.feature_dict["p-p,p-p-1,c-p-1,c-p" + str(
                (sent.tokens[arc[0]].pos, sent.tokens[arc[0]-1].pos, sent.tokens[arc[1]-1].pos, sent.tokens[arc[1]].pos))])
        if "p-p,p-p+1,c-p,c-p+1" + str((sent.tokens[arc[0]].pos, sent.tokens[arc[0]+1].pos, sent.tokens[arc[1]].pos, sent.tokens[arc[1]+1].pos)) in self.feature_dict:
            feature_id.append(self.feature_dict["p-p,p-p+1,c-p,c-p+1" + str(
                (sent.tokens[arc[0]].pos, sent.tokens[arc[0]+1].pos, sent.tokens[arc[1]].pos, sent.tokens[arc[1]+1].pos))])
        if "p-p-1,p-p,c-p,c-p+1" + str((sent.tokens[arc[0]-1].pos, sent.tokens[arc[0]].pos, sent.tokens[arc[1]].pos, sent.tokens[arc[1]+1].pos)) in self.feature_dict:
            feature_id.append(self.feature_dict["p-p-1,p-p,c-p,c-p+1" + str(
                (sent.tokens[arc[0]-1].pos, sent.tokens[arc[0]].pos, sent.tokens[arc[1]].pos, sent.tokens[arc[1]+1].pos))])
        return feature_id

    # test = FeatureDict("/Users/lintzuru/Desktop/WS22:23/parsing/test_feature")
    # print(test.extract_feature())
