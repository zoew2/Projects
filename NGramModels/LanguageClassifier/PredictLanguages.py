import os
import sys
import glob
import re
import math
import operator
import numpy


def create_models():
    """
    Transform counts to probabilities and store the statistics in a dictionary for each language
    :return: language models in a dictionary
    """
    language_model_path = sys.argv[1]
    files = glob.glob(language_model_path)

    language_models = {}

    for file in files:
        language = os.path.splitext(os.path.basename(file))[0]
        language_models[language] = {}
        language_models[language]['probs'] = {}
        language_models[language]['total_count'] = 0

        for unigram in open(file):
            unigram = unigram.strip().split('\t')
            language_models[language]['probs'][unigram[0]] = int(unigram[1])
            language_models[language]['total_count'] += int(unigram[1])

    return language_models


def classify(models, line):
    """
    Classify a given line of text given a set of unigram probabilities
    :param models: A dictionary of unigram probabilities for each language
    :param line: A line of text
    :return: void
    """
    no_punctuation = re.sub(r"[.,!¡¥$£¿;:()\"\'—–\-/\[\]¹²³«»]", ' ', line)
    no_quotes = re.sub(r"(\s'+|'+\s)", ' ', no_punctuation)
    no_extra_whitespace = re.sub(r"\s+", ' ', no_quotes)

    probabilities = {}

    # for each language, determine the log prob
    for language, model in sorted(models.items()):
        probability = 0

        # sum the log probs for each word in the line
        for word in no_extra_whitespace.split(' '):
            words = model['probs'].keys()
            if word.strip() in words:
                word_count = model['probs'][word.strip()]
            else:
                word_count = 0

            # add one to the numerator and denominator for Laplace smoothing
            probability += math.log(word_count + 1/(model['total_count'] + 1), 10)

        probabilities[probability] = language
        print(language + "\t" + str(probability))

    # sort the probabilities for this line from highest to lowest
    sorted_probs = sorted(probabilities.items(), key=operator.itemgetter(0), reverse=True)

    # gather statistics and important data points about the probabilities
    mean = numpy.mean(list(probabilities.keys()))
    sd = numpy.std(list(probabilities.keys()))
    mean_diff = mean - sorted_probs[0][0]
    first_diff = abs(sorted_probs[0][0] - sorted_probs[1][0])

    # our threshold is that the most likely language is more than one standard deviation from the mean
    # and the difference between the first and second probabilities is more than 10
    # otherwise we decide the language is unknown
    best_match = 'unk'
    if abs(mean_diff) > abs(sd) and abs(first_diff) > 10:
        best_match = sorted_probs[0][1]
    print("result " + best_match + "\n")


def main():
    """
    Store the language models and use them to classify the given text
    :return: void
    """
    models = create_models()
    test_data = sys.argv[2]

    # for each line, determine the most likely language
    for line in open(test_data):
        print(line.strip())
        classify(models, line)


if __name__ == "__main__":
    main()
