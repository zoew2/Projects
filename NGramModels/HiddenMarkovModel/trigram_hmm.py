import sys
from unittest import TestCase
from math import log10
import numpy


class TrigramHiddenMarkovModel:
    """
    This class builds a hidden markov model using trigram counts
    """

    # 3d Numpy array of transition counts
    transitions = None

    # 2d Numpy array of emission counts
    emissions = None

    # mappings for tags and symbols
    tag2idx = {}
    idx2tag = {}
    symbol2idx = {}
    idx2symbol = {}

    # counts of tags and symbols
    tagset = set()
    vocab = set()
    tokens = 0

    # CONSTANTS
    START_TAG = "BOS_BOS"
    BOS_TAG = "<s>"
    EOS_TAG = "<\s>"
    UNK_SYMBOL = "<unk>"
    BOS = "BOS"
    EOS = "EOS"
    BOUNDARIES = [BOS, EOS]

    def __init__(self, tagged_input, unknown_probabilities, lambda_1, lambda_2, lambda_3):
        """
        Initialize the class with counts and matricies
        :param tagged_input: tagged input sentences
        :param unknown_probabilities: given unknown probabilities
        :param lambda_1: lambda 1 value
        :param lambda_2: lambda 2 value
        :param lambda_3: lambda 3 value
        """
        self.initialize_data_structures(tagged_input)
        self.save_unknown_probabilities(unknown_probabilities)
        self.lambda1 = float(lambda_1)
        self.lambda2 = float(lambda_2)
        self.lambda3 = float(lambda_3)

        for line in tagged_input:
            self.build_model(line)

    def initialize_data_structures(self, tagged_input):
        """
        Count total observations and initialize matricies
        :param tagged_input: the tagged input sentences
        :return: void
        """
        for line in tagged_input:
            if not line:
                continue
            sentence = " ".join(["/".join([self.BOS_TAG, self.BOS]), line.strip(), "/".join([self.EOS_TAG, self.EOS])])
            self.tokens += len(sentence.split())
            for pair in sentence.split():
                pair_list = pair.rsplit("/", 1)
                word = pair_list[0]
                tag = pair_list[1]

                self.vocab.add(word)
                self.tagset.add(tag)

        tagset_size = len(self.tagset)+1
        vocab_size = len(self.vocab)+1
        self.transitions = numpy.zeros((tagset_size, tagset_size, tagset_size), dtype=int)
        self.emissions = numpy.zeros((tagset_size, vocab_size))

        for index, tag in enumerate(sorted(self.tagset)):
            self.tag2idx[tag] = index
            self.idx2tag[index] = tag

        self.vocab.add(self.UNK_SYMBOL)
        for index, symbol in enumerate(sorted(self.vocab)):
            self.symbol2idx[symbol] = index
            self.idx2symbol[index] = symbol

    def save_unknown_probabilities(self, unknown_probabilities):
        """
        Save unknown probabilities to a dictionary
        :param unknown_probabilities: given probabilities
        :return: void
        """
        for line in unknown_probabilities:
            probs = line.split()
            tag = probs[0]
            prob = float(probs[1])
            tag_index = self.tag2idx[tag]
            unk_index = self.symbol2idx[self.UNK_SYMBOL]
            self.emissions[tag_index][unk_index] = prob

    def build_model(self, tagged_data):
        """
        Build an hmm based on trigram counts in the tagged data
        :param tagged_data: the given tagged data
        :return: void
        """
        if not tagged_data.strip():
            return
        sentence = " ".join(["/".join([self.BOS_TAG, self.BOS]), tagged_data.strip(), "/".join([self.EOS_TAG, self.EOS])])

        t1 = ''
        t2 = self.BOS

        for pair in sentence.split():
            pair_list = pair.rsplit("/", 1)
            word = pair_list[0]
            t3 = pair_list[1]
            t3_index = self.tag2idx[t3]

            if t1 and t2:
                t1_index = self.tag2idx[t1]
                t2_index = self.tag2idx[t2]
                self.transitions[t1_index][t2_index][t3_index] += 1

            word_index = self.symbol2idx[word]
            self.emissions[t3_index][word_index] += 1

            t1 = t2
            t2 = t3
        t1_index = self.tag2idx[t1]
        t2_index = self.tag2idx[t2]
        self.transitions[t1_index][t2_index][t3_index] += 1

    def hmm_to_string(self):
        """
        Return a string representation of this HMM
        :return: string
        """
        output_string = []

        output_string.append("state_num=" + str(pow(len(self.tagset), 2)))
        output_string.append("sym_num=" + str(len(self.vocab)))
        output_string.append("init_line_num=1")
        transition_count = pow((len(self.transitions) - 1), 3)
        output_string.append("trans_line_num=" + str(transition_count))
        emission_count = numpy.count_nonzero(self.emissions) * (len(self.transitions)-1)
        output_string.append("emiss_line_num=" + str(emission_count))
        output_string.append("")

        output_string.append("\\init\nBOS_BOS\t1.0")
        output_string.append("")
        output_string.append("")
        output_string.append("\\transition")

        sorted_tagmap = sorted(self.tag2idx)
        for t1, t1_transitions in zip(sorted_tagmap, self.transitions):
            for t2, t2_transitions in zip(sorted_tagmap, t1_transitions):
                for t3, trigram_count in zip(sorted_tagmap, t2_transitions):
                    from_state = "_".join([t1, t2])
                    to_state = "_".join([t2, t3])
                    interpolated_prob = self.calculate_transition_probability(t1, t2, t3)
                    interpolated_log_prob = log10(interpolated_prob)
                    output_string.append("\t".join([from_state, to_state, '%.10f' % interpolated_prob, '%.10f' % interpolated_log_prob]))

        sorted_tagset = sorted(self.tagset)
        sorted_vocab = sorted(self.vocab)
        output_string.append("")
        output_string.append("\\emission")
        for first_tag in sorted_tagset:
            for second_tag in sorted_tagset:
                second_tag_index = self.tag2idx[second_tag]
                state = "_".join([first_tag, second_tag])
                for word, count in zip(sorted_vocab, self.emissions[second_tag_index]):
                    if count == 0:
                        continue
                    unk_index = self.symbol2idx[self.UNK_SYMBOL]
                    unk_count = self.emissions[second_tag_index][unk_index]
                    tag_count = sum(self.emissions[second_tag_index]) - unk_count
                    word_index = self.symbol2idx[word]
                    if tag_count > 0:
                        smoothed_prob = count / tag_count * (1 - unk_count) if word_index != unk_index else count
                        smoothed_log_prob = log10(smoothed_prob)
                        output_string.append("\t".join([state, word, '%.10f' % smoothed_prob, '%.10f' % smoothed_log_prob]))
        return "\n".join(output_string)

    def calculate_transition_probability(self, t1, t2, t3):
        """
        Calculate the interpolated probability for the given trigram
        :param t1: the first tag
        :param t2: the second tag
        :param t3: the third tag
        :return: interpolated probability
        """
        t1_index = self.tag2idx[t1]
        t2_index = self.tag2idx[t2]
        t3_index = self.tag2idx[t3]

        t3_count = sum([sum(x[t3_index]) for x in [y for y in self.transitions]])
        unigram_prob = t3_count / self.tokens

        t2_count = sum([sum(x[t2_index]) for x in [y for y in self.transitions]])
        t2_t3_count = sum(self.transitions[t2_index][t3_index]) if (t2 + "_" + t3 != self.START_TAG) else 0
        bigram_prob = (t2_t3_count / t2_count)

        t1_t2_count = sum(self.transitions[t1_index][t2_index]) if (t1 + "_" + t2 != self.START_TAG) else 0
        t1_t2_t3_count = self.transitions[t1_index][t2_index][t3_index]
        trigram_prob = 0 if t3 == self.BOS else (1/(len(self.tagset)-1) if t1_t2_count == 0 else t1_t2_t3_count / t1_t2_count)

        interpolated_prob = self.lambda1 * unigram_prob + self.lambda2 * bigram_prob + self.lambda3 * trigram_prob
        return interpolated_prob


