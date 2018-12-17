This FSA acceptor takes in an FSA as described in a text file, and input strings from a file, and determines if the given FSA would accept each of the input strings in the file. The FSAs can be NFAs or DFAs, I chose to have my code maintain multiple possible paths instead of converting the NFAs to DFAs for the acceptor.

It can be run using the following command:

python3 fsa_acceptor.py <fsa_file> <input_file> > <output_file>

fsa_file - an FSA file in Carmel format (https://github.com/graehl/carmel/blob/master/carmel/carmel-tutorial/carmel-training.pdf)

input_file - each line in the input_file is a string where each character is in double quotes

output_file - each line in the output_file has the format “x => y”, where x is the string from the input file, and y is “yes” is x is accepted by the FSA, and “no” otherwise