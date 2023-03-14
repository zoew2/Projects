import unittest
from src.helpers.class_preprocessor import Preprocessor


class PreprocessorTests(unittest.TestCase):
    """
    Tests for Preprocessor class
    """

    Preprocessor.load_models()


    def test_sent_preprocessing(self):

        raw_sentence = "He took his small puppy to New York today ."
        expected_tokenized_sen= ['take', 'small', 'puppy', 'New York', 'today']

        tokenized_sen=Preprocessor.sent_preprocessing(raw_sentence)
        self.assertEqual(expected_tokenized_sen, tokenized_sen)

        raw_sentence1 = "In the morning he took his small puppy to New York today ."
        expected_tokenized_sen1 = ['the morning', 'take', 'small', 'puppy', 'New York', 'today']

        tokenized_sen1=Preprocessor.sent_preprocessing(raw_sentence1)
        self.assertEqual(expected_tokenized_sen1, tokenized_sen1)

        raw_sentence2 = "THE WORLD is ending. NEW YORK is ending. That's what HE said."
        expected_tokenized_sen2 = ['WORLD', 'end', 'NEW YORK', 'end', 'say']

        tokenized_sen2=Preprocessor.sent_preprocessing(raw_sentence2)
        self.assertEqual(expected_tokenized_sen2, tokenized_sen2)

        raw_sentence3 = "Washington is New York ."
        expected_tokenized_sen3 = ['Washington', 'New York']

        tokenized_sen3=Preprocessor.sent_preprocessing(raw_sentence3)
        self.assertEqual(expected_tokenized_sen3, tokenized_sen3)

    def test_strip_beginning(self):
        raw_sent1 = "*Friday, Feb. 26, 1999 Iranians Vote in Local Elections TEHRAN, Iran (AP) -- Iranians cast ballots today in the nation’s first election of local officials in 20 years."
        result = Preprocessor.strip_beginning(raw_sent1)
        self.assertEqual(result,
                         "Iranians cast ballots today in the nation’s first election of local officials in 20 years.")

        raw_sent2 = "JAKARTA, November 19 (Xinhua) -- Local people and students in Indonesia’s capital Jakarta held an anti-Soeharto mass demonstration, starting at 14:00 local time on Thursday."
        result = Preprocessor.strip_beginning(raw_sent2)
        self.assertEqual(result,
                         "Local people and students in Indonesia’s capital Jakarta held an anti-Soeharto mass demonstration, starting at 14:00 local time on Thursday.")


if __name__ == '__main__':
    unittest.main()
