import sys
from unittest import TestCase
from math import log10


class BuildLanguageModel:
    """
    This class builds a language model with the given ngram counts
    """

    def __init__(self, ngram_counts):
        """
        Initialize the class with the given ngram counts
        :param ngram_counts: the given ngram counts
        """
        self.unigram_model = self.build_unigram_model(ngram_counts)
        self.bigram_model = self.build_bigram_model(ngram_counts)
        self.trigram_model = self.build_trigram_model(ngram_counts)

    @staticmethod
    def build_unigram_model(ngram_counts):
        """
        Build a unigram language model with the given ngram counts
        :param ngram_counts: the given ngram counts
        :return: a dictionary representation of the unigram model
        """
        model = {'types': 0, 'tokens': 0, 'unigrams': {}}
        types = 0
        tokens = 0
        for line in ngram_counts:
            # if this line is not a unigram count, skip it
            if not line.strip() or len(line.strip().split()) is not 2:
                continue
            line_list = line.strip().split()
            count = int(line_list[0])
            unigram = line_list[1]

            model['unigrams'][unigram] = {}
            model['unigrams'][unigram]['count'] = count

            types += 1
            tokens += count

        model['types'] = types
        model['tokens'] = tokens

        # calculate the probability and log probability for each unigram now that we have the totals
        for unigram in model['unigrams'].keys():

            count = model['unigrams'][unigram]['count']
            total = model['tokens']

            model['unigrams'][unigram]['prob'] = count/total
            model['unigrams'][unigram]['logprob'] = log10(count/total)

        return model

    def build_bigram_model(self, ngram_counts):
        """
        Build a bigram language model with the given ngram counts
        :param ngram_counts: the given ngram counts
        :return: a dictionary representation of the bigram model
        """
        model = {'types': 0, 'tokens': 0, 'bigrams': {}}
        types = 0
        tokens = 0
        for line in ngram_counts:
            # if this line is not a bigram count, skip it
            if not line.strip() or len(line.strip().split()) is not 3:
                continue
            line_list = line.strip().split()
            count = int(line_list[0])
            w1 = line_list[1]
            w2 = line_list[2]
            unigram_count = self.unigram_model['unigrams'][w1]['count']

            bigram = w1 + " " + w2

            model['bigrams'][bigram] = {}
            model['bigrams'][bigram]['count'] = count
            model['bigrams'][bigram]['words'] = [w1, w2]

            #calculate the probability using maximum likelihood estimation
            model['bigrams'][bigram]['prob'] = count / unigram_count
            model['bigrams'][bigram]['logprob'] = log10(model['bigrams'][bigram]['prob'])

            types += 1
            tokens += count

        model['types'] = types
        model['tokens'] = tokens

        return model

    def build_trigram_model(self, ngram_counts):
        """
        Build a trigram language model with the given ngram counts
        :param ngram_counts: the given ngram counts
        :return: a dictionary representation of the trigram model
        """
        model = {'types': 0, 'tokens': 0, 'trigrams': {}}
        types = 0
        tokens = 0
        for line in ngram_counts:
            # if this line is not a bigram count, skip it
            if not line.strip() or len(line.strip().split()) is not 4:
                continue
            line_list = line.strip().split()
            count = int(line_list[0])
            w1 = line_list[1]
            w2 = line_list[2]
            w3 = line_list[3]
            bigram_count = self.bigram_model['bigrams'][w1 + " " + w2]['count']

            trigram = w1 + " " + w2 + " " + w3

            model['trigrams'][trigram] = {}
            model['trigrams'][trigram]['count'] = count

            #calculate the probability using maximum likelihood estimation
            model['trigrams'][trigram]['prob'] = count / bigram_count
            model['trigrams'][trigram]['logprob'] = log10(count / bigram_count)

            types += 1
            tokens += count

        model['types'] = types
        model['tokens'] = tokens

        return model

    def language_model_to_string_arpa(self):
        """
        Return the language model in ARPA format
        :return: a string representation of the language model
        """
        output_string = "\\data\\\n"
        output_string += "ngram 1: type=" + str(self.unigram_model['types']) + " token=" + str(self.unigram_model['tokens']) + "\n"
        output_string += "ngram 2: type=" + str(self.bigram_model['types'])+ " token=" + str(self.bigram_model['tokens']) + "\n"
        output_string += "ngram 3: type=" + str(self.trigram_model['types']) + " token=" + str(self.trigram_model['tokens']) + "\n"

        output_string += "\n\\1-grams:\n"
        for ngram, info in sorted(self.unigram_model['unigrams'].items(), key=lambda kv: (-kv[1]['count'], kv[0])):
            output_string += str(info['count']) + "\t" + '%.10f'%(info['prob']) + "\t" + '%.10f'%(info['logprob']) + "\t" + ngram + "\n"

        output_string += "\n\\2-grams:\n"
        for ngram, info in sorted(self.bigram_model['bigrams'].items(), key=lambda kv: (-kv[1]['count'], kv[0])):
            output_string += str(info['count']) + "\t" + '%.10f'%(info['prob']) + "\t" + '%.10f'%(info['logprob']) + "\t" + ngram + "\n"

        output_string += "\n\\3-grams:\n"
        for ngram, info in sorted(self.trigram_model['trigrams'].items(), key=lambda kv: (-kv[1]['count'], kv[0])):
            output_string += str(info['count']) + "\t" + '%.10f'%(info['prob']) + "\t" + '%.10f'%(info['logprob']) + "\t" + ngram + "\n"

        output_string += "\n\\end\\"

        return output_string.strip()


