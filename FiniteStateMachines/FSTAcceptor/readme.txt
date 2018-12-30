This FST acceptor takes in an FST as described in a text file, and input strings from a file, and determines if the given FST would accept each of the input strings in the file, the output string with the highest probability, and the probability of the output string. The FSTs may be ambiguous.

It can be run using the following command:

python3 fst_acceptor.py <fst_file> <input_file> > <output_file>

fst_file - an FST file in Carmel format (https://github.com/graehl/carmel/blob/master/carmel/carmel-tutorial/carmel-training.pdf)

input_file - each line in the input_file is a string where each character is in double quotes

output_file - each line in the output_file has the format “x => y prob”, where x is the string from the input file, y is the output string if x is accepted by the FST, or *none* if x is not accepted by the FST, and prob is the probability of the path whose yield is x.