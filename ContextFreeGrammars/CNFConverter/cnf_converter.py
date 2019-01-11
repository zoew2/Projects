#! /usr/bin/env python3

import sys
import nltk
from unittest import TestCase


class CNFConverter:
    """
    This class converts a given Context Free Grammar into Chomsky Normal Form
    """

    def __init__(self):

        # a count of how many dummy non-terminals have been created to ensure they're unique
        self.dummy_count = 0

        # a dictionary containing the new productions in the CNF format
        self.cnf_grammar = {}

    @staticmethod
    def is_hybrid(rhs):
        """
        Is the given right-hand side a hybrid production? (i.e. contains both terminals and non-terminals)
        :param rhs: the right-hand side
        :return: bool
        """
        return any(nltk.grammar.is_terminal(x) for x in rhs) and any(nltk.grammar.is_nonterminal(x) for x in rhs)

    @staticmethod
    def is_unit(rhs):
        """
        Is the given right-hand side a unit production? (i.e. contains a single non-terminal)
        :param rhs: the right-hand side
        :return: bool
        """
        return len(rhs) is 1 and nltk.grammar.is_nonterminal(rhs[0])

    @staticmethod
    def is_long(rhs):
        """
        Is the given right-hand side a long production? (i.e. contains more than 2 non-terminals)
        :param rhs: the right-hand side
        :return: bool
        """
        return len(rhs) > 2 and all(nltk.grammar.is_nonterminal(x) for x in rhs)

    @staticmethod
    def is_cnf(rhs):
        """
        Is the given right-hand side in valid Chomsky Normal Form? (i.e. exactly 2 non-terminals or a single terminal)
        :param rhs: the right-hand side
        :return: bool
        """
        return (len(rhs) is 2 and all(nltk.grammar.is_nonterminal(x) for x in rhs)) or (len(rhs) is 1 and nltk.grammar.is_terminal(rhs[0]))

    @staticmethod
    def production_string(rhs):
        """
        Returns the given right-hand side as a string, enclosing any terminals in quotes
        :param rhs: the right-hand side
        :return: str
        """
        return " ".join([x.symbol() if nltk.grammar.is_nonterminal(x) else '"{0}"'.format(x) for x in rhs])

    def add_production(self, lhs, rhs):
        """
        Add the given production into the dictionary of CNF rules
        :param lhs: the left-hand side of the new production
        :param rhs: the right-hand side of the new production
        :return: void
        """
        self.cnf_grammar.setdefault(lhs, []).append(rhs)

    def convert_hybrid_productions(self, production):
        """
        Convert a hybrid production into valid CNF by creating new non-terminals for any terminals in the production
        :param production: a hybrid production
        :return:
        """
        terminal_list = []
        new_rhs = []

        for node in production.rhs():
            if nltk.grammar.is_nonterminal(node):
                new_rhs.append(node)
            else:
                terminal_list.append(node)
                # replace each terminal with a new non-terminal
                new_rhs.append(nltk.Nonterminal(node.upper()))

        if self.is_long(new_rhs):
            self.convert_long_productions(production.lhs().symbol(), new_rhs)
        else:
            self.add_production(production.lhs().symbol(), self.production_string(new_rhs))

        # add new productions for each new non-terminal created
        for string in terminal_list:
            self.add_production(string.upper(), self.production_string([string]))

    def convert_unit_productions(self, grammar, lhs, rhs):
        """
        Convert a unit production into valid CNF by re-writing the right-hand side with the right-hand side of all derivable, non-unit productions
        :param grammar: the CFG grammar
        :param lhs: the left-hand side
        :param rhs: the right-hand side
        :return: void
        """
        next_rules = grammar.productions(lhs=rhs)
        for next_rule in next_rules:
            if self.is_unit(next_rule.rhs()):
                self.convert_unit_productions(grammar, lhs, next_rule.rhs()[0])
            elif self.is_long(next_rule.rhs()):
                self.convert_long_productions(lhs, list(next_rule.rhs()))
            else:
                self.add_production(lhs, self.production_string(next_rule.rhs()))

    def convert_long_productions(self, lhs, rhs):
        """
        Convert a long production into valid CNF by introducing unique non-terminals and spreading them over productions
        :param lhs: the left-hand side
        :param rhs: the right-hand side
        :return: void
        """
        if len(rhs) is 2:
            self.add_production(lhs, self.production_string(rhs))
            return
        else:
            self.dummy_count += 1
            dummy_nonterminal = "X" + str(self.dummy_count)

            self.add_production(lhs, dummy_nonterminal + " " + rhs[len(rhs) - 1].symbol())
            rhs.pop(len(rhs) - 1)
            self.convert_long_productions(dummy_nonterminal, rhs)

    def convert_grammar(self, cfg_grammar):
        """
        Convert every production in a CFG grammar into valid CNF
        :param cfg_grammar: the CFG grammar
        :return: void
        """
        for rule in cfg_grammar.productions():
            if self.is_cnf(rule.rhs()):
                self.add_production(rule.lhs().symbol(), self.production_string(rule.rhs()))
            if self.is_hybrid(rule.rhs()):
                self.convert_hybrid_productions(rule)
            if self.is_unit(rule.rhs()):
                self.convert_unit_productions(cfg_grammar, rule.lhs().symbol(), rule.rhs()[0])
            if self.is_long(rule.rhs()):
                self.convert_long_productions(rule.lhs().symbol(), list(rule.rhs()))


