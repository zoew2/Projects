import sys
from unittest import TestCase
from collections import defaultdict
import re


class MaxEntTagger:
    """
    This class collects word and feature frequencies and creates vectors
    """

    def __init__(self, rare_threshold, feature_threshold):
        """
        Initialize this class with the threshold values and empty dictionaries
        :param rare_threshold: threshold value for rare words
        :param feature_threshold: threshold value for features
        """
        self.rare_threshold = rare_threshold
        self.feature_threshold = feature_threshold

        self.word_freq = defaultdict(int)
        self.feat_freq = defaultdict(int)
        self.features = {}

        self.tag2idx = {}
        self.idx2tag = {}

    def count_words(self, line):
        """
        Count the words in the input file
        :return:
        """
        for word_index, pair in enumerate(line.split()):
            current_pair = pair.strip().rsplit("/", 1)
            current_word = current_pair[0]
            self.word_freq[current_word] += 1

    def print_counts(self):
        """
        Print the word frequencies in the required format
        :return:
        """
        output_string = list()

        for word, count in sorted(self.word_freq.items(), key=lambda kv: (-kv[1], kv[0])):
            output_string.append("\t".join([word, str(count)]))

        return "\n".join(output_string)

    def reset_features(self):
        """
        reset the feature vectors
        :return:
        """
        self.features = {}

    def get_tag_id(self, tag):
        """
        Get tag ID
        :param tag:
        :return:
        """
        if tag not in self.tag2idx:
            self.tag2idx[tag] = len(self.tag2idx)
            self.idx2tag[self.tag2idx[tag]] = tag

        return self.tag2idx[tag]

    def add_feature(self, word, feature_name, is_test):
        """
        Add a feature for the given word
        :param word: the word to add the feature for
        :param feature_name: the feature to add
        :param is_test: is this test data?
        :return:
        """
        self.features[word][feature_name] = 1
        if not is_test:
            self.feat_freq[feature_name] += 1

    def count_features(self, line, line_index, is_test=False):
        """
        Add all of Ratnaparkhi’s features for all the words in the line
        :param line: the current line of text
        :param line_index: index of the current line of text
        :param is_test: is this test data?
        :return:
        """
        words = line.split()
        # loop through words in the line
        for index in range(0, len(words)):
            current_pair = words[index].rsplit("/", 1)
            current_word = current_pair[0]
            word_string = str(line_index) + "-" + str(index) + "-" + current_word
            current_tag = current_pair[1]

            # get the necessary words and tags in the context

            self.features[word_string] = {}
            self.features[word_string]["tag"] = self.get_tag_id(current_tag)

            # add features depending on if the word is rare or not
            if self.word_freq[current_word] < self.rare_threshold:
                self.add_rare_features(current_word, word_string, is_test)
            else:
                self.add_feature(word_string, "curW=" + current_word, is_test)

            # add context features
            self.add_context_features(index, words, word_string, is_test)

    def add_context_features(self, index, words, word_string, is_test):
        """
        Add context features
        :param index: index of current words
        :param words: list of words
        :param word_string: current word
        :param is_test: is this test data?
        :return:
        """
        next2_word, next_word, prev2_tag, prev2_word, prev_tag, prev_word = self.get_context(index, words)

        self.add_feature(word_string, "prevT=" + prev_tag, is_test)
        self.add_feature(word_string, "prev2T=" + prev_tag + "+" + prev2_tag, is_test)
        self.add_feature(word_string, "prevW=" + prev_word, is_test)
        self.add_feature(word_string, "prev2W=" + prev2_word, is_test)
        self.add_feature(word_string, "nextW=" + next_word, is_test)
        self.add_feature(word_string, "next2W=" + next2_word, is_test)

    @staticmethod
    def get_context(index, words):
        """
        Get relevant context words and tags
        :param index: index of the current word
        :param words: list of words
        :return:
        """
        if index > 0:
            prev_pair = words[index - 1].split("/")
            prev_word = prev_pair[0]
            prev_tag = prev_pair[1]
        else:
            prev_word = prev_tag = "BOS"
        if index > 1:
            prev2_pair = words[index - 2].split("/")
            prev2_word = prev2_pair[0]
            prev2_tag = prev2_pair[1]
        else:
            prev2_word = prev2_tag = "BOS"
        if index < len(words) - 1:
            next_pair = words[index + 1].split("/")
            next_word = next_pair[0]
        else:
            next_word = "EOS"
        if index < len(words) - 2:
            next2_pair = words[index + 2].split("/")
            next2_word = next2_pair[0]
        else:
            next2_word = "EOS"
        return next2_word, next_word, prev2_tag, prev2_word, prev_tag, prev_word

    def add_rare_features(self, current_word, word_string, is_test):
        """
        Add all the features necessary for a rare word
        :param current_word: the current word
        :param is_test: the current word
        :return:
        """
        pref_1 = current_word[:1]
        self.add_feature(word_string, "pref=" + pref_1, is_test)
        suf_1 = current_word[-1:]
        self.add_feature(word_string, "suf=" + suf_1, is_test)
        if len(current_word) > 1:
            pref_2 = current_word[:2]
            self.add_feature(word_string, "pref=" + pref_2, is_test)
            suf_2 = current_word[-2:]
            self.add_feature(word_string, "suf=" + suf_2, is_test)
        if len(current_word) > 2:
            pref_3 = current_word[:3]
            self.add_feature(word_string, "pref=" + pref_3, is_test)
            suf_3 = current_word[-3:]
            self.add_feature(word_string, "suf=" + suf_3, is_test)
        if len(current_word) > 3:
            pref_4 = current_word[:4]
            self.add_feature(word_string, "pref=" + pref_4, is_test)
            suf_4 = current_word[-4:]
            self.add_feature(word_string, "suf=" + suf_4, is_test)
        if any(x.isupper() for x in current_word):
            self.add_feature(word_string, "containsUC", is_test)
        if any(x.isdigit() for x in current_word):
            self.add_feature(word_string, "containsNum", is_test)
        if any(x == "-" for x in current_word):
            self.add_feature(word_string, "containsHyphen", is_test)

    def print_init_features(self):
        """
        Print the initial features and frequencies
        :return:
        """
        output_string = list()

        for feature, count in sorted(self.feat_freq.items(), key=lambda kv: (-kv[1], kv[0])):
            output_string.append(" ".join([feature, str(count)]))

        return "\n".join(output_string)

    def print_kept_features(self):
        """
        Print the kept features based on the feature threshold
        :return:
        """
        output_string = list()

        for feature, count in sorted(self.feat_freq.items(), key=lambda kv: (-kv[1], kv[0])):
            if self.use_feature(feature):
                output_string.append(" ".join([feature, str(count)]))

        return "\n".join(output_string)

    def use_feature(self, feature_name):
        """
        Should this feature be used
        :param feature_name: the given feature
        :return:
        """
        if feature_name.startswith("curW"):
            return True
        if feature_name.startswith("tag") or self.feat_freq[feature_name] < self.feature_threshold:
            return False

        return True

    def print_features(self):
        """
        Print the feature vector
        :return:
        """
        output_string = list()

        for word, features in sorted(self.features.items()):
            feature_string = list()
            feature_string.append(word)
            feature_string.append(self.idx2tag[features["tag"]])
            for feature, count in sorted(features.items()):
                if self.use_feature(feature):
                    feature_string.append(feature)
                    feature_string.append(str(count))
            output_string.append(" ".join(feature_string))

        return re.sub(",", "comma", "\n".join(output_string))


