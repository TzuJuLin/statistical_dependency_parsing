from feature import FeatureMap
from reader import Corpus
import numpy as np
from eisner import Decoder
import time
import random


class Parser:

    def __init__(self, feature_map) -> None:
        self.feature_map = feature_map
        # weight vector has the length of the number of features
        self.weight = np.zeros(
            [len(self.feature_map.feature_dict)], dtype=float)

    def score_for_decoder(self, sentence):

        # get all the possible arcs
        tree = sentence.get_full_tree()
        # initialize a score matrix that can be passed in the decoder
        score_matrix = np.zeros(
            [len(sentence.tokens), len(sentence.tokens)], dtype=float)
        # loop through the arcs and assigne a score to it
        for arc in tree:
            score = 0.0
            # get the features of the arc
            features = self.feature_map.feature_mapping(arc, sentence)
            # if feature already in feature dict, add up the corresponding weight
            for feature in features:
                # add up the scores of the arc
                score += self.weight[feature]
            # assign the score in to the scoring matrix
            score_matrix[arc[0], arc[1]] = score

        # return a score matrix that can be passed into the decoder
        return score_matrix

    # train the parser, pass in the corpus and epoch
    # can be used for train and dev set

    def train_parser(self, corpus, epoch=4):

        decoder = Decoder()

        # iterate through epoch
        for iter in range(epoch):
            # shuffle the sentence
            random.shuffle(corpus.sentences)
            start = time.time()

            # one sentence at a time
            for i, sent in enumerate(corpus.sentences):
                if i % 500 == 0:
                    print("sentence: " + str(i), "time: ",
                          str(time.time()-start))

                # get the score matrix that can be decoded by the decoder
                score_matrix = self.score_for_decoder(sent)

                # get the predicted tree predicted by the decoder
                pred_tree = decoder.parse(score_matrix)

                # check the edges predicted by the decoder
                for edge in pred_tree:

                    sent.tokens[edge[1]].pred_head = edge[0]

                # check one token at a time
                for i, token in enumerate(sent.tokens):
                    if i != 0:  # skip Root
                        # if predicted head != gold head, update the weight
                        if token.head != token.pred_head:
                            gold_feature = self.feature_map.feature_mapping(
                                arc=(token.head, token.id), sent=sent)
                            pred_feature = self.feature_map.feature_mapping(
                                arc=(token.pred_head, token.id), sent=sent)
                            self.weight[gold_feature] += 1
                            self.weight[pred_feature] -= 1
            end = time.time()
            print("執行時間:%f 秒" % (end - start))

            # check point after every epoch
            print('epoch {}'.format(iter), corpus.uas())
        return corpus.uas()

    # pruning function if want to make the feature dictionary smaller
    # set up a threshhold (smallest weight allowed)
    def prune(self, th=1):
        remove_id = []
        for i, w in enumerate(self.weight):
            if w < th:
                remove_id.append(i)
        self.feature_map.feature_dict = {
            key: val for key, val in self.feature_map.feature_dict.items() if val in remove_id}

    # predict the arcs for a given corpus

    def predict(self, corpus):

        decoder = Decoder()
        for sent in corpus.sentences:
            score_matrix = self.score_for_decoder(sent)
            pred_tree = decoder.parse(score_matrix)
            # add the edges into the corpus
            for edge in pred_tree:
                sent.tokens[edge[1]].head = edge[0]


def main(corpus_path):
    train_corpus = Corpus(corpus_path)
    train_corpus.add_sentence()
    feature_map = FeatureMap(train_corpus)

    feature_map.create_feat()
    parser = Parser(feature_map)
    uas = parser.train_parser(train_corpus)

    print('uas: ', uas)

# main("test_feature")

# main("wsj_train.only-projective.first-5k.conll06")