class TestBuildLanguageModel(TestCase):
    """
    This class contains tests for the NgramCount class
    """

    maxDiff = None

    test_ngram_count = [
        '2\ta',
        '2\tis',
        '2\ttest',
        '2\tthis',
        '1\t</s>',
        '1\t<s>',
        '1\tcounter',
        '1\tfor',
        '1\tsentence',
        '1\tso',
        '1\tthe',
        '2\ta test',
        '2\tis a',
        '2\tthis is',
        '1\t<s> this',
        '1\tcounter so',
        '1\tfor the',
        '1\tsentence </s>',
        '1\tso this',
        '1\ttest for',
        '1\ttest sentence',
        '1\tthe counter',
        '2\tis a test',
        '2\tthis is a',
        '1\t<s> this is',
        '1\ta test for',
        '1\ta test sentence',
        '1\tcounter so this',
        '1\tfor the counter',
        '1\tso this is',
        '1\ttest for the',
        '1\ttest sentence </s>',
        '1\tthe counter so'
    ]

    test_expected = [
        '\\data\\',
        'ngram 1: type=11 token=15',
        'ngram 2: type=11 token=14',
        'ngram 3: type=11 token=13',
        '',
        '\\1-grams:',
        '2\t0.1333333333\t-0.8750612634\ta',
        '2\t0.1333333333\t-0.8750612634\tis',
        '2\t0.1333333333\t-0.8750612634\ttest',
        '2\t0.1333333333\t-0.8750612634\tthis',
        '1\t0.0666666667\t-1.1760912591\t</s>',
        '1\t0.0666666667\t-1.1760912591\t<s>',
        '1\t0.0666666667\t-1.1760912591\tcounter',
        '1\t0.0666666667\t-1.1760912591\tfor',
        '1\t0.0666666667\t-1.1760912591\tsentence',
        '1\t0.0666666667\t-1.1760912591\tso',
        '1\t0.0666666667\t-1.1760912591\tthe',
        '',
        '\\2-grams:',
        '2\t1.0000000000\t0.0000000000\ta test',
        '2\t1.0000000000\t0.0000000000\tis a',
        '2\t1.0000000000\t0.0000000000\tthis is',
        '1\t1.0000000000\t0.0000000000\t<s> this',
        '1\t1.0000000000\t0.0000000000\tcounter so',
        '1\t1.0000000000\t0.0000000000\tfor the',
        '1\t1.0000000000\t0.0000000000\tsentence </s>',
        '1\t1.0000000000\t0.0000000000\tso this',
        '1\t0.5000000000\t-0.3010299957\ttest for',
        '1\t0.5000000000\t-0.3010299957\ttest sentence',
        '1\t1.0000000000\t0.0000000000\tthe counter',
        '',
        '\\3-grams:',
        '2\t1.0000000000\t0.0000000000\tis a test',
        '2\t1.0000000000\t0.0000000000\tthis is a',
        '1\t1.0000000000\t0.0000000000\t<s> this is',
        '1\t0.5000000000\t-0.3010299957\ta test for',
        '1\t0.5000000000\t-0.3010299957\ta test sentence',
        '1\t1.0000000000\t0.0000000000\tcounter so this',
        '1\t1.0000000000\t0.0000000000\tfor the counter',
        '1\t1.0000000000\t0.0000000000\tso this is',
        '1\t1.0000000000\t0.0000000000\ttest for the',
        '1\t1.0000000000\t0.0000000000\ttest sentence </s>',
        '1\t1.0000000000\t0.0000000000\tthe counter so',
        '',
        '\\end\\'
    ]

    def test_build_language_model(self):
        """
        Tests for build_language_model
        :return: void
        """

        builder = BuildLanguageModel(self.test_ngram_count)
        model = builder.language_model_to_string_arpa()
        self.assertEquals(model.strip().split("\n"), self.test_expected)


def main():
    """
    Parse the system arguments, call the BuildLanguageModel class and write results to the output file
    :return:
    """
    ngram_counts_filename = sys.argv[1]
    ngram_counts_file = open(ngram_counts_filename, "r")
    ngram_counts = ngram_counts_file.readlines()

    output_filename = sys.argv[2]

    with open(output_filename, "w") as output_file:
        builder = BuildLanguageModel(ngram_counts)
        print(builder.language_model_to_string_arpa(), file=output_file)


if __name__ == "__main__":
    main()
