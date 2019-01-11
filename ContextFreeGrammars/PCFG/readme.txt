The PCFG class induces a probabilistic context free grammar from a treebank

I used the NLTK Tree fromstring() function for each line in the training data, and then entered counts in a dictionary
for each tree with a unique left and right hand side. I then looped through the dictionary and transformed the counts
into probabilities by dividing by the length of the list of right-hand sides for each left-hand side

The parent annotated PCFG class is an improvement on this baseline induction.

Improvements
- I tried two different approaches to improve my algorithm. First I tried to improve coverage by choosing the most likely
POS tag for any word not seen in my training data. I did this by including a string "UNK" with a count of 1 for each
preterminal seen in the training data, in increasing the count for every terminal by 1, similar to Laplace smoothing.
Then, any time the algorithm saw a previously unseen word, instead of being unable to continue, it would consider every
possible preterminal and a decision would be made higher up about which POS tag resulted in the most probable parse.

> This approach increased the number of valid parses to 54/55, but reduced the recall/precision/fmeasure to 87.46 with 98.23
tagging accuracy. I think this is because more sentences were able to be successfully parsed, but since we're guessing
about a POS, they're less likely to be accurate.

- I also tried to improve accuracy by implementing parent annotation. I did this by concatenating the parent node, after
a "^" symbol, to each nonterminal, and stripping off the suffix before printing.

> This approach reduced the number of valid parses to 38/55, but the recall/precision/fmeasure only fell to 95.44 with
99.05 tagging accuracy. I think this is because the induced PCFG is somewhat overfit to the training data, so the parses
that are found are very accurate, but novel parses are unable to be parsed at all.

> Together, these two approaches lead to a recall/precision/fmeasure of 95.20 with 98.79 tagging accuracy on 40/55
sentences.


They can be run using the following commands:


python3 pcfg.py <treebank_filename> <output_file>

treebank_filename -  the parsed sentences, one parse per line, in Chomsky Normal Form

output_file - the output filename


python3 parent_annotated_pcfg.py <treebank_filename> <output_file>

treebank_filename -  the parsed sentences, one parse per line, in Chomsky Normal Form

output_file - the output filename