class TestMaxEntTagger(TestCase):
    """
    This class contains tests for the MaxEntTagger class
    """

    maxDiff = None

    train_input = "This/DET is/VBD a/DET test/JJ file/NN with/PREP some/DET words/NP in/PREP it/NN\nThis/DET test/JJ " \
                  "file/NN has/VBD so/ADV many/JJ words/NP in/PREP it/NN\nRare/JJ word/NN test/NN"
    test_input = "Here/DET is/VBD another/DET test/JJ file/NN for/PREP testing/VBD\nSome/DET words/NNP are/VBD new/JJ"

    def count_words(self):
        for line in self.train_input.split("\n"):
            self.tagger.count_words(line)

    def count_features(self):
        for line_index, line in enumerate(self.train_input.split("\n")):
            self.tagger.count_features(line, line_index)

    def test_count_words(self):
        self.tagger = MaxEntTagger(2, 2)
        self.count_words()
        output = self.tagger.print_counts()

        with open('./TestFiles/word_freq', "r") as word_freq:
            test_word_freq = word_freq.readlines()

        self.assertEquals(output.split("\n"), [x.strip("\n") for x in test_word_freq])

    def test_init_features(self):
        self.tagger = MaxEntTagger(2, 2)
        self.count_words()
        self.count_features()
        output = self.tagger.print_init_features()

        with open('./TestFiles/init_freq', "r") as init_freq:
            test_init_freq = init_freq.readlines()

        self.assertEquals(output.split("\n"), [x.strip("\n") for x in test_init_freq])

    def test_kept_features(self):
        self.tagger = MaxEntTagger(2, 2)
        self.count_words()
        self.count_features()
        output = self.tagger.print_kept_features()

        with open('./TestFiles/kept_freq', "r") as kept_freq:
            test_kept_freq = kept_freq.readlines()

        self.assertEquals(output.split("\n"), [x.strip("\n") for x in test_kept_freq])

    def test_train_features(self):
        self.tagger = MaxEntTagger(2, 2)
        self.count_words()
        self.count_features()
        output = self.tagger.print_features()

        with open('./TestFiles/train_freq', "r") as train_freq:
            expected_train_freq = train_freq.readlines()

        self.assertEquals(output.split("\n"), [x.strip("\n") for x in expected_train_freq])

    def test_test_features(self):
        self.tagger = MaxEntTagger(2, 2)
        self.count_words()
        self.count_features()
        self.tagger.reset_features()

        for line_index, line in enumerate(self.test_input.split("\n")):
            self.tagger.count_features(line, line_index, True)
        output = self.tagger.print_features()

        with open('./TestFiles/test_freq', "r") as test_freq:
            expected_test_freq = test_freq.readlines()

        self.assertEquals(output.split("\n"), [x.strip("\n") for x in expected_test_freq])


