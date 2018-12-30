from string import whitespace
import sys
from unittest import TestCase


class FSTAcceptor:
    """
    This class determines if a given string is accepted by a given FST
    """

    output_string = ""
    output_probability = 1

    def __init__(self, fst_rules):
        """
        Initialize the class by loading the FST
        :param fst_rules: a description of an FST
        """
        self.fst = self.load_fst(fst_rules)

    @staticmethod
    def load_fst(fst_rules):
        """
        Load the given FST into a dictionary
        :param fst_rules: a description of an FST
        :return: dictionary representation of the FST
        """
        fst = {'start_state': '', 'final_states': [], 'transitions': {}}

        for line in fst_rules:
            rule = list(filter(None, line.split()))

            if len(rule) < 1 or rule[0] == '':
                continue
            if "(" not in rule[0]:
                # if this is not a transition, it's the final state
                fst['final_states'] = rule
            else:
                # get the values for the transition
                first_state = rule[0].strip(whitespace + '"\'()')
                second_state = rule[1].strip(whitespace + '"\'()')
                input_string = rule[2].strip(whitespace + '"\'()')
                output_string = rule[3].strip(whitespace + '"\'()')
                probability = float(rule[4].strip(whitespace + '"\'()') if len(rule) > 4 else 1)

                if "*e*" in input_string:
                    input_string = ''
                if fst['start_state'] is '':
                    fst['start_state'] = first_state
                if first_state not in fst['transitions'].keys():
                    fst['transitions'][first_state] = {}

                fst['transitions'][first_state].setdefault(input_string, []).append((second_state, output_string, probability))

        return fst

    def can_accept_string(self, string):
        """
        Can this FST accept the given string?
        :param string: the string to check for acceptance
        :return: bool
        """
        characters = [x.strip(whitespace + '"\'()') for x in string.split()]
        self.output_string = ''
        self.output_probability = 1

        accepted = self.input_to_output(characters, 0, self.fst['start_state'])

        if accepted and self.output_string is "":
            self.output_string = "*e*"

        return accepted

    def input_to_output(self, characters, index, current_state):
        """
        Can we reach a final state from the current state?
        :param characters: the string of characters
        :param index: the current index of the string
        :param current_state: the current state
        :return: bool
        """
        accepted = False
        # if we've reached the end of the string and we're in a final state, we can accept the string
        if index == len(characters) and current_state in self.fst['final_states']:
            return True
        # otherwise continue to attempt to transition towards a final state
        elif current_state in self.fst['transitions']:
            if index < len(characters) and characters[index] in self.fst['transitions'][current_state]:
                transitions = sorted(self.fst['transitions'][current_state][characters[index]], key=lambda x: x[2])
                for transition in transitions:
                    accepted = accepted or self.input_to_output(characters, index + 1, transition[0])
                    if accepted:
                        self.output_string = ("\"" + transition[1] + "\" " if transition[1] != '*e*' else '') + self.output_string
                        self.output_probability *= transition[2]
                        break
            if '' in self.fst['transitions'][current_state] and not accepted:
                transitions = sorted(self.fst['transitions'][current_state][''], key=lambda x: x[2])
                for transition in transitions:
                    accepted = accepted or self.input_to_output(characters, index, transition[0])
                    if accepted:
                        self.output_string = ("\"" + transition[1] + "\" " if transition[1] != '*e*' else '') + self.output_string
                        self.output_probability *= transition[2]
                        break

        return accepted


class TestFSTAcceptor(TestCase):
    """
    This class contains tests for the FSTAcceptor class
    """

    test_string1 = '"a" "a" "b"'
    test_string2 = '"a" "a"'
    test_empty_string = ''

    def test_fst1(self):
        """
        Tests for FST1
        :return: void
        """
        fst_filename = './TestFSTs/fst1'

        with open(fst_filename, "r") as fst_file:
            fst_rules = fst_file.readlines()

        expected_output = '"b"'

        acceptor = FSTAcceptor(fst_rules)

        self.assertFalse(acceptor.can_accept_string(self.test_string1))

        self.assertTrue(acceptor.can_accept_string(self.test_string2))
        self.assertEqual(expected_output, acceptor.output_string.strip())

        self.assertTrue(acceptor.can_accept_string(self.test_empty_string))
        self.assertEqual('*e*', acceptor.output_string.strip())

    def test_fst2(self):
        """
        Tests for FST2
        :return: void
        """
        fst_filename = './TestFSTs/fst2'

        with open(fst_filename, "r") as fst_file:
            fst_rules = fst_file.readlines()

        expected_output = '"b" "b" "b" "b" "c"'

        acceptor = FSTAcceptor(fst_rules)

        self.assertFalse(acceptor.can_accept_string(self.test_string1))

        self.assertTrue(acceptor.can_accept_string(self.test_string2))
        self.assertEqual(expected_output, acceptor.output_string.strip())

        self.assertTrue(acceptor.can_accept_string(self.test_empty_string))
        self.assertEqual('"c"', acceptor.output_string.strip())

    def test_fst3(self):
        """
        Tests for FST3
        :return: void
        """
        fst_filename = './TestFSTs/fst3'

        with open(fst_filename, "r") as fst_file:
            fst_rules = fst_file.readlines()

        expected_output = '"b" "c" "b" "c" "g"'

        acceptor = FSTAcceptor(fst_rules)

        self.assertFalse(acceptor.can_accept_string(self.test_string1))

        self.assertTrue(acceptor.can_accept_string(self.test_string2))
        self.assertEqual(expected_output, acceptor.output_string.strip())

        self.assertTrue(acceptor.can_accept_string(self.test_empty_string))
        self.assertEqual('"g"', acceptor.output_string.strip())


def main():
    """
    Parse the system arguments, call the FSTAcceptor class and write results to the output file
    :return:
    """
    fst_filename = sys.argv[1]
    test_filename = sys.argv[2]

    with open(fst_filename, "r") as fst_file:
        fst_rules = fst_file.readlines()

    acceptor = FSTAcceptor(fst_rules)

    with open(test_filename, "r") as test_file:
        test_strings = test_file.readlines()

    for string in test_strings:
        output = acceptor.can_accept_string(string)
        output_string = acceptor.output_string
        output_prob = acceptor.output_probability
        print(string.strip(whitespace) + " => " + (output_string + " " + str(output_prob) if output else "*none* 0"))


if __name__ == "__main__":
    main()
