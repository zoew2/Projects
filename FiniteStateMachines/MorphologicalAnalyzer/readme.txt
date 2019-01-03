This FST acceptor takes in an FSM as described in a text file describing morphological rules, a lexicon of labeled morphemes, and exapands the FSM using the lexicon given. It then takes a list of words and outputs each word with morpheme labels if the given word can be parsed using the given morphological rules and lexicon.

It can be run using the following command:

./morph_acceptor.sh <lexicon> <morph_rules> <fsm_file> <word_list> <output_file>

lexicon - A file where each line is a morpheme followed by a label

morph_rules - an FSM file in Carmel format (https://github.com/graehl/carmel/blob/master/carmel/carmel-tutorial/carmel-training.pdf) describing a set of morphological rules for the labels in the given lexicon

fsm_file - the output file to write the expanded FST file to in Carmel format (https://github.com/graehl/carmel/blob/master/carmel/carmel-tutorial/carmel-training.pdf)

word_list - A list of words to label, with each word on a new line

output_file - The output file where the format is “word => morph1/label1 morph2/label2 ...” if the word is accepted or "*NONE*" otherwise
