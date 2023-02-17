from feature import FeatureMap
from reader import Corpus, Sentence, Token
import numpy as np
from eisner import Decoder
# hyperparameters
epoch = 30


def score_arc(weight, feature):

    return np.dot(weight, feature)


def get_feature_vector(feature_ids, Feature_map):
    feature_vector = np.zeros([len(Feature_map.feature_dict)])
    for feature in feature_ids:
        feature_vector[feature] += 1
    return feature_vector


def score_for_decoder(weight, sentence, Feature_map):
    N = len(sentence.tokens)
    tree = sentence.get_full_tree()
    score_matrix = np.zeros([N, N], dtype=int)

    for arc in tree:
        # features of 1 arc, represented as feature_ids
        features = Feature_map.extract(arc, sentence)

        # initialize a feature vector of the current arc
        feature_vector = get_feature_vector(features, Feature_map)

        # add the computed score into the score matrix
        score = score_arc(weight, feature_vector)
        score_matrix[arc[0], arc[1]] = score
    return score_matrix


def train_parser(corpus, Feature_map, epoch=10):
    decoder = Decoder()
    weight = np.zeros([len(Feature_map.feature_dict)])
    for i in range(epoch):

        for sent in corpus.sentences:
            score_matrix = score_for_decoder(weight, sent, Feature_map)
            pred_tree = decoder.get_best_tree(score_matrix)

            for i in range(1, len(pred_tree)):
                child = sent.tokens[i]
                child.pred_head = pred_tree[i]

            for i, token in enumerate(sent.tokens):
                if i != 0:  # skip Root
                    if token.head != token.pred_head:
                        gold_feature = Feature_map.extract(
                            arc=(token.head, token.id), sent=sent)
                        gold_feature_vector = get_feature_vector(
                            gold_feature, Feature_map)
                        pred_feature = Feature_map.extract(
                            arc=(token.pred_head, token.id), sent=sent)
                        pred_feature_vector = get_feature_vector(
                            pred_feature, Feature_map)
                        weight = weight + gold_feature_vector
                        weight = weight + pred_feature_vector
    print(weight)
    return corpus.uas()


def main(corpus_path):
    train_corpus = Corpus(corpus_path)
    train_corpus.add_sentence()
    feature_map = FeatureMap(train_corpus)
    feature_map.get_all_features()
    uas = train_parser(train_corpus, feature_map)
    print('uas: ', uas)


main("/Users/lintzuru/Desktop/WS22:23/parsing/test_feature")
# main("/Users/lintzuru/Desktop/WS22:23/parsing/wsj_train.first-1k.conll06")