def main():
    """
    Parse the system arguments, call the MaxEntTagger class and write results to the output file
    :return:
    """
    training_filename = sys.argv[1]
    training_file = open(training_filename, "r")
    training_data = training_file.readlines()

    test_filename = sys.argv[2]
    test_file = open(test_filename, "r")
    test_data = test_file.readlines()

    rare_threshold = int(sys.argv[3])
    feature_threshold = int(sys.argv[4])

    output_directory = sys.argv[5]

    vocabulary_filename = output_directory + "/train_voc"
    init_filename = output_directory + "/init_feats"
    kept_filename = output_directory + "/kept_feats"
    train_filename = output_directory + "/final_train.vectors.txt"
    test_filename = output_directory + "/final_test.vectors.txt"

    tagger = MaxEntTagger(rare_threshold, feature_threshold)
    for line in training_data:
        tagger.count_words(line)
    with open(vocabulary_filename, "a") as train_voc:
        print(tagger.print_counts(), file=train_voc)

    for line_index, line in enumerate(training_data):
        tagger.count_features(line, line_index+1)
    with open(init_filename, "a") as init_feats:
        print(tagger.print_init_features(), file=init_feats)

    with open(kept_filename, "a") as kept_feats:
        print(tagger.print_kept_features(), file=kept_feats)

    with open(train_filename, "a") as train:
        print(tagger.print_features(), file=train)

    tagger.reset_features()
    for line_index, line in enumerate(test_data):
        tagger.count_features(line, line_index+1, True)
    with open(test_filename, "a") as test:
        print(tagger.print_features(), file=test)


if __name__ == "__main__":
    main()
