This class collects word and feature frequencies and creates feature vectors for training and test data and uses mallet
(http://mallet.cs.umass.edu/) to test a POS tagging classifier using these vectors.


It can be run using the following commands:


./maxent_tagger.sh <train_̠file> <test_file> <rare_threshold> <feature_threshold> <output_directory> >&2

train_̠file - file in the format "w1/t1 ... wn/tn"

test_file - file in the format "w1/t1 ... wn/tn"

rare_threshold - threshold value for rare words

feature_threshold - threshold value for rare features

output_directory - the directory to write output files to
