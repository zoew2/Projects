import sys
from unittest import TestCase
import numpy as np


class WordAnalogy:
    """
    This class finds analogies using word vectors
    """
    vectors = {}
    accurate = 0

    word2idx = {}
    idx2word = {}

    def __init__(self, vectors, should_normalize):
        """
        Initialize this class with the word vectors and normalize if necessary
        :param vectors: threshold value for rare words
        :param should_normalize: whether to normalize the vector
        """
        first_line = vectors[0].split()
        self.default_word = first_line[0]
        self.vectors = np.empty(shape=(len(vectors), len(first_line)-1))

        # convert the input vectors into a multidimensional numpy array
        for vector in vectors:
            values = vector.split()
            word_id = self.get_word_id(values[0])
            self.vectors[word_id] = np.array([float(x) for x in values[1:]])

        # normalize if flag1 is true
        if should_normalize:
            np.divide(self.vectors, np.linalg.norm(self.vectors))

    def get_word_id(self, word):
        """
        Get the ID for the given word
        :param word: the given word
        :return:
        """
        if word not in self.word2idx:
            self.word2idx[word] = len(self.word2idx)
            self.idx2word[self.word2idx[word]] = word

        return self.word2idx[word]

    def get_vector(self, word):
        """
        Get the vector corresponding to the given word
        :param word: the given word
        :return:
        """
        word_id = self.get_word_id(word)
        if word_id >= len(self.vectors):
            return np.array([])

        return self.vectors[word_id]

    def get_analogy(self, words, use_euclid):
        """
        Get the analogy for the given words
        :param words: the given list of words
        :param use_euclid: Should we use euclid distance
        :return:
        """
        word_list = words.split()
        A = self.get_vector(word_list[0])
        B = self.get_vector(word_list[1])
        C = self.get_vector(word_list[2])

        # if any of the first three words are not in the vocabulary, output the default word
        if any([A.size == 0, B.size == 0, C.size == 0]):
            self.accurate += 1 if self.default_word == word_list[3] else 0
            return " ".join([word_list[0], word_list[1], word_list[2], self.default_word])

        target_value = (B - A) + C

        if use_euclid:
            answer = np.argmin(self.get_euclidean_distance(self.vectors, target_value))
        else:
            answer = np.argmax(self.get_cosine_similarity(self.vectors, target_value))

        self.accurate += 1 if self.idx2word[answer] == word_list[3] else 0
        return " ".join([word_list[0], word_list[1], word_list[2], self.idx2word[answer]])

    @staticmethod
    def get_euclidean_distance(vector_matrix, vector):
        """
        Get the euclidean distance between the vectors in the input matrix and the second vector
        :param vector_matrix: the matrix of vectors
        :param vector: the second vector
        :return:
        """
        return np.linalg.norm(vector_matrix - vector, axis=-1)[:, np.newaxis]

    @staticmethod
    def get_cosine_similarity(vector_matrix, vector):
        """
        Get the cosine similarity between the vectors in the input matrix and the second vector
        :param vector_matrix: the matrix of vectors
        :param vector: the second vector
        :return:
        """
        return np.inner(vector_matrix, vector) / (np.linalg.norm(vector_matrix, axis=-1)[:, np.newaxis] * np.linalg.norm(vector)).T


class TestWordAnalogy(TestCase):
    """
    This class contains tests for the WordAnalogy class
    """

    maxDiff = None

    vectors = [
        "boy -0.9 -0.5 0.2 -0.5 0.3",
        "girl -0.6 -0.6 0.1 0.4 0.1",
        "brother -0.1 -0.9 0.3 -0.6 0.8",
        "sister -0.6 -0.9 0.2 0.1 0.3",
        "dad -0.3 0.7 -0.6 -0.6 0.9",
        "mom -0.2 0.6 -0.1 0.8 0.5"
    ]

    input_words = [
        "boy girl brother sister",
        "boy girl dad mom"
    ]

    def test_get_analogy_normalize_euclid(self):
        thesaurus = WordAnalogy(self.vectors, True)
        output = []
        for line in self.input_words:
            output.append(thesaurus.get_analogy(line, True))
        self.assertEquals(output, self.input_words)

    def test_get_analogy_no_normalize_euclid(self):
        thesaurus = WordAnalogy(self.vectors, False)
        output = []
        for line in self.input_words:
            output.append(thesaurus.get_analogy(line, True))
        self.assertEquals(output, self.input_words)

    def test_get_analogy_normalize_cosine(self):
        thesaurus = WordAnalogy(self.vectors, True)
        output = []
        for line in self.input_words:
            output.append(thesaurus.get_analogy(line, False))
        self.assertEquals(output, self.input_words)

    def test_get_analogy_no_normalize_cosine(self):
        thesaurus = WordAnalogy(self.vectors, False)
        output = []
        for line in self.input_words:
            output.append(thesaurus.get_analogy(line, False))
        self.assertEquals(output, self.input_words)


def main():
    """
    Parse the system arguments, call the WordAnalogy class and write results to the output file
    :return:
    """
    vectors_filename = sys.argv[1]
    vectors_file = open(vectors_filename, "r")
    vectors = vectors_file.readlines()

    input_filename = sys.argv[2]
    input_file = open(input_filename, "r")
    inputs = input_file.readlines()

    output_filename = sys.argv[3]

    should_normalize = int(sys.argv[4]) != 0
    use_cosine = int(sys.argv[5]) != 0

    thesaurus = WordAnalogy(vectors, should_normalize)

    with open(output_filename, "a") as out:

        for line in inputs:
            print(thesaurus.get_analogy(line, use_cosine), file=out)

    print(thesaurus.accurate)


if __name__ == "__main__":
    main()
