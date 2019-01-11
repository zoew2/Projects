import sys
from unittest import TestCase
from math import log10
from collections import defaultdict


class Viterbi:
    """
    This class uses the Viterbi algorithm to find the most probable sequence of states
    through the given HMM for a given observation
    """

    # dictionary of initial probabilities
    initials = defaultdict(float)

    # 2d dictionary of transition probabilities
    transitions = {}

    # 2d dictionary of emission probabilities
    emissions = {}

    # mapping of states to indicies
    state2idx = {}

    # mapping of indicies to states
    idx2state = {}

    # mapping of symbols to indicies
    symbol2idx = {}

    # constant for the unknown emission character
    UNK = "<unk>"

    def __init__(self, hmm_file):
        """
        Initalize this class by reading in the HMM file
        :param hmm_file: the given hmm file
        """

        expected_init = int(hmm_file[2].split("=")[1])
        expected_trans = int(hmm_file[3].split("=")[1])
        expected_emiss = int(hmm_file[4].split("=")[1])

        clean_hmm = [x.strip() for x in hmm_file]

        init_index = clean_hmm.index("\init") + 1
        trans_index = clean_hmm.index("\\transition") + 1
        emiss_index = clean_hmm.index("\emission") + 1

        initials = hmm_file[init_index:(init_index + expected_init)]
        transitions = hmm_file[trans_index:(trans_index + expected_trans)]
        emissions = hmm_file[emiss_index:(emiss_index + expected_emiss)]

        self.load_hmm(initials, transitions, emissions)

    def load_hmm(self, initials, transitions, emissions):
        """
        Load in an HMM by saving the initial, transition and emission probabilities
        :param initials: initial probability lines
        :param transitions: transition probability lines
        :param emissions: emission probability lines
        :return: void
        """
        # load the initial probabilities
        for initial in initials:
            initial_list = initial.split()
            initial_state = initial_list[0]
            initial_prob = float(initial_list[1])

            # if the probability is not between 0 and 1 log an error and continue
            if initial_prob > 1 or initial_prob < 0:
                sys.stderr.write("warning: the prob is not in [0,1] range: " + initial)
            self.initials[self.get_state_id(initial_state)] = initial_prob

        # load the transition probabilities
        for transition in transitions:
            transition_list = transition.split()
            from_state = transition_list[0]
            to_state = transition_list[1]
            transition_prob = float(transition_list[2])

            # if the probability is not between 0 and 1 log an error and continue
            if transition_prob > 1 or transition_prob < 0:
                sys.stderr.write("warning: the prob is not in [0,1] range: " + transition)
            self.transitions[self.get_state_id(from_state)][self.get_state_id(to_state)] = transition_prob

        # load the emission probabilities
        for emission in emissions:
            emission_list = emission.split()
            emission_state = emission_list[0]
            emission = emission_list[1]
            emission_prob = float(emission_list[2])

            # if the probability is not between 0 and 1 log and error
            if emission_prob > 1 or emission_prob < 0:
                sys.stderr.write("warning: the prob is not in [0,1] range: " + emission)
            self.emissions[self.get_state_id(emission_state)][self.get_symbol_id(emission, True)] = emission_prob

    def get_state_id(self, state):
        """
        Get the index mapped to the given state
        Insert it into the mapping if needed
        :param state: the given state string
        :return: int
        """
        if state not in self.state2idx:
            self.state2idx[state] = len(self.transitions)
            self.idx2state[self.state2idx[state]] = state
            self.transitions[self.state2idx[state]] = defaultdict(float)
            self.emissions[self.state2idx[state]] = defaultdict(float)

        return self.state2idx[state]

    def get_symbol_id(self, symbol, insert=False):
        """
        Get the index mapped to the given symbol
        Insert it if needed and indicated
        :param symbol: the given symbol string
        :param insert: whether to insert into the mapping
        :return: int
        """
        if symbol not in self.symbol2idx:
            if insert:
                self.symbol2idx[symbol] = len(self.symbol2idx)
            else:
                return self.symbol2idx[self.UNK]

        return self.symbol2idx[symbol]

    def run_viterbi(self, observation):
        """
        Run the viterbi algorithm to find the best path through the HMM for the given observation string
        :param observation: the given observation string
        :return: the best path and probability
        """
        observations = observation.split()

        # initialize the trellis as an empty dictionary
        trellis = [{}]

        # loop through every state with an initial probability
        for state in [x for x in self.idx2state if x in self.initials]:

            # set first series of nodes in the trellis to the initial probability for that state with an empty backtrace
            trellis[0][state] = (self.initials[state], [])

        # loop through the items in the observation, with timesteps starting at 1
        for time in range(1, len(observations)+1):

            # get the index for the observation at this timestep
            symbol_id = self.get_symbol_id(observations[time - 1])

            # add a new dictionary to the trellis for this timestep
            trellis.append({})

            # loop through every state which has a non-zero emission probability for the observation at this timestep
            for state in [x for x in self.idx2state if symbol_id in self.emissions[x]]:

                # initialize the max probability and previous state as zeros to start
                max_trellis_prob = 0
                previous_state_selected = 0

                # loop through every state which has a non-zero probability at the previous timestep
                for prev_state in [x for x in self.idx2state if x in trellis[time-1]]:

                    # calculate the probability for this node
                    trellis_prob = trellis[time - 1][prev_state][0] * self.transitions[prev_state][state]

                    # if this is the highest probable next step for the path, save it as the max
                    if trellis_prob > max_trellis_prob:
                        max_trellis_prob = trellis_prob
                        previous_state_selected = prev_state

                # add in the emission probability to the highest probable value
                max_prob = max_trellis_prob * self.emissions[state][symbol_id]

                # if the probability is non-zero, add it into the trellis
                if max_prob > 0:
                    trace = trellis[time - 1][previous_state_selected][1][:]
                    trace.append(previous_state_selected)
                    trellis[time][state] = (max_prob, trace)

        # find the path and probability value for the best path
        sequence = []
        max_max_prob = max(value[0] for value in trellis[-1].values())
        for index, value in trellis[-1].items():
            if value[0] == max_max_prob:
                backtrace = value[1].copy()
                backtrace.append(index)
                sequence = [self.idx2state[x] for x in backtrace]

        # calculate the log prob
        max_max_prob = log10(max_max_prob) if max_max_prob > 0 else 0

        # return the results in the correct format
        return observation.strip() + " => " + " ".join(sequence) + " " + str(max_max_prob)


