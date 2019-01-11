#! /usr/bin/env python3

import sys
from gensim.models import Word2Vec
from nltk.corpus import brown
from unittest import TestCase
from scipy.stats.stats import spearmanr
from scipy import spatial
from collections import defaultdict
from math import log2
from string import punctuation


class SemanticSimilarity:
    """
    This class loads a Semantic Feature-Based Grammar and uses it to parse sentences
    """

    collocation_matrix = {}
    distributional_model = {}
    vec_model = None
    word2idx = {}

    def __init__(self, window_size, model):
        """
        Initialize the class by setting the window size and building the similarity model
        :param window_size: the given window size
        """
        self.window_size = int(window_size)
        self.words = self.load_corpus()
        self.collocation_matrix = {}
        self.distributional_model = {}
        if model == "FREQ":
            self.build_collocation_matrix()
            self.distributional_model = self.collocation_matrix
        if model == "PMI":
            self.build_collocation_matrix()
            self.build_pmi_model()
        if model == "CBOW":
            self.build_cbow_model()

    def get_word_id(self, word):
        if word not in self.word2idx:
            self.word2idx[word] = len(self.word2idx)
            self.word2idx[self.word2idx[word]] = word
            self.collocation_matrix[self.word2idx[word]] = defaultdict(int)
            self.distributional_model[self.word2idx[word]] = defaultdict(int)
        return self.word2idx[word]

    @staticmethod
    def load_corpus():
        brown_words = list(brown.words())
        return [w.lower() for w in brown_words if w not in punctuation]

    def build_collocation_matrix(self):
        for word_index, word in enumerate(self.words):
            word_id = self.get_word_id(word)
            for window_index in range(1, self.window_size + 1):
                before = self.words[word_index - window_index] if word_index - window_index >= 0 else ""
                after = self.words[word_index + window_index] if word_index + window_index < len(self.words) else ""
                if before:
                    before_id = self.get_word_id(before)
                    self.collocation_matrix[word_id][before_id] += 1
                if after:
                    after_id = self.get_word_id(after)
                    self.collocation_matrix[word_id][after_id] += 1

    def build_pmi_model(self):
        total_sum = sum([sum(x.values()) for x in self.collocation_matrix.values()])
        for word_1_id, row in self.collocation_matrix.items():
            w = sum(row.values())
            for word_2_id, w_f in row.items():
                f = sum(self.collocation_matrix[word_2_id].values())
                ppmi = (w_f / total_sum) / ((w / total_sum) * (f / total_sum))
                self.distributional_model[word_1_id][word_2_id] = max(0.0, log2(ppmi))

    def build_cbow_model(self):
        self.vec_model = Word2Vec([self.words], min_count=1, window=self.window_size, workers=1)
        print(str(len(self.words)))
        print(str(self.vec_model))

    def dist_to_string(self, judgements):
        output_string = []
        human_similarities = []
        cosine_similarities = []
        for judgement in judgements:
            if not judgement.strip():
                continue
            line = judgement.split(",")
            word_1 = line[0]
            word_1_index = self.get_word_id(word_1)
            word_2 = line[1]
            word_2_index = self.get_word_id(word_2)
            human_similarities.append(float(line[2]))

            word_1_context = self.distributional_model[word_1_index]
            word_2_context = self.distributional_model[word_2_index]
            length = 10 if len(word_1_context) > 10 and len(word_2_context) > 10 else min(len(word_1_context),
                                                                                          len(word_2_context))

            word_1_top_10 = sorted(word_1_context.items(), key=lambda kv: (-kv[1], kv[0]))[:length]
            word_2_top_10 = sorted(word_2_context.items(), key=lambda kv: (-kv[1], kv[0]))[:length]
            output_string.append(word_1 + " " + " ".join(['%s: %i' % (self.word2idx[k], v) for k, v in word_1_top_10]))
            output_string.append(word_2 + " " + " ".join(['%s: %i' % (self.word2idx[k], v) for k, v in word_2_top_10]))

            word_1_values = [t[1] for t in word_1_top_10]
            word_2_values = [t[1] for t in word_2_top_10]
            cosine_similarity = 1 - spatial.distance.cosine(word_1_values, word_2_values)
            cosine_similarities.append(cosine_similarity)

            output_string.append(word_1 + "," + word_2 + ":" + str(cosine_similarity))
        output_string.append("correlation:" + str(spearmanr(cosine_similarities, human_similarities)[0]))
        return "\n".join(output_string)

    def cbow_to_string(self, judgements):
        output_string = []
        human_similarities = []
        similarities = []
        for judgement in judgements:
            if not judgement.strip():
                continue
            line = judgement.split(",")
            word_1 = line[0]
            word_2 = line[1]
            human_similarities.append(float(line[2]))

            similarity = 1 - self.vec_model.wv.similarity(word_1, word_2)
            similarities.append(similarity)

            output_string.append(word_1 + "," + word_2 + ":" + str(similarity))
        output_string.append("correlation:" + str(spearmanr(similarities, human_similarities)[0]))
        return "\n".join(output_string)


class TestSemanticSimilarity(TestCase):
    """
    This class contains tests for the SemanticSimilarity class
    """

    maxDiff = None

    with open('./TestFiles/word_pairs', "r") as word_pairs:
        test_word_pairs = word_pairs.readlines()

    with open('./TestFiles/similarities', "r") as similarities:
        expected_similarities = similarities.readlines()

    def test_freq(self):
        """
        Test frequency distribution
        :return: void
        """

        evaluator = SemanticSimilarity(2, "FREQ")

        output = evaluator.dist_to_string(self.test_word_pairs)

        self.assertCountEqual(output.strip().split("\n"), self.expected_similarities)

    def test_pmi(self):
        """
        Test point-wise mutual information distribution
        :return: void
        """

        evaluator = SemanticSimilarity(2, "PMI")

        output = evaluator.dist_to_string(self.test_word_pairs)

        self.assertCountEqual(output.strip().split("\n"), self.expected_similarities)

    def test_cbow(self):
        """
        Test continuous bag of words
        :return: void
        """

        evaluator = SemanticSimilarity(2, "CBOW")

        output = evaluator.cbow_to_string(self.test_word_pairs)

        self.assertCountEqual(output.strip().split("\n"), self.expected_similarities)


def main():
    """
    Parse the system arguments, call the SemanticSimilarity class and write results to the output file
    :return:
    """
    model = sys.argv[1]
    window_size = sys.argv[2]

    judgement_filename = sys.argv[3]
    judgement_file = open(judgement_filename, "r")
    judgements = judgement_file.readlines()

    output_file = sys.argv[4]
    with open(output_file, "w") as f:

        evaluator = SemanticSimilarity(window_size, model)
        output = evaluator.cbow_to_string(judgements) if model == "CBOW" else evaluator.dist_to_string(judgements)
        print(output, file=f)


if __name__ == "__main__":
    main()
