#!/bin/sh


ec_output_file='../outputs/BECR-TweetEmotionCauseRelation/test_out.txt'
recall_file='recall_file.txt'

precision_file_10='BECR-TweetEmotionCauseRelation/top_10_precision.txt'
output_file_10='BECR-TweetEmotionCauseRelation/10_results'

# evaluate with k=10 for p@k
time /opt/python-3.6/bin/python3.6 evaluate.py ${ec_output_file} ${recall_file} ${precision_file_10} ${output_file_10} 10

precision_file_25='BECR-TweetEmotionCauseRelation/top_25_precision.txt'
output_file_25='BECR-TweetEmotionCauseRelation/25_results'

# evaluate with k=25 for p@k
time /opt/python-3.6/bin/python3.6 evaluate.py ${ec_output_file} ${recall_file} ${precision_file_25} ${output_file_25} 25
