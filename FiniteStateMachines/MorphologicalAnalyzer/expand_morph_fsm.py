from string import whitespace
import sys
from unittest import TestCase


class ExpandMorphFSM:
    """
    This class expands a given FSM of morphosyntactic rules using the given lexicon
    """

    def __init__(self, lexicon, morph_rules):
        """
        Initialize the class by loading the lexicon
        :param lexicon: the given lexicon
        """
        self.lexicon = self.load_lexicon(lexicon)
        self.fsm = self.load_fsm(morph_rules)
        self.expanded = {'start_state': '', 'final_state': '', 'transitions': {}}
        self.state_count = 0
        self.label_count = 0

    @staticmethod
    def load_lexicon(lexicon):
        """
        Load the given lexicon into a dictionary
        :param lexicon: the given lexicon
        :return: dictionary representation of the lexicon
        """
        labels = {}

        for line in lexicon:
            if not line.strip():
                continue
            word_label = line.split()
            labels.setdefault(word_label[1], []).append(word_label[0])

        return labels

    @staticmethod
    def load_fsm(morph_rules):
        fsm = {'start_state': '', 'final_state': '', 'transitions': {}}

        for line in morph_rules:
            rule = list(filter(None, line.split()))

            if len(rule) < 1 or rule[0].strip(whitespace) == '':
                continue
            if "(" not in rule[0]:
                # if this is not a transition, it's the final state
                fsm['final_state'] = rule[0]
            else:
                # get the values for the transition
                first_state = rule[0].strip(whitespace + '"\'()')
                second_state = rule[1].strip(whitespace + '"\'()')
                input_string = rule[2].strip(whitespace + '"\'()')

                if "*e*" in input_string:
                    input_string = ''
                if fsm['start_state'] == '':
                    fsm['start_state'] = first_state
                if first_state not in fsm['transitions'].keys():
                    fsm['transitions'][first_state] = {}

                fsm['transitions'][first_state].setdefault(input_string, []).append(second_state)

        return fsm

    def expand_morph_fsm(self):
        """
        Expand this FSM given the lexicon
        :return: void
        """
        state_map = {}
        for first_state in self.fsm['transitions']:
            first_state_name = state_map.setdefault(first_state, self.get_next_state_name(True))
            if not self.expanded['start_state'] and first_state == self.fsm['start_state']:
                self.expanded['start_state'] = first_state_name
            for label in self.fsm['transitions'][first_state]:
                for second_state in self.fsm['transitions'][first_state][label]:
                    second_state_name = state_map.setdefault(second_state, self.get_next_state_name(True))
                    if not self.expanded['final_state'] and second_state == self.fsm['final_state']:
                        self.expanded['final_state'] = second_state_name
                    self.expand_arc(first_state_name, second_state_name, label)

    def expand_arc(self, first_state, second_state, label):
        """
        Expand this arc from the FSM
        :param first_state: the origin state
        :param second_state: the destination state
        :param label: the label of the arc
        :return: void
        """
        if not label:
            self.add_arc(first_state, second_state, label, '')
            return
        for word in self.lexicon[label]:
            if len(word) is 1:
                self.add_arc(first_state, second_state, word[0], word + "/" + label + " ")
                return
            second_state_name = self.get_next_state_name(False)
            second_state_name = self.add_arc(first_state, second_state_name, word[0], '')
            for index in range(1, len(word)-1):
                first_state_name = second_state_name
                second_state_name = self.get_next_state_name(False)
                second_state_name = self.add_arc(first_state_name, second_state_name, word[index], '')
            self.add_arc(second_state_name, second_state, word[-1], word + "/" + label + " ")

    def add_arc(self, first_state, second_state, character, output):
        """
        Add an arc to the expanded FSM
        :param first_state: the origin state of the arc
        :param second_state: the destination state of the arc
        :param character: the input character for the arc
        :param output: the output character for the arc
        :return: the name of the destination state
        """
        self.expanded['transitions'].setdefault(first_state, {}).setdefault(character, '')
        # only add the arc it it doesn't already exist
        if not self.expanded['transitions'][first_state][character]:
            self.expanded['transitions'][first_state][character] = (second_state, output)

        # if it exists but ends at a final state, insert a new state and an epsilon transition to the final state
        elif self.expanded['transitions'][first_state][character][0] in self.expanded['final_state']:
            old_value = self.expanded['transitions'][first_state][character]
            self.expanded['transitions'][first_state][character] = (second_state, output)

            self.expanded['transitions'].setdefault(second_state, {}).setdefault('', '')
            self.expanded['transitions'][second_state][''] = old_value

        return self.expanded['transitions'][first_state][character][0]

    def print_in_carmel_format(self):
        """
        Print the FSM in carmel format
        :return: a string representation of the FSM in carmel format
        """
        output_string = ""
        output_string += self.expanded['final_state'] + "\n"
        start_state = self.expanded['start_state']

        for character in self.expanded['transitions'][start_state]:
            second_state = self.expanded['transitions'][start_state][character][0]
            output = self.expanded['transitions'][start_state][character][1]
            input_char = " \"" + character + "\"" if character else " *e*"
            output_char = " \"" + output.strip() + "\"" if output.strip() else " *e*"
            output_string += "(" + start_state + " (" + second_state + input_char + output_char + "))\n"

        for first_state in self.expanded['transitions']:
            if first_state != start_state:
                for character in self.expanded['transitions'][first_state]:
                    second_state = self.expanded['transitions'][first_state][character][0]
                    output = self.expanded['transitions'][first_state][character][1]
                    input_char = " \"" + character + "\"" if character else " *e*"
                    output_char = " \"" + output.strip() + "\"" if output.strip() else " *e*"
                    output_string += "(" + first_state + " (" + second_state + input_char + output_char + "))\n"
        return output_string.strip()

    def get_next_state_name(self, is_label):
        """
        Generate the next state name
        :param is_label: is this a label state?
        :return: string label name

        """
        if is_label:
            self.label_count += 1
            return "label_" + str(self.label_count)
        else:
            self.state_count += 1
            return "q" + str(self.state_count)


