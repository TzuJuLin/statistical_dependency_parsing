from feature import FeatureMap
from reader import Corpus, Sentence, Token
import numpy as np
# hyperparameters
epoch = 30


def score_arc(weight, feature):

    return np.dot(weight, feature)


'''
一次處理一個句子
sentence是包含所有句子資訊的
'''


def score_matrx(weight, sentence, Feature_map):
    N = len(sentence)
    tree = sentence.get_full_tree()
    score_matrix = np.zeros([N, N], dtype=int)

    for arc in tree:
        # features of 1 arc, represented as feature_ids
        features = Feature_map.extract(arc, sentence)
        # initialize a feature vector of the current arc
        feature_vector = np.zeros([len(Feature_map.feature_dict), 1])
        # add 1 to the index of the feature vector according to the extracted feature
        for feature in features:
            feature_vector[feature, 0] += 1
        # add the computed score into the score matrix
        score = score_arc(weight, feature_vector)

        score_matrix[arc[0], arc[1]] = score

    return score_matrix


def train_parser(corpus, feature, gold_arc, Feature_map):

    weight = np.zeros(len(feature))
    for i in range(epoch):

        #
        for sent in corpus.sentences:
            score_matrix = score_matrx(weight, sent, Feature_map)

            # get the feature vector of such sentence

            # get the scaler product of the feature vector(of the sentence) and the w

            #

            pass
