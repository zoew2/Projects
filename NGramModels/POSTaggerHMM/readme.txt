This class the annotated training data as input and creates an HMM for a trigram POS tagger smoothing using
interpolation and the unknown probabilities provided.

To store my HMM I used a multidimentional array. I used a 3d numpy array for the transition counts and a 2d numpy array
for the emission counts. I had to add the possible state EOS_EOS to reliably obtain bigram counts from my 3d array, and
for the case of BOS_BOS, I had to manually consider the bigram count 0 since the bigram was never seen in the input
data, but trigrams beginning with BOS_BOS were observed.

It can be run using the following command:

cat <input_file> | python trigram_hmm.py <output_file> <lambda_1> <lambda_2> <lambda_3> <unknown_probabilities>

input_file - the tagged input sentences in the form "w1/t1 ... wn/tn"

output_file - the resultant hmm, described as transition and emission probabilities

lambda_1 - the value for lambda 1

lambda_2 - the value for lambda 2

lambda_3 - the value for lambda 3

unknown_probabilities - a file containing unknown probabilities for each tag type
