from string import whitespace
import sys
from unittest import TestCase


class FSAAcceptor:
    """
    This class determines if a given string is accepted by a given FSA
    """

    def __init__(self, fsa_rules):
        """
        Initialize the class by loading the FSA
        :param fsa_rules: a description of an FSA
        """
        self.fsa = self.load_fsa(fsa_rules)

    @staticmethod
    def load_fsa(fsa_rules):
        """
        Load the given FSA into a dictionary
        :param fsa_rules: a description of an FSA
        :return: dictionary representation of the FSA
        """
        fsa = {'start_state': '', 'final_states': [], 'transitions': {}}

        for line in fsa_rules:
            rule = line.split()

            if "(" not in rule[0]:
                # if this is not a transition, it's the final state
                fsa['final_states'] = [state for state in rule]
            else:
                # get the values for the transition
                first_state = rule[0].strip(whitespace + '"\'()')
                second_state = rule[1].strip(whitespace + '"\'()')
                arc_output = rule[2].strip(whitespace + '"\'()')

                if "*e*" in arc_output:
                    arc_output = ''
                if fsa['start_state'] == '':
                    fsa['start_state'] = first_state
                if first_state not in fsa['transitions'].keys():
                    fsa['transitions'][first_state] = {}

                fsa['transitions'][first_state].setdefault(arc_output, []).append(second_state)

        return fsa

    def can_accept_string(self, string):
        """
        Can this FSA accept the given string?
        :param string: the string to check for acceptance
        :return: bool
        """
        characters = [character.strip(whitespace + '"\'()') for character in string.split()]

        return self.can_reach_final_state(characters, 0, self.fsa['start_state'])

    def can_reach_final_state(self, characters, index, current_state):
        """
        Can we reach a final state from the current state?
        :param characters: the string of characters
        :param index: the current index of the string
        :param current_state: the current state
        :return: bool
        """
        accepted = False
        # if we've reached the end of the string and we're in a final state, we can accept the string
        if index == len(characters) and current_state in self.fsa['final_states']:
            return True
        # otherwise continue to attempt to transition towards a final state
        elif current_state in self.fsa['transitions']:
            if index < len(characters) and characters[index] in self.fsa['transitions'][current_state]:
                for state in self.fsa['transitions'][current_state][characters[index]]:
                    accepted = self.can_reach_final_state(characters, index+1, state)
            if '' in self.fsa['transitions'][current_state]:
                for state in self.fsa['transitions'][current_state]['']:
                    accepted = accepted or self.can_reach_final_state(characters, index, state)

        return accepted


class TestFSAAcceptor(TestCase):
    """
    This class contains tests for the FSAAcceptor class
    """

    test_string1 = '"a" "a" "b"'
    test_string2 = '"a" "a"'
    test_string3 = '"b"'
    test_string4 = '"a" "b" "a"'
    test_string5 = '"a" "c"'

    def test_fsa1(self):
        """
        Tests for FSA1
        :return: void
        """
        fsa_filename = './TestFiles/fsa1'

        with open(fsa_filename, "r") as fsa_file:
            fsa_rules = fsa_file.readlines()

        acceptor = FSAAcceptor(fsa_rules)

        self.assertTrue(acceptor.can_accept_string(self.test_string1))
        self.assertTrue(acceptor.can_accept_string(self.test_string2))
        self.assertTrue(acceptor.can_accept_string(self.test_string3))
        self.assertFalse(acceptor.can_accept_string(self.test_string4))
        self.assertFalse(acceptor.can_accept_string(self.test_string5))

    def test_fsa2(self):
        """
        Tests for FSA2
        :return: void
        """
        fsa_filename = './TestFiles/fsa2'

        with open(fsa_filename, "r") as fsa_file:
            fsa_rules = fsa_file.readlines()

        acceptor = FSAAcceptor(fsa_rules)

        self.assertFalse(acceptor.can_accept_string(self.test_string1))
        self.assertFalse(acceptor.can_accept_string(self.test_string2))
        self.assertFalse(acceptor.can_accept_string(self.test_string3))
        self.assertFalse(acceptor.can_accept_string(self.test_string4))
        self.assertTrue(acceptor.can_accept_string(self.test_string5))

    def test_fsa3(self):
        """
        Tests for FSA3
        :return: void
        """
        fsa_filename = './TestFiles/fsa3'

        with open(fsa_filename, "r") as fsa_file:
            fsa_rules = fsa_file.readlines()

        acceptor = FSAAcceptor(fsa_rules)

        self.assertFalse(acceptor.can_accept_string(self.test_string1))
        self.assertFalse(acceptor.can_accept_string(self.test_string2))
        self.assertTrue(acceptor.can_accept_string(self.test_string3))
        self.assertFalse(acceptor.can_accept_string(self.test_string4))
        self.assertTrue(acceptor.can_accept_string(self.test_string5))

    def test_fsa4(self):
        """
        Tests for FSA4
        :return:
        """
        fsa_filename = './TestFiles/fsa4'

        with open(fsa_filename, "r") as fsa_file:
            fsa_rules = fsa_file.readlines()

        acceptor = FSAAcceptor(fsa_rules)

        self.assertFalse(acceptor.can_accept_string(self.test_string1))
        self.assertFalse(acceptor.can_accept_string(self.test_string2))
        self.assertFalse(acceptor.can_accept_string(self.test_string3))
        self.assertFalse(acceptor.can_accept_string(self.test_string4))
        self.assertFalse(acceptor.can_accept_string(self.test_string5))


def main():
    """
    Parse the system arguments, call the FSAAcceptor class and write results to the output file
    :return:
    """
    fsa_filename = sys.argv[1]
    test_filename = sys.argv[2]

    with open(fsa_filename, "r") as fsa_file:
        fsa_rules = fsa_file.readlines()

    acceptor = FSAAcceptor(fsa_rules)

    with open(test_filename, "r") as test_file:
        test_strings = test_file.readlines()

    for string in test_strings:
        print(string.strip() + " => " + ("yes" if acceptor.can_accept_string(string) else "no"))


if __name__ == "__main__":
    main()