class TestExpandFSM(TestCase):
    """
    This class contains tests for the ExpandMorphFSM class
    """

    maxDiff = None

    test_lexicon = '''
        walk       reg_verb_stem
        talk       reg_verb_stem
        impeach    reg_verb_stem
        
        cut        irreg_verb_stem
        speak      irreg_verb_stem
        sing       irreg_verb_stem
        
        caught     irreg_past_verb_form
        ate        irreg_past_verb_form
        sang       irreg_past_verb_form
        spoke      irreg_past_verb_form
        
        eaten      irreg_past_verb_form
        sung       irreg_past_verb_form
        spoken     irreg_past_verb_form
        
        ed         past
        ed         past_participle
        ing        pres_part
        s          3sg
    '''

    test_morph_rules = '''
        q3
        (q0 (q3 irreg_past_verb_form))
        (q0 (q1 reg_verb_stem))
        (q1 (q3 past))
        (q1 (q3 past_participle))
        (q0 (q2 reg_verb_stem))
        (q0 (q2 irreg_verb_stem))
        (q2 (q3 pres_part))
        (q2 (q3 3sg))
        (q1 (q3 *e*))
        (q2 (q3 *e*))
        '''

    test_expected_output = '''
        label_2
        (label_1 (q1 "c" *e*))
        (label_1 (q6 "a" *e*))
        (label_1 (q8 "s" *e*))
        (label_1 (q15 "e" *e*))
        (label_1 (q27 "w" *e*))
        (label_1 (q30 "t" *e*))
        (label_1 (q33 "i" *e*))
        (q1 (q2 "a" *e*))
        (q1 (q52 "u" *e*))
        (q2 (q3 "u" *e*))
        (q3 (q4 "g" *e*))
        (q4 (q5 "h" *e*))
        (q5 (label_2 "t" "caught/irreg_past_verb_form"))
        (q6 (q7 "t" *e*))
        (q7 (label_2 "e" "ate/irreg_past_verb_form"))
        (q8 (q9 "a" *e*))
        (q8 (q12 "p" *e*))
        (q8 (q20 "u" *e*))
        (q8 (q58 "i" *e*))
        (q9 (q10 "n" *e*))
        (q10 (label_2 "g" "sang/irreg_past_verb_form"))
        (q12 (q13 "o" *e*))
        (q12 (q55 "e" *e*))
        (q13 (q14 "k" *e*))
        (q14 (q26 "e" *e*))
        (q15 (q16 "a" *e*))
        (q16 (q17 "t" *e*))
        (q17 (q18 "e" *e*))
        (q18 (label_2 "n" "eaten/irreg_past_verb_form"))
        (q20 (q21 "n" *e*))
        (q21 (label_2 "g" "sung/irreg_past_verb_form"))
        (q26 (label_2 *e* "spoke/irreg_past_verb_form"))
        (q26 (label_2 "n" "spoken/irreg_past_verb_form"))
        (q27 (q28 "a" *e*))
        (q28 (q29 "l" *e*))
        (q29 (label_3 "k" "walk/reg_verb_stem"))
        (q30 (q31 "a" *e*))
        (q31 (q32 "l" *e*))
        (q32 (label_3 "k" "talk/reg_verb_stem"))
        (q33 (q34 "m" *e*))
        (q34 (q35 "p" *e*))
        (q35 (q36 "e" *e*))
        (q36 (q37 "a" *e*))
        (q37 (q38 "c" *e*))
        (q38 (label_3 "h" "impeach/reg_verb_stem"))
        (q52 (label_4 "t" "cut/irreg_verb_stem"))
        (q55 (q56 "a" *e*))
        (q56 (label_4 "k" "speak/irreg_verb_stem"))
        (q58 (q59 "n" *e*))
        (q59 (label_4 "g" "sing/irreg_verb_stem"))
        (label_3 (q60 "e" *e*))
        (label_3 (label_2 *e* *e*))
        (q60 (label_2 "d" "ed/past_participle"))
        (label_2 (label_2 *e* "ed/past"))
        (label_4 (q62 "i" *e*))
        (label_4 (label_2 "s" "s/3sg"))
        (label_4 (label_2 *e* *e*))
        (q62 (q63 "n" *e*))
        (q63 (label_2 "g" "ing/pres_part"))
    '''

    def test_expand_fsm(self):
        """
        Tests for expand_fsm
        :return: void
        """

        expander = ExpandMorphFSM(self.test_lexicon.split("\n"), self.test_morph_rules.split("\n"))
        expander.expand_morph_fsm()
        output_list = expander.print_in_carmel_format().split("\n")

        expected_list = self.test_expected_output.strip().split("\n")
        self.assertEqual(len(expected_list), len(output_list))


def main():
    """
    Parse the system arguments, call the ExpandFSM class and write results to the output file
    :return:
    """
    lexicon_filename = sys.argv[1]
    morph_rules_filename = sys.argv[2]
    output_filename = sys.argv[3]

    lexicon_file = open(lexicon_filename, "r")
    lexicon = lexicon_file.readlines()

    morph_rules_file = open(morph_rules_filename, "r")
    morph_rules = morph_rules_file.readlines()

    with open(output_filename, "w") as output_file:
        expander = ExpandMorphFSM(lexicon, morph_rules)
        expander.expand_morph_fsm()
        print(expander.print_in_carmel_format(), file=output_file)


if __name__ == "__main__":
    main()