class TestViterbi(TestCase):
    """
    This class contains tests for the Viterbi class
    """

    maxDiff = None

    test_input = [
        'the cat ate the rat',
        'blue cats are fake'
    ]

    test_expected = [
        'the cat ate the rat => BOS_BOS BOS_DT DT_N N_V V_DT DT_N -2.9901019295842777',
        'blue cats are fake => BOS_BOS BOS_JJ JJ_N N_V V_JJ -2.9220593322569814'
    ]

    def test_viterbi(self):
        """
        Tests for run_viterbi
        :return: void
        """

        hmm_filename = "./TestFiles/hmm"
        hmm_file = open(hmm_filename, "r")
        hmm = hmm_file.readlines()

        output = []

        viterbi = Viterbi(hmm)
        for sentence in self.test_input:
            output.append(viterbi.run_viterbi(sentence))
        self.assertCountEqual(output, self.test_expected)


def main():
    """
    Parse the system arguments, call the Viterbi class and write results to the output file
    :return:
    """
    hmm_filename = sys.argv[1]
    hmm_file = open(hmm_filename, "r")
    hmm = hmm_file.readlines()

    input_sentence_filename = sys.argv[2]
    input_sentence_file = open(input_sentence_filename, "r")
    input_sentences = input_sentence_file.readlines()

    output_filename = sys.argv[3]

    viterbi = Viterbi(hmm)
    with open(output_filename, "w") as output_file:
        for sentence in input_sentences:
            output_line = viterbi.run_viterbi(sentence)
            print(output_line, file=output_file)


if __name__ == "__main__":
    main()
