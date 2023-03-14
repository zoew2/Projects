#!/bin/sh

DATA_DIR=/dropbox/18-19/573/Data/Documents/devtest
ROUGE_DIR='/dropbox/18-19/573/code/ROUGE'
RESULTS_FILE_PATH='../results'

# run lead
#time /opt/python-3.6/bin/python3.6 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml lead
# evaluate lead
#"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$RESULTS_FILE_PATH"/lead_rouge_run.xml &> "$RESULTS_FILE_PATH"/lead_rouge_scores.out

# run mead
#time /opt/python-3.6/bin/python3.6 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml mead
## evaluate mead
#"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$RESULTS_FILE_PATH"/mead_rouge_run.xml &> "$RESULTS_FILE_PATH"/mead_rouge_scores.out

#run melda
time /opt/python-3.6/bin/python3.6 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml melda --first_method first_sentence
# evaluate melda
"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$RESULTS_FILE_PATH"/melda_rouge_run_first.xml &> "$RESULTS_FILE_PATH"/D4_devtest_rouge_scores.out
