def read(file):
    f = open(file, 'r')
    i = 0
    for line in f:
        print(line)


class Sentence:
    def __init__(self):
        self.id = []
        self.form = []
        self.lemma = []
        self.pos = []
        self.xpos = []
        self.morph = []
        self.head = []
        self.rel = []


class Corpus:

    def __init__(self, path):
        self.path = path
        self.sentences = []

    def add_sentence(self):
        f = open(self.path, 'r')
        sent = Sentence()
        for line in f:
            if line != "\n":
                current_line = line.split("\t")
                # if current_line[0] == "1":
                #     sent.id.append(0)
                #     sent.form.append('ROOT')
                #     sent.lemma.append('ROOT')
                sent.id.append(current_line[0])
                sent.form.append(current_line[1])
                sent.lemma.append(current_line[2])
                sent.pos.append(current_line[3])
                sent.xpos.append(current_line[4])
                sent.morph.append(current_line[5])
                sent.head.append(current_line[6])
                sent.rel.append(current_line[7])
            else:
                self.sentences.append(sent)
                sent = Sentence()

    def write_file(self):
        new_f = open("new.pred", "w")
        for sent in self.sentences:
            for i in range(len(sent.id)):
                new_line = ""
                new_line += sent.id[i]
                new_line += "\t"
                new_line += sent.form[i]
                new_line += "\t"
                new_line += sent.lemma[i]
                new_line += "\t"
                new_line += sent.pos[i]
                new_line += "\t"
                new_line += sent.xpos[i]
                new_line += "\t"
                new_line += sent.morph[i]
                new_line += "\t"
                new_line += sent.head[i]
                new_line += "\t"
                new_line += sent.rel[i]
                new_line += "\t"
                new_line += "_"
                new_line += "\t"
                new_line += "_"
                new_line += "\n"
                new_f.write(new_line)
            new_f.write("\n")


# c = Corpus("/Users/lintzuru/Desktop/WS22:23/parsing/test_feature")
# c.add_sentence()
# print(type(c.sentences))
