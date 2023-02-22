from itertools import permutations


def read(file):
    f = open(file, 'r')
    for line in f:
        print(line)


class Token:

    def __init__(self):
        self.id = None
        self.form = None
        self.lemma = None
        self.pos = None
        self.xpos = None
        self.morph = None
        self.head = None
        self.rel = None
        self.pred_head = None


class Sentence:
    def __init__(self):
        self.tokens = []

    # get all the possible edges of the given sentences
    def get_full_tree(self):
        a = list(range(1, len(self.tokens)))
        fully_connected_tree = list(permutations(a, 2))
        for i in a:
            fully_connected_tree.append((0, i))
        return fully_connected_tree


class Corpus:

    def __init__(self, path):
        self.path = path
        self.sentences = []

    def add_sentence(self):
        f = open(self.path, 'r')
        sent = Sentence()
        for line in f:
            token = Token()
            if line != "\n":
                current_line = line.split("\t")
                if current_line[0] == "1":
                    token.id = 0
                    token.form = 'ROOT'
                    token.pos = 'ROOT'
                    sent.tokens.append(token)
                    token = Token()
                token.id = int(current_line[0])
                token.form = current_line[1]
                token.lemma = current_line[2]
                token.pos = current_line[3]
                token.xpos = current_line[4]
                token.morph = current_line[5]
                if current_line[6] != "_":
                    token.head = int(current_line[6])
                else:
                    token.head = current_line[6]
                token.rel = current_line[7]
                sent.tokens.append(token)

            else:
                self.sentences.append(sent)
                sent = Sentence()

    def write_file(self, file_name):
        new_f = open(file_name, "w")
        for sent in self.sentences:
            for token in sent.tokens:
                if token.form != 'ROOT':
                    new_line = ""
                    new_line += str(token.id)
                    new_line += "\t"
                    new_line += token.form
                    new_line += "\t"
                    new_line += token.lemma
                    new_line += "\t"
                    new_line += token.pos
                    new_line += "\t"
                    new_line += token.xpos
                    new_line += "\t"
                    new_line += token.morph
                    new_line += "\t"
                    new_line += str(token.head)
                    new_line += "\t"
                    new_line += token.rel
                    new_line += "\t"
                    new_line += "_"
                    new_line += "\t"
                    new_line += "_"
                    new_f.write(new_line)
                new_f.write("\n")
            # new_f.write("\n")
        new_f.close()

    def uas(self):
        token_n = 0
        correct_head = 0
        for sent in self.sentences:
            for token in sent.tokens:
                if token.id != 0:
                    if token.pred_head == token.head:
                        correct_head += 1
                        token_n += 1
                    else:
                        token_n += 1
        print("total tokens: ", token_n, "correct tokens:", correct_head)
        return correct_head/token_n
