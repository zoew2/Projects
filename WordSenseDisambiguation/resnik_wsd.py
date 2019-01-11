#! /usr/bin/env python3

import sys
from unittest import TestCase
from nltk.corpus import *
from collections import defaultdict
from nltk.corpus.reader.wordnet import information_content
from scipy.stats.stats import spearmanr


class ResnikWordSenseDisambiguation:
    """
    This class uses Resnik Similarity to disambiguate word senses
    """

    human_similarities = []
    resnik_similarities = []

    def __init__(self):
        """
        Initialize this class by loading the information content
        """
        self.brown_ic = wordnet_ic.ic('ic-brown-resnik-add1.dat')

    def get_sense(self, target, probes):
        """
        Get the most likely sense for the target word based on its similarity to the probes
        :param target: the target word
        :param probes: the probe words
        :return: the similarities calculated and the chosen sense
        """
        probe_words = probes.split(",")
        support = defaultdict(int)
        sim_scores = []
        for probe in probe_words:
            lcs = self.get_resnik_similarity(target, probe)
            support[lcs[0]] += lcs[1]
            sim_scores.append("(" + target + ", " + probe + ", " + '%.10f' % lcs[1] + ")")

        max_sim = max(score for score in support.values())
        max_sense = [sense for sense, score in support.items() if score == max_sim][0]

        return " ".join(sim_scores) + "\n" + max_sense

    def get_resnik_similarity(self, target, probe):
        """
        calculate the resnik similarity for the given two words
        :param target: the target word
        :param probe: the probe word
        :return:
        """
        sense = ""
        sim = 0
        for target_sense in wordnet.synsets(target, pos=wordnet.NOUN):
            for probe_sense in wordnet.synsets(probe, pos=wordnet.NOUN):
                hypernyms = target_sense.common_hypernyms(probe_sense)
                ic = max(information_content(hp, self.brown_ic) for hp in hypernyms)
                if ic > sim:
                    sense = target_sense.name()
                    sim = ic

        return sense, sim

    def get_similarities(self, judgement):
        """
        Get and compare resnik similarities to the human judgement passed in
        :param judgement: the human judgement
        :return: the similarity calculated
        """
        line = judgement.split(",")
        word_1 = line[0]
        word_2 = line[1]
        self.human_similarities.append(float(line[2]))

        resnik_similarity = self.get_resnik_similarity(word_1, word_2)[1]
        self.resnik_similarities.append(resnik_similarity)

        return word_1 + "," + word_2 + ":" + '%.10f' % resnik_similarity

    def get_correlation(self):
        """
        Get the correlation between the human and resnik similarities
        :return: the correlation calculated
        """
        return "Correlation:" + '%.10f' % (spearmanr(self.resnik_similarities, self.human_similarities)[0])


class TestResnikWordSenseDisambiguation(TestCase):
    """
    This class contains tests for the ResnikWordSenseDisambiguation class
    """

    maxDiff = None

    contexts = [
        "tie    jacket,suit",
        "suit   jacket,tie"
    ]

    expected_senses = [
        "(tie, jacket, 6.7417934959) (tie, suit, 6.7417934959)",
        "necktie.n.01",
        "(suit, jacket, 6.7417934959) (suit, tie, 6.7417934959)",
        "suit.n.01"
    ]

    judgements = [
        "car,automobile,3.92",
        "journey,voyage,3.84",
        "magician,wizard,3.76"
    ]

    expected_similarities = [
        "car,automobile:7.2797467672",
        "journey,voyage:7.4165398078",
        "magician,wizard:10.6065797336"
    ]

    correlation = "Correlation:-1.0000000000"

    def test_get_senses(self):
        """
        Test get_sense function
        :return: void
        """

        disambiguator = ResnikWordSenseDisambiguation()

        output = []
        for line in self.contexts:
            similarity = disambiguator.get_sense(line.split()[0], line.split()[1])
            output.extend(similarity.split("\n"))

        self.assertCountEqual(output, self.expected_senses)

    def test_get_similarities(self):
        """
        Test get_similarities function
        :return: void
        """

        disambiguator = ResnikWordSenseDisambiguation()

        output = []
        for line in self.judgements:
            similarity = disambiguator.get_similarities(line)
            output.extend(similarity.split("\n"))

        self.assertCountEqual(output, self.expected_similarities)
        self.assertEquals(disambiguator.get_correlation(), self.correlation)


def main():
    """
    Parse the system arguments, call the ResnikWordSenseDisambiguation class and write results to the output file
    :return:
    """
    context_filename = sys.argv[1]
    context_file = open(context_filename, "r")
    contexts = context_file.readlines()

    judgement_filename = sys.argv[2]
    judgement_file = open(judgement_filename, "r")
    judgements = judgement_file.readlines()

    output_file = sys.argv[3]
    with open(output_file, "w") as f:

        disambiguator = ResnikWordSenseDisambiguation()

        for context in contexts:
            context_words = context.split()
            print(disambiguator.get_sense(context_words[0], context_words[1]), file=f)

        for judgement in judgements:
            print(disambiguator.get_similarities(judgement), file=f)

        print(disambiguator.get_correlation(), file=f)


if __name__ == "__main__":
    main()
