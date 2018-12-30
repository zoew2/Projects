This converter converts an input NFA to an equivalent DFA. Due to the limitations of the Carmel format, if the resulting DFA has more than one final state, a new final state called FinalState will be added with arcs that go from each of these DFA final states to FinalState with with the empty string as the label. So in that sense, the output_dfa_file is not a real DFA.

It can be run using the following command:

python3 nfa_to_dfa.py <input_nfa_file> > <output_dfa_file>

input_nfa_file - an FSA (NFA) file in Carmel format (https://github.com/graehl/carmel/blob/master/carmel/carmel-tutorial/carmel-training.pdf)

output_dfa_file - an FSA (DFA) file in Carmel format (https://github.com/graehl/carmel/blob/master/carmel/carmel-tutorial/carmel-training.pdf)
