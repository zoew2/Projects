"""
Class Sentence that takes raw sentence from Document class as input
and returns information about sentence including tokenized sentence,
word count for sentence, whether sentence is first or initial sentence of
document and position/order of sentence within document as integer
"""

import string
from src.helpers.class_wordmap import WordMap
from src.helpers.class_preprocessor import Preprocessor

class Sentence:

    def __init__(self, raw_sentence, sent_pos, doc_id=None):
        """
        initialize Sentence class with methods for plain/raw and tokenized sentence
        options, word count, position of sentence in document and document id
        :param raw_sentence:
        :param sent_pos:
        """
        self.raw_sentence = ' '.join(raw_sentence.rstrip().split())
        self.raw_sentence = Preprocessor.strip_beginning(self.raw_sentence)
        self.tokens = []

        self.processed = Preprocessor.get_processed_sentence(self.raw_sentence)
        self.__tokenize_sentence(self.raw_sentence)

        self.sent_pos = int(sent_pos)  # position of sentence in document
        self.doc_id = doc_id
        self.vector = []  # placeholder
        self.order_by = self.sent_pos
        self.c_score = self.p_score = self.f_score = self.mead_score = self.lda_scores = self.melda_scores = None
        self.compressed = self.raw_sentence

        # update global mapping of words to indices
        WordMap.add_words(self.tokens)  # make sure self.tokens is the right thing here

    def is_first_sentence(self):
        """
        grab headline and content(text) of the document
        :return: Boolean
        """
        if self.sent_pos == 0:
            return True
        else:
            return False

    def position(self):
        """
        returns position of sentence in document as a number
        :return: integer
        """
        return self.sent_pos

    def tokenized(self):
        """
        returns words in sentence excluding punctuation
        :return: list of words in sentence
        """
        return self.tokens

    def word_count(self):
        """
        count number of words in sentence excluding punctuation
        :return: integer
        """
        ct = 0
        for w in self.compressed.split(" "):
            if w not in string.punctuation:
                ct += 1
        return ct

    def document_id(self):
        """
        return document id associated with sentence
        :return: String of document id or None if not provided
        """
        return self.doc_id

    def set_mead_score(self, score):
        """
        assign sentence score
        :return: float
        """
        self.mead_score = score
        self.order_by = self.mead_score

    def get_score(self):
        """
        return sentence score
        :return: float
        """
        return self.mead_score

    def __tokenize_sentence(self, processed):
        """
        tokenize sentence and remove sentence-level punctuation,
        such as comma (,) but not dash (-) in, e.g. 'morning-after'
        function only for internal usage
        """
        self.tokens = Preprocessor.get_processed_tokens(processed)

    def set_vector(self, vector):
        """
        assign a vector representing the sentence to self.vector
        :param vector: one-dimensional scipy sparse matrix
        :return:
        """
        self.vector = vector

    def __str__(self):
        """
        print sentence as readable string
        """
        return self.raw_sentence

    def __eq__(self, other):
        """
        One Sentence is equal to another if the raw sentences match
        :param other:
        :return:
        """
        return isinstance(other, Sentence) and self.raw_sentence == other.raw_sentence


    def __lt__(self, other):
        """
        Sentences are ordered by their sentence positions by default
        if a Sentence has a mead score, that is used
        :param other:
        :return:
        """
        return self.order_by < other.order_by
