This class uses either Euclidean distance or Cosine similarity measures to solve the word analogy task.

Ex:
boy is to girl as brother is to ?


It can be run using the following commands:


./word_analogy.sh <vector_file> <input_directory> <output_directory> <flag1> <flag2>

vector_file - an input file with the format “w v1 v2 ... vn”, where <v1, v2, ..., vn > is word embedding of the word w

input_directory - a directory that contains a list of test files. The lines in the test file have the format “A B C D”,
the four words as in the word analogy task

output_directory - a directory to store the output

flag1 - an interger indicating whether the word embeddings should be normalized first

flag2 - an integer indicating which similarity function to use for calculating sim(x,y) (0 - Euclidean, else - Cosine)
