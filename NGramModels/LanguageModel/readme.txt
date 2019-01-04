This class builds a ngram language model using maximum likelihood estimation with no smoothing.

It can be run using the following command:

python build_lm.py <ngram_frequencies> <output_file>

ngram_frequencies - A file of ngram frequency counts, with each ngram and frequency on a new line

output_file - A file describing the resultant probability distributions for the language model in a modified ARPA format