class TestCNFConverter(TestCase):
    """
    This class contains tests for the CNFConverter class
    """

    def test_hybrid_production(self):
        """
        Test hybrid productions
        :return: void
        """
        grammar = nltk.CFG.fromstring('NP -> "the" Nom')

        converter = CNFConverter()
        converter.cnf_grammar = {}
        converter.convert_grammar(grammar)

        expected_grammar = {
            "NP": ["THE Nom"],
            "THE": ['"the"']
        }

        self.assertDictEqual(converter.cnf_grammar, expected_grammar)

    def test_unit_production(self):
        """
        Test unit productions
        :return: void
        """
        grammar = nltk.CFG.fromstring('QP -> VP\n VP -> V\n V -> "word" | "word2"')

        converter = CNFConverter()
        converter.cnf_grammar = {}
        converter.convert_grammar(grammar)

        expected_grammar = {
            "QP": ['"word"', '"word2"'],
            "VP": ['"word"', '"word2"'],
            "V": ['"word"', '"word2"']
        }

        self.assertDictEqual(converter.cnf_grammar, expected_grammar)

    def test_long_production(self):
        """
        Test long productions
        :return: void
        """
        grammar = nltk.CFG.fromstring("NP -> Det Adj N")

        converter = CNFConverter()
        converter.cnf_grammar = {}
        converter.convert_grammar(grammar)

        expected_grammar = {
            "NP": ["X1 N"],
            "X1": ["Det Adj"]
        }

        self.assertDictEqual(converter.cnf_grammar, expected_grammar)

    def test_long_unit(self):
        """
        Test long and unit productions
        :return: void
        """
        grammar = nltk.CFG.fromstring("SIGMA -> NREL_VBZ \nSIGMA -> DECL_DOZ \nNREL_VBZ -> NP_WPS VERB_VBS INFCL_VB \nDECL_DOZ -> NP_DT VERB_DOZ NP_NN pt_char_per")

        converter = CNFConverter()
        converter.cnf_grammar = {}
        converter.convert_grammar(grammar)

        expected_grammar = {
            "SIGMA": ["X1 INFCL_VB", "X2 pt_char_per"],
            "X1": ["NP_WPS VERB_VBS"],
            "X2": ["X3 NP_NN"],
            "X3": ["NP_DT VERB_DOZ"],
            "NREL_VBZ": ["X4 INFCL_VB"],
            "DECL_DOZ": ["X5 pt_char_per"],
            "X4": ["NP_WPS VERB_VBS"],
            "X5": ["X6 NP_NN"],
            "X6": ["NP_DT VERB_DOZ"]
        }

        self.assertDictEqual(converter.cnf_grammar, expected_grammar)

    def test_hybrid_long(self):
        """
        Test hybrid and long productions
        :return: void
        """
        grammar = nltk.CFG.fromstring('NP -> "the" Nom "to" Nom')

        converter = CNFConverter()
        converter.cnf_grammar = {}
        converter.convert_grammar(grammar)

        expected_grammar = {
            "NP": ["X1 Nom"],
            "THE": ['"the"'],
            "TO": ['"to"'],
            "X1": ["X2 TO"],
            "X2": ["THE Nom"]
        }

        self.assertDictEqual(converter.cnf_grammar, expected_grammar)
        

def main():
    """
    Parse the system arguments, call the CNFConverter class and write results to the output file
    :return:
    """
    grammar_file = sys.argv[1]
    cfg_grammar = nltk.data.load(grammar_file)

    output_file = sys.argv[2]
    output = open(output_file, "w")

    output.write("%start " + cfg_grammar.start().symbol() + "\n")

    converter = CNFConverter()
    converter.convert_grammar(cfg_grammar)

    for key, value in converter.cnf_grammar.items():
        output.write(key + " -> " + " | ".join(value) + "\n")

    output.close()


if __name__ == "__main__":
    main()
