This class uses the given language models to create a language classifier to determine the most probable language for a
given sentence and provide the probability that lead to that judgement.

For this project, I first stored the data from the language models into a dictionary, storing the unigram probabilities
and total word counts of each language sample. Then, for each line in the test data, I sum the log probabilities of
each word for each language to determine the log probability of each language for the given line. I chose to use
Laplace or additive smoothing to account for data points in the test set that were not in the training set.

I also determined that an appropriate threshold to predict a language from the training set over an unknown one would
be that the probability of the most likely language is more than one standard deviation away from the mean of all the
probabilities predicted for lanugages in the dataset, and the difference between the most probable language and the
second most probable language is significant (I used more than 10 after examining the training dataset). This threshold
criteria did not result in 100% accuracy on the training dataset - it identified Iloko as Tagalog and Welsh as Gaelic.
However since the correct languages were not in the original training data (the language models) and both pairs of
languages are closely related, these predictions seem more than reasonable.

It can be run using the following command:

python PredictLanguages.py <language_models> <test_sentences>

language_models - a directory containing language models

test_sentences - a file containing sentences in various languages