class TestTrigramHiddenMarkovModel(TestCase):
    """
    This class contains tests for the NgramCount class
    """

    maxDiff = None

    unk_probs = [
        'DT\t0.01',
        'N\t0.01',
        'V\t0.01',
        'JJ\t0.01',
    ]

    test_tags = [
        'the/DT cat/N ate/V the/DT rat/N',
        'blue/JJ cats/N are/V fake/JJ'
    ]

    def test_build_hmm(self):
        """
        Tests for build_hmm
        :return: void
        """
        builder = TrigramHiddenMarkovModel(self.test_tags, self.unk_probs, 0.4, 0.3, 0.3)
        hmm = builder.hmm_to_string()
        hmm_filename = './TestFiles/hmm'

        with open(hmm_filename, "r") as hmm_file:
            test_expected = hmm_file.readlines()

        result = hmm.split("\n")
        expected = [x.strip("\n") for x in test_expected]

        self.assertCountEqual(result, expected)


def main():
    """
    Parse the system arguments, call the TrigramHiddenMarkovModel class and write results to the output file
    :return:
    """

    lambda1 = sys.argv[2]
    lambda2 = sys.argv[3]
    lambda3 = sys.argv[4]
    unk_prob_filename = sys.argv[5]
    unk_prob_file = open(unk_prob_filename, "r")
    unk_probs = unk_prob_file.readlines()

    output_filename = sys.argv[1]

    with open(output_filename, "w") as output_file:
        builder = TrigramHiddenMarkovModel(sys.stdin.readlines(), unk_probs, lambda1, lambda2, lambda3)
        print(builder.hmm_to_string(), file=output_file)


if __name__ == "__main__":
    main()
