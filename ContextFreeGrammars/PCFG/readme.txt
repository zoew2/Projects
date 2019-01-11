This class induces a probabilistic context free grammar from a treebank

I used the NLTK Tree fromstring() function for each line in the training data, and then entered counts in a dictionary
for each tree with a unique left and right hand side. I then looped through the dictionary and transformed the counts
into probabilities by dividing by the length of the list of right-hand sides for each left-hand side


It can be run using the following command:


python3 pcfg.py <treebank_filename> <output_file>

treebank_filename -  the parsed sentences, one parse per line, in Chomsky Normal Form

output_file - the output filename
