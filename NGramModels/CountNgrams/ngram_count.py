import sys
from unittest import TestCase


class NgramCount:
    """
    This class collects unigram, bigram and trigram frequency counts
    """

    # a dictionary of unigrams and counts
    unigrams = {}

    # a dictionary of bigrams and counts
    bigrams = {}

    # a dictionary of trigrams and counts
    trigrams = {}

    def __init__(self, input_sentences):
        """
        Initialize the class counting the ngrams in the given sentences
        :param input_sentences: the given sentences
        """
        self.count_ngrams(input_sentences)

    def count_ngrams(self, input_sentences):
        """
        Count the ngrams in the given sentences
        :param input_sentences: the given sentences
        :return: void
        """
        for sentence in input_sentences:

            if not sentence.strip():
                continue

            tagged_sentence = "<s> " + sentence.strip() + " </s>"
            words = tagged_sentence.strip().split(" ")

            for word_index in range(len(words)):

                unigram = words[word_index]
                bigram = unigram + " " + words[word_index+1] if word_index + 1 < len(words) else ""
                trigram = bigram + " " + words[word_index+2] if word_index + 2 < len(words) else ""

                self.unigrams.setdefault(unigram, 0)
                self.unigrams[unigram] += 1

                if bigram:
                    self.bigrams.setdefault(bigram, 0)
                    self.bigrams[bigram] += 1

                if trigram:
                    self.trigrams.setdefault(trigram, 0)
                    self.trigrams[trigram] += 1

    def ngrams_to_string_sorted(self):
        """
        Return the sorted ngram counts
        :return: a sorted string representation of the ngram counts
        """
        output_string = ""

        for unigram, count in sorted(self.unigrams.items(), key=lambda kv: (-kv[1], kv[0])):
            output_string += str(count) + "\t" + unigram + "\n"
        for bigram, count in sorted(self.bigrams.items(), key=lambda kv: (-kv[1], kv[0])):
            output_string += str(count) + "\t" + bigram + "\n"
        for trigram, count in sorted(self.trigrams.items(), key=lambda kv: (-kv[1], kv[0])):
            output_string += str(count) + "\t" + trigram + "\n"

        return output_string.strip()


class TestNgramCount(TestCase):
    """
    This class contains tests for the NgramCount class
    """

    maxDiff = None

    test_sentences = ['this is a test for the counter so this is a test sentence']

    def test_ngram_count(self):
        """
        Tests for ngram_count
        :return: void
        """

        counter = NgramCount(self.test_sentences)
        ngrams = counter.ngrams_to_string_sorted()

        with open('./TestFiles/ngrams', "r") as expected_ngrams:
            test_expected = expected_ngrams.readlines()
        self.assertEqual(ngrams.split("\n"), [x.strip("\n") for x in test_expected])


def main():
    """
    Parse the system arguments, call the NgramCount class and write results to the output file
    :return:
    """
    sentence_filename = sys.argv[1]
    sentences_file = open(sentence_filename, "r")
    sentences = sentences_file.readlines()

    output_filename = sys.argv[2]

    with open(output_filename, "w") as output_file:
        counter = NgramCount(sentences)
        print(counter.ngrams_to_string_sorted(), file=output_file)


if __name__ == "__main__":
    main()
