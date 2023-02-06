from reader import Sentence, Corpus


class FeatureDict():

    def __init__(self, corpus_path) -> None:
        self.corpus = Corpus(corpus_path)
        self.corpus.add_sentence()
        self.feature_dict = {}
    '''
    get the arcs of the sentence
    # argument
    sent: one entry(sentence) in the corpus
    '''

    def get_arc(self, sent):
        arc_set = []
        for i in range(len(sent.id)):
            if sent.rel[i] != "P" and sent.rel[i] != "ROOT":
                arc_set.append((int(sent.head[i]), int(sent.id[i])))
        return arc_set

    def get_feature(self):
        for i in range(len(self.corpus.sentences)):
            sentence = self.corpus.sentences[i]
            arc_set = self.get_arc(sentence)
            for arc in arc_set:
                '''
                unigram features
                every index has to be -1 since the corpus do not include ROOT
                '''
                # p-word
                if sentence.form[arc[0]-1] not in self.feature_dict:
                    self.feature_dict[sentence.form[arc[0]-1]] = 1
                # p-pos
                if sentence.pos[arc[0]-1] not in self.feature_dict:
                    self.feature_dict[sentence.pos[arc[0]-1]] = 1
                # (p-word,p-pos)
                if (sentence.form[arc[0]-1], sentence.pos[arc[0]-1]) not in self.feature_dict:
                    self.feature_dict[(sentence.form[arc[0]-1],
                                       sentence.pos[arc[0]-1])] = 1
                # c-word
                if sentence.form[arc[1]-1] not in self.feature_dict:
                    self.feature_dict[sentence.form[arc[0]-1]] = 1
                # c-pos
                if sentence.pos[arc[1]-1] not in self.feature_dict:
                    self.feature_dict[sentence.pos[arc[0]-1]] = 1
                # (c-word, c-pos)
                if (sentence.form[arc[1]-1], sentence.pos[arc[1]-1]) not in self.feature_dict:
                    self.feature_dict[(sentence.form[arc[1]-1],
                                       sentence.pos[arc[1]-1])] = 1
                '''
                basic bigram features
                '''
                # (p-word, p-pos, c-word, c-pos)
                if (sentence.form[arc[0]-1], sentence.pos[arc[0]-1], sentence.form[arc[1]-1], sentence.pos[arc[1]-1]) not in self.feature_dict:
                    self.feature_dict[(sentence.form[arc[0]-1], sentence.pos[arc[0]-1],
                                       sentence.form[arc[1]-1], sentence.pos[arc[1]-1])] = 1
                # (p-pos, c-word, c-pos)
                if (sentence.pos[arc[0]-1], sentence.form[arc[1]-1], sentence.pos[arc[1]-1]) not in self.feature_dict:
                    self.feature_dict[sentence.pos[arc[0]-1],
                                      sentence.form[arc[1]-1], sentence.pos[arc[1]-1]] = 1
                # (p-word, c-word, c-pos)
                if (sentence.form[arc[0]-1], sentence.form[arc[1]-1], sentence.pos[arc[1]-1]) not in self.feature_dict:
                    self.feature_dict[sentence.form[arc[0]-1],
                                      sentence.form[arc[1]-1], sentence.pos[arc[1]-1]] = 1
                # (p-word, p-pos, c-pos)
                if (sentence.form[arc[0]-1], sentence.pos[arc[0]-1], sentence.pos[arc[1]-1]) not in self.feature_dict:
                    self.feature_dict[(
                        sentence.form[arc[0]-1], sentence.pos[arc[0]-1], sentence.pos[arc[1]-1])] = 1
                # (p-word, p-pos, c-word)
                if (sentence.form[arc[0]-1], sentence.pos[arc[0]-1], sentence.form[arc[1]-1]) not in self.feature_dict:
                    self.feature_dict[(
                        sentence.form[arc[0]-1], sentence.pos[arc[0]-1], sentence.form[arc[1]-1])] = 1
                # (p-word, c-word)
                if (sentence.form[arc[0]-1], sentence.form[arc[1]-1]) not in self.feature_dict:
                    self.feature_dict[(sentence.form[arc[0]-1],
                                       sentence.form[arc[1]-1])] = 1
                # (p-pos, c-pos)
                if (sentence.pos[arc[0]-1], sentence.pos[arc[1]-1]) not in self.feature_dict:
                    self.feature_dict[(sentence.pos[arc[0]-1],
                                       sentence.pos[arc[1]-1])] = 1

                '''
                In between POS features
                get all the POS tag between the head and child
                '''
                # (p-pod, b-pos, c-pos)
                # check if  the parent and child are immediate neighbors
                if abs(arc[1]-arc[0]) != 1:
                    # initialize a list that has the p-pos as first entry
                    pos_in_between = [sentence.pos[arc[0]-1]]
                    # if child is at the right of parent
                    if arc[1] > arc[0]:
                        for i in range(arc[0], arc[1]-1):
                            pos_in_between.append(sentence.pos[i])
                    # if child is at the left (bigger index than parent)
                    else:
                        for i in range(arc[1], arc[0]-1):
                            pos_in_between.append(sentence.pos[i])
                    # append c-pos
                    pos_in_between.append(sentence.pos[arc[1]-1])
                    # get a tuple of the list
                    pos_in_between_tuple = tuple(pos_in_between)
                    if pos_in_between_tuple not in self.feature_dict:
                        self.feature_dict[pos_in_between_tuple] = 1

                    '''
                    surrounding word POS features
                    '''
                    # (p-pos, p-pos+1, c-pos-1, c-pos)
                    if (sentence.pos[arc[0]-1], sentence.pos[arc[0]], sentence.pos[arc[1]-2], sentence.pos[arc[1]-1]) not in self.feature_dict:
                        self.feature_dict[(sentence.pos[arc[0]-1], sentence.pos[arc[0]],
                                           sentence.pos[arc[1]-2], sentence.pos[arc[1]-1])] = 1
                    # (p-pos, p-pos-1, c-pos-1, c-pos)
                    if (sentence.pos[arc[0]-2], sentence.pos[arc[0]-1], sentence.pos[arc[1]-2], sentence.pos[arc[1]-1]) not in self.feature_dict:
                        self.feature_dict[(sentence.pos[arc[0]-2], sentence.pos[arc[0]-1],
                                           sentence.pos[arc[1]-2], sentence.pos[arc[1]-1])] = 1
                     # (p-pos, p-pos+1, c-pos, c-pos+1)
                    if (sentence.pos[arc[0]-1], sentence.pos[arc[0]], sentence.pos[arc[1]-1], sentence.pos[arc[1]]) not in self.feature_dict:
                        self.feature_dict[(sentence.pos[arc[0]-1], sentence.pos[arc[0]],
                                           sentence.pos[arc[1]-1], sentence.pos[arc[1]])] = 1
                     # (p-pos-1, p-pos, c-pos, c-pos+1)
                    if (sentence.pos[arc[0]-2], sentence.pos[arc[0]-1], sentence.pos[arc[1]-1], sentence.pos[arc[1]]) not in self.feature_dict:
                        self.feature_dict[(sentence.pos[arc[0]-2], sentence.pos[arc[0]-1],
                                           sentence.pos[arc[1]-1], sentence.pos[arc[1]])] = 1
        return self.feature_dict


test = FeatureDict("/Users/lintzuru/Desktop/WS22:23/parsing/test_feature")
print(len(test.get_feature()))
