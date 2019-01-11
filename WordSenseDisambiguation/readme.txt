This class performs word sense disambiguation based on noun groups using Resnik's method and WordNet-based similarity.

I implemented the lowest common subsumer portion by find the most informative common subsumer, assuming that in all
cases, this would also be the lowest common subsumer. My results sometimes differ from the results in the gold file,
but I think this is mainly due to tie breaking since the built-in res_similarity function often returns the same
results that I find.


It can be run using the following command:


python3 resnik_wsd.py <wsd_test_filename> <judgment_file> <output_filename>

wsd_test_filename - the file that contains the lines of "probe-word, noun group words" pairs

judgment_file - the input file holding human judgments of the pairs of words and their similarity to evaluate against

output_file - the output file with the results
