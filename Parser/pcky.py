#! /usr/bin/env python3

import sys
import nltk
import re
from nltk import Nonterminal, Tree
from unittest import TestCase
from math import log


class PCKY:
    """
    This class parses a given sentence according the the given CNF grammar using a probabilistic CKY algorithm
    """

    def __init__(self, cnf_grammar):
        """
        Initialize the class by loading the grammar
        :param cnf_grammar: the given CNF grammar
        """
        self.grammar = cnf_grammar
        self.matrix = []
        self.i = self.k = self.j = 0

    def setup(self, length):
        """
        Set up the matrix and indices for a new parse
        :param length: the length of the sentence to parse
        :return: void
        """
        self.matrix = [None] * length
        for x in range(0,length):
            self.matrix[x] = [None] * length
        self.i = self.k = self.j = 0

    def tag_word(self, words):
        """
        Add the POS tags for each word at the edge of the matrix
        :param words: the list of words to parse
        :return: void
        """
        self.j += 1
        self.i = self.j - 1
        self.matrix[self.i][self.j] = {}

        possible_tags = self.grammar.productions(rhs=words[self.j - 1])

        if not possible_tags:
            possible_tags = self.grammar.productions(rhs="UNK")

        for rule in sorted(possible_tags, key=lambda x: x.prob()):
            lhs = rule.lhs().symbol()
            self.matrix[self.i][self.j][lhs] = (log(rule.prob()), Tree(lhs, [words[self.j - 1]]))

    def compose_children(self):
        """
        Combine all valid left and right children for the current location in the matrix
        :return:
        """
        for l_symbol, l_info in self.matrix[self.i][self.k].items():
            l_rhs = Nonterminal(l_symbol)
            for r_symbol, r_info in self.matrix[self.k][self.j].items():
                r_rhs = Nonterminal(r_symbol)

                # check the subtrees in [i][k] and [k][j] to see if you can make a valid rhs
                potential_rules = [p for p in self.grammar.productions(rhs=l_rhs) if p.rhs()[1] == r_rhs]
                for potential_rule in sorted(potential_rules, key=lambda x: x.prob()):
                    new_lhs = potential_rule.lhs().symbol()
                    new_tree = Tree(new_lhs, [l_info[1], r_info[1]])
                    new_prob = log(potential_rule.prob()) + l_info[0] + r_info[0]
                    if new_lhs not in self.matrix[self.i][self.j] or new_prob > self.matrix[self.i][self.j][new_lhs][0]:
                            self.matrix[self.i][self.j][new_lhs] = (new_prob, new_tree)

    def parse(self, sentence):
        """
        Parse the given sentence using the CKY algorithm
        :param sentence: the sentencee to parse as a string
        :return: list of valid parse trees
        """
        words = nltk.word_tokenize(sentence)
        self.setup(len(words)+1)

        while self.j < len(words):
            # we start each column at the bottom by tagging the POS of the word
            self.tag_word(words)
            while self.i > 0:
                # move up the column row by row
                self.i -= 1
                self.matrix[self.i][self.j] = {}
                # start k at one more than i
                self.k = self.i+1
                while self.k < self.j:
                    # for each value between i and j, look for potential child trees to connect
                    self.compose_children()
                    self.k += 1

        for root in self.matrix[0][len(words)]:
            if root == self.grammar.start().symbol():
                best_parse = self.matrix[0][len(words)][root][1].pformat(margin=100000000000000)
                return re.sub("\^[^\s]*", "", best_parse)

        return ""


class TestPCKY(TestCase):
    """
    This class contains tests for the PCKY class
    """

    maxDiff = None

    def test_parse(self):
        """
        Test grammar parse example
        :return: void
        """
        grammar = nltk.data.load('./TestFiles/pcfg.pcfg')

        with open('./TestFiles/sentences', "r") as sentences:
            test_sentences = sentences.readlines()

        with open('./TestFiles/trees', "r") as trees:
            expected_trees = trees.readlines()

        parser = PCKY(grammar)

        for sentence, expected in zip(test_sentences, expected_trees):
            output = parser.parse(sentence)
            self.assertEquals(expected.strip("\n"), output)

    def test_unk(self):
        """
        Test unknown words
        :return:
        """
        grammar = nltk.data.load('./TestFiles/unk_pcfg.pcfg')

        with open('./TestFiles/unk_sentences', "r") as sentences:
            test_sentences = sentences.readlines()

        with open('./TestFiles/unk_trees', "r") as trees:
            expected_trees = trees.readlines()

        parser = PCKY(grammar)

        for sentence, expected in zip(test_sentences, expected_trees):
            output = parser.parse(sentence)
            self.assertEquals(expected.strip("\n"), output)


def main():
    """
    Parse the system arguments, call the PCKY class and write results to the output file
    :return:
    """
    grammar_file = sys.argv[1]
    cfg_grammar = nltk.data.load(grammar_file)

    sentence_file = sys.argv[2]
    sentences = open(sentence_file, "r")
    sentences = sentences.readlines()

    output_file = sys.argv[3]
    with open(output_file, "w") as f:

        parser = PCKY(cfg_grammar)

        for sentence in sentences:
            tree = parser.parse(sentence)
            print(tree, file=f)


if __name__ == "__main__":
    main()
