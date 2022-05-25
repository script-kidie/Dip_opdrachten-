import numpy
import pandas as pd
pd.set_option('display.max_columns', None)
import string


class language_object:
    def __init__(self):
        self.matrix_dutch = pd.DataFrame(data=numpy.zeros((28, 28)), columns=list(string.ascii_lowercase) + [" ", "_"], index=list(string.ascii_lowercase) + [" ", "_"])
        self.matrix_english = pd.DataFrame(data=numpy.zeros((28, 28)), columns=list(string.ascii_lowercase) + [" ", "_"], index=list(string.ascii_lowercase) + [" ", "_"])
        self.matrixes = []

    def train(self, train_string:str, language):
        train_string = train_string.lower()
        self.matrixes = []

        workers = 2
        list_train_strings = []
        incrementation = int(len(train_string)/workers)
        start = 0
        end = incrementation

        for i in range(workers):
            list_train_strings.append(train_string[start:end])
            start += incrementation
            end += incrementation

            self.map_make_matrix(list_train_strings[i])

        if language == "dutch":
            self.matrix_dutch = self.reduce_combine_matrixes()
            dutch_total = self.matrix_dutch.sum().sum()
            self.matrix_dutch = self.matrix_dutch.div(dutch_total)

        else:
            self.matrix_english = self.reduce_combine_matrixes()
            english_total = self.matrix_english.sum().sum()
            self.matrix_english = self.matrix_english.div(english_total)





    def is_special_char(self, x):
        if x in list(string.ascii_lowercase) + [" "]:
            return x
        else:
            return "_"

    def map_make_matrix(self, data_string):
        this_matrix = pd.DataFrame(data=numpy.zeros((28, 28)), columns=list(string.ascii_lowercase) + [" ", "_"],
                                   index=list(string.ascii_lowercase) + [" ", "_"])

        # replace all special characters with underscores
        data_string = list(map(self.is_special_char, data_string))

        # MAP make pairs of letters

        pairs = list(map(lambda x, y: (x, y), data_string, data_string[1:]))

        for pair in pairs:
            this_matrix.loc[pair[0], pair[1]] += 1

        self.matrixes.append(this_matrix)

    def reduce_combine_matrixes(self):
        total_matrix = pd.DataFrame(data=numpy.zeros((28, 28)), columns=list(string.ascii_lowercase) + [" ", "_"], index=list(string.ascii_lowercase) + [" ", "_"])

        for matrix in self.matrixes:
            total_matrix += matrix

        return total_matrix

    def recognise_lang(self, input_str):
        input_str = input_str.lower()
        self.matrixes = []

        workers = 1
        list_train_strings = []
        incrementation = int(len(input_str) / workers)
        start = 0
        end = incrementation


        for i in range(workers):
            list_train_strings.append(input_str[start:end])
            start += incrementation
            end += incrementation

            self.map_make_matrix(list_train_strings[i])

        sentence_matrix = self.reduce_combine_matrixes()


        english_multiplicator = self.matrix_english * sentence_matrix
        dutch_multiplicator = self.matrix_dutch * sentence_matrix

        if english_multiplicator.sum().sum() > dutch_multiplicator.sum().sum():
            return True
        else:
            return False

def main():
    lan_ob = language_object()
    with open("dutch.txt", "r", encoding="utf-8") as d:
        text = str(d.readlines())
        lan_ob.train(text, "dutch")

    with open("english.txt", "r", encoding="utf-8") as e:
        text = str(e.readlines())
        lan_ob.train(text, "english")


    with open("test.txt", "r", encoding="utf-8") as t:
        total_english = 0
        total_dutch = 0
        for line in t.readlines():
            if lan_ob.recognise_lang(line):
                total_english += 1
            else:
                total_dutch += 1

        print("aantal engelse zinnen: ", total_english)
        print("aantal nederlandse zinnen: ", total_dutch)


if __name__ == '__main__':
    main()

