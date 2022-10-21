from reader import Corupus, Sentence


def UAS(gold, pred):
    gold_corpus = Corupus(gold)
    gold_corpus.add_sentence()
    pred_corpus = Corupus(pred)
    pred_corpus.add_sentence()
    token = 0
    correct_head = 0
    for i in range(len(gold_corpus.sentences)):
        token += len(gold_corpus.sentences[i].id)
        for j in range(len(gold_corpus.sentences[i].head)):
            if gold_corpus.sentences[i].head[j] == pred_corpus.sentences[i].head[j]:
                correct_head += 1

    uas = correct_head/token
    return uas


def LAS(gold, pred):
    gold_corpus = Corupus(gold)
    gold_corpus.add_sentence()
    pred_corpus = Corupus(pred)
    pred_corpus.add_sentence()
    token = 0
    correct = 0
    for i in range(len(gold_corpus.sentences)):
        token += len(gold_corpus.sentences[i].id)
        for j in range(len(gold_corpus.sentences[i].head)):
            if gold_corpus.sentences[i].head[j] == pred_corpus.sentences[i].head[j]:
                if gold_corpus.sentences[i].rel[j] == pred_corpus.sentences[i].rel[j]:
                    correct += 1

    las = correct/token
    return las
