#! /usr/bin/env python3

import sys
from nltk import Tree, Nonterminal
from unittest import TestCase


class PCFG:
    """
    This class induces a probabilistic context free grammar from a treebank
    """

    grammar_counts = {}
    start = ''

    def count_rules(self, tree, parent):
        """
        For each level in the given tree, increment the corresponding count in the dictionary
        :param tree: the given tree
        :param parent: the parent label
        :return: void
        """
        lhs = tree.label()

        if self.start is '':
            self.start = lhs

        # if this tree's children are subtrees, count the rules in each of those too
        if len(tree) > 1:
            rhs = Nonterminal(tree[0].label() + "^" + lhs + " " + tree[1].label() + "^" + lhs)
            self.count_rules(tree[0], lhs)
            self.count_rules(tree[1], lhs)
        # if this tree has one child, and it's a subtree, count the rules in there too
        elif isinstance(tree[0], Tree):
            rhs = Nonterminal(tree[0].label() + "^" + lhs)
            self.count_rules(tree[0], lhs)
        # if this tree's child is a leaf, no recursion is necessary
        else:
            rhs = tree[0]

        if lhs != self.start:
            lhs = lhs + "^" + parent
        self.grammar_counts.setdefault(lhs, {}).setdefault(rhs, 1)

        if "UNK" not in self.grammar_counts[lhs]:
            self.grammar_counts[lhs]["UNK"] = 1

        self.grammar_counts[lhs][rhs] += 1

    def induce_cfg(self, trees):
        """
        Induce a probabilistic CFG from the given set of trees
        :param trees:
        :return: void
        """
        for tree in trees:
            if tree.strip() is '':
                continue
            self.count_rules(Tree.fromstring(tree.strip()), '')

    def print_pcfg(self):
        """
        Print out the rules in the dictionary with their corresponding probabilities
        :return: the string of rules for the PCFG
        """
        output = ""

        for rhs in self.grammar_counts[self.start]:
            total_lhs = sum(self.grammar_counts[self.start].values())
            prob = self.grammar_counts[self.start][rhs] / total_lhs
            output += self.start + " -> " + (str(rhs) if isinstance(rhs, Nonterminal) else "\"" + rhs + "\"") + " [" + str(prob) + "]\n"

        for lhs in self.grammar_counts.keys():
            if lhs is self.start:
                continue
            total_lhs = sum(self.grammar_counts[lhs].values())
            for rhs in self.grammar_counts[lhs]:
                prob = self.grammar_counts[lhs][rhs]/total_lhs
                output += lhs + " -> " + (str(rhs) if isinstance(rhs, Nonterminal) else "\"" + rhs + "\"") + " [" + str(prob) + "]\n"

        return output.strip()


class TestPCFG(TestCase):
    """
    This class contains tests for the PCFG class
    """

    def test_induction(self):
        """
        Tests for the grammar induction
        :return: void
        """
        with open('./TestFiles/trees', "r") as trees:
            test_trees = trees.readlines()

        inducer = PCFG()
        inducer.induce_cfg(test_trees)

        with open('./TestFiles/annotated_grammar', "r") as grammar:
            expected_grammar = grammar.readlines()

        induced_list = inducer.print_pcfg().split("\n")

        self.assertCountEqual([x.strip("\n") for x in expected_grammar], induced_list)


def main():
    """
    Parse the system arguments, call the PCFG class and write results to the output file
    :return:
    """
    treebank_file = sys.argv[1]
    treebank = open(treebank_file, "r")
    trees = treebank.readlines()

    output_file = sys.argv[2]
    with open(output_file, "w") as f:

        inducer = PCFG()
        inducer.induce_cfg(trees)
        print(inducer.print_pcfg(), file=f)


if __name__ == "__main__":
    main()
