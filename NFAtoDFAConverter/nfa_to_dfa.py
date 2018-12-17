from string import whitespace
import sys
from unittest import TestCase


class NFAtoDFA:

    dfa = {'start_state': '', 'final_state': '', 'transitions': {}}
    vocabulary = []
    final_states = []

    def __init__(self, nfa_rules):
        """
        Initialize the class by loading the FSA
        :param nfa_rules: a description of an FSA
        """
        self.nfa = self.load_nfa(nfa_rules)

    def load_nfa(self, nfa_rules):
        """
        Load the given NFA into a dictionary
        :param nfa_rules: a description of an NFA
        :return: dictionary representation of the NFA
        """
        nfa = {'start_state': '', 'final_state': '', 'transitions': {}}

        for line in nfa_rules:
            rule = line.strip().split()

            if not rule[0]:
                continue
            if "(" not in rule[0] and nfa['final_state'] == '':
                # if this is not a transition, it's the final state
                nfa['final_state'] = rule[0]
            else:
                # get the values for the transition
                first_state = rule[0].strip(whitespace + '"\'()')
                second_state = rule[1].strip(whitespace + '"\'()')
                arc_output = rule[2].strip(whitespace + '"\'()')

                if "*e*" in arc_output:
                    arc_output = ''

                if arc_output not in self.vocabulary and arc_output != '':
                    self.vocabulary.append(arc_output)

                if nfa['start_state'] == '':
                    nfa['start_state'] = first_state

                if first_state not in nfa['transitions']:
                    nfa['transitions'][first_state] = {}

                nfa['transitions'][first_state].setdefault(arc_output, []).append(second_state)

        return nfa

    def convert_nfa_to_dfa(self):
        """
        Convert the NFA to a DFA
        :return: void
        """
        start_states = self.epsilon_closure(self.nfa['start_state'], [self.nfa['start_state']])
        self.dfa['start_state'] = "-".join(sorted(start_states))
        self.add_new_states(start_states)
        if len(self.final_states) == 1:
            self.dfa['final_state'] = self.final_states[0]
        else:
            self.dfa['final_state'] = 'FinalState'
            for final_state in self.final_states:
                self.dfa['transitions'][final_state] = {}
                self.dfa['transitions'][final_state][''] = 'FinalState'

    def add_new_states(self, states):
        """
        Add a new state to the DFA
        :param states: an array of states
        :return: void
        """
        for character in self.vocabulary:
            next_states = []
            for state in states:
                next_states = list(set(self.epsilon_closure(state, []) + next_states))
                if state in self.nfa['transitions'] and character in self.nfa['transitions'][state]:
                    for next_state in self.nfa['transitions'][state][character]:
                        epsilon_closure_states = self.epsilon_closure(next_state, [next_state])
                        next_states = list(set(epsilon_closure_states + next_states))

            first_state = "-".join(sorted(states))
            second_state = "-".join(sorted(next_states))
            if first_state not in self.dfa['transitions']:
                self.dfa['transitions'][first_state] = {}
            if next_states:
                self.dfa['transitions'][first_state][character] = second_state
            if self.nfa['final_state'] in next_states and second_state not in self.final_states:
                self.final_states.append(second_state)
            if second_state not in self.dfa['transitions']:
                self.add_new_states(next_states)

    def epsilon_closure(self, state, next_states):
        """
        Get the epsilon closure for the given state
        :param state: state in NFA
        :param next_states: states that can be reached from the given NFA state
        :return: list of states that can be reached
        """
        if state in self.nfa['transitions'] and '' in self.nfa['transitions'][state]:
            for next_state in self.nfa['transitions'][state]['']:
                if next_state not in next_states:
                    next_states.append(next_state)
                    next_states = self.epsilon_closure(next_state, next_states)

        return next_states

    def print_in_carmel_format(self):
        """
        Print the DFA in carmel format
        :return: a string representation of the DFA in carmel format
        """
        output_string = ""
        output_string += self.dfa['final_state'] + "\n"
        start_state = self.dfa['start_state']

        for character in self.dfa['transitions'][start_state]:
            second_state = self.dfa['transitions'][start_state][character]
            output_string += "(" + start_state + " (" + second_state + ' "' + character + '"))\n'

        for first_state in self.dfa['transitions']:
            if first_state != start_state:
                for character in self.dfa['transitions'][first_state]:
                    second_state = self.dfa['transitions'][first_state][character]
                    output_string += "(" + first_state + " (" + second_state + ' "' + character + '"))\n'
        return output_string.strip()


class TestNFAtoDFA(TestCase):
    """
    This class contains tests for the NFAtoDFA class
    """

    maxDiff = None

    def test_epsilon_closure(self):
        """
        Test the epsilon_closure function
        :return:
        """

        nfa_filename = './TestFSAs/nfa1'

        with open(nfa_filename, "r") as nfa_file:
            nfa_rules = nfa_file.readlines()

        converter = NFAtoDFA(nfa_rules)
        expected = ['0', '1', '2', '4', '7']

        self.assertEqual(expected, converter.epsilon_closure(converter.nfa['start_state'], [converter.nfa['start_state']]))

    def test_nfa1(self):
        """
        Tests for NFA1
        :return: void
        """
        nfa_filename = './TestFSAs/nfa1'

        with open(nfa_filename, "r") as nfa_file:
            nfa_rules = nfa_file.readlines()

        converter = NFAtoDFA(nfa_rules)
        converter.convert_nfa_to_dfa()

        dfa_filename = './TestFSAs/dfa1'

        with open(dfa_filename, "r") as dfa_file:
            expected = [line.strip("\n") for line in dfa_file.readlines()]

        self.assertCountEqual(expected, converter.print_in_carmel_format().split("\n"))

    def test_nfa2(self):
        """
        Tests for NFA2
        :return: void
        """
        nfa_filename = './TestFSAs/nfa2'

        with open(nfa_filename, "r") as nfa_file:
            nfa_rules = nfa_file.readlines()

        converter = NFAtoDFA(nfa_rules)
        converter.convert_nfa_to_dfa()

        dfa_filename = './TestFSAs/dfa2'

        with open(dfa_filename, "r") as dfa_file:
            expected = [line.strip("\n") for line in dfa_file.readlines()]

        self.assertCountEqual(expected, converter.print_in_carmel_format().split("\n"))


def main():
    """
    Parse the system arguments, call the NFAtoDFA class and write results to the output file
    :return: void
    """
    nfa_filename = sys.argv[1]

    with open(nfa_filename, "r") as nfa_file:
        nfa_rules = nfa_file.readlines()

    converter = NFAtoDFA(nfa_rules)
    converter.convert_nfa_to_dfa()

    print(converter.print_in_carmel_format())


if __name__ == "__main__":
    main()
