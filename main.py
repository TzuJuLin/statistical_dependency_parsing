import argparse
import _pickle as cPickle
import gzip

from model import Parser
from reader import Corpus
from feature import FeatureMap


def train(args):
    train_corpus = Corpus(args.data)
    train_corpus.add_sentence()
    print("Reading corpus....")
    print("Corpus has {} sentences in total".format(len(train_corpus.sentences)))
    feature_map = FeatureMap(train_corpus)
    feature_map.create_feat()
    print("Extracting features...")
    print("{} features are extracted from the corpus".format(
        len(feature_map.feature_dict)))
    parser = Parser(feature_map)
    print("Training...")
    if args.epochs:
        parser.train_parser(train_corpus, epoch=args.epochs)
    else:
        parser.train_parser(train_corpus)
    save_feat = input("Do you want to save the model? (y/n)")
    if save_feat.lower() in ["y", "yes"]:
        model_file = input("Save the model as: ")
        print("saving the feature as {}".format(model_file))
        stream = gzip.open(model_file, 'wb')
        cPickle.dump(parser, stream, -1)
        stream.close()


def predict(args):
    test_corpus = Corpus(args.data)
    test_corpus.add_sentence()
    stream = gzip.open(args.model, 'rb')
    parser = cPickle.load(stream)
    stream.close()
    parser.predict(test_corpus)
    write_name = input("Please provide a file name for the predicted results:")
    test_corpus.write_file(write_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'mode', choices=['train', 'predict'], help='train or predict')
    parser.add_argument(
        '--langauge', choices=['eng', 'de'], help='choose between "eng" and "de"')
    parser.add_argument('--model', type=str, help='path to model')
    parser.add_argument('--data', type=str, help='data directory')
    parser.add_argument('--epochs', type=int,
                        help='epochs to train')

    args = parser.parse_args()

    if args.mode == 'train':
        train(args)

    if args.mode == 'predict':
        predict(args)
