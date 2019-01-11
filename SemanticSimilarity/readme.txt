This class computes semantic similarity using 3 different strategies. If the "CBOW" flag is passed, a predictive CBOW
distributional model of word similarity is built using Word2Vec. Otherwise, a distributional model of word similarity
ased on local context term cooccurence is built weighted by either term frequency ("FREQ") or (positive) point-wise
mutual information ("PMI"), a variant of PMI where negative association scores are removed.

I chose to use
brown.words instead of brown.sents. This means that sentence boundaries are not being considered as meaningful as if I
had chosen to use sentences since punctuation is also removed, so a word in a different sentence is still considered
as context for a given word.

The frequency model with a window of 2 provided pretty small correlation results. Although punctuation was removed, stop
words were not, so many words that were considered in context were words that provided little meaningful information
about a word such as "the" and "a"

The PMI model with a window of 2 had a slightly higher correlation, because that algorithm does a better job of normalizing
values by considering total word count and individual word contexts in computing a similarity score.

Increasing the window size for the PMI value actually dropped the correlation, because by increasing the window-size, we
are also increasing the probability that there will be overlap in the context between any given two words, even if they
are unrelated.

CBOW has the highest correlation score because the bag of words approach uses the limited information available in a much
more meaningful way and allows us to consider context in a way that gives more insight.


It can be run using the following command:


python3 sem_sim.py <window> <weighting> <judgment_file> <output_file>

window - the size of the context window

weighting - a string specifying the weighting scheme to apply: "FREQ" or "PMI" or "CBOW"

judgment_file - the input file holding human judgments of the pairs of words and their similarity to evaluate against

output_file - the output file with the results of computing similarities and correlations over the word pairs
