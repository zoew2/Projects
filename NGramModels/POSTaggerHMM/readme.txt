The Trigram HMM class uses the annotated training data as input and creates an HMM for a trigram POS tagger smoothing
using interpolation and the unknown probabilities provided.

To store my HMM I used a multidimentional array. I used a 3d numpy array for the transition counts and a 2d numpy array
for the emission counts. I had to add the possible state EOS_EOS to reliably obtain bigram counts from my 3d array, and
for the case of BOS_BOS, I had to manually consider the bigram count 0 since the bigram was never seen in the input
data, but trigrams beginning with BOS_BOS were observed.

The Viterbi class uses the Viterbi algorithm to find the most probable sequence of states through the given HMM for a
given observation.

For my implementation of the Viterbi algorithm, I used integer-indexed dictionaries along with state and symbol to
index mappings to improve efficiency. I also stored the best path so far as a list in a tuple along with the probability
in a given node in the trellis instead of storing backpointers separately as shown in the pseudocode.


They can be run using the following commands:


cat <input_file> | python trigram_hmm.py <output_file> <lambda_1> <lambda_2> <lambda_3> <unknown_probabilities>

input_file - the tagged input sentences in the form "w1/t1 ... wn/tn"

output_file - the resultant hmm, described as transition and emission probabilities

lambda_1 - the value for lambda 1

lambda_2 - the value for lambda 2

lambda_3 - the value for lambda 3

unknown_probabilities - a file containing unknown probabilities for each tag type



python viterby.py <hmm_file> <input_file> <output_file>

hmm_file - the input HMM

input_file - a file of observations to run through the HMM

output_file - the most probable sequence of states for each observation and the probability for each sequence
