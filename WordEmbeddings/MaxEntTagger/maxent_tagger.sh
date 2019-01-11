#!/bin/sh

python3 maxent_tagger.py "$@"

mallet import-file --token-regex "[^\s]+" --preserve-case --input "$5"/final_train.vectors.txt --output "$5"/final_train.vectors
mallet import-file --token-regex "[^\s]+" --preserve-case --input "$5"/final_test.vectors.txt --output "$5"/final_test.vectors --use-pipe-from "$5"/final_train.vectors
vectors2classify -Xmx3g --training-file "$5"/final_train.vectors --testing-file "$5"/final_test.vectors --trainer MaxEnt --output-classifier "$5"/me_model > "$5"/me_model.stdout 2> "$5"/me_model.stderr

mallet classify-file --input "$5"/final_test.vectors.txt --classifier "$5"/me_model --output "$5"/sys_out

cat "$5"/me_model.stdout | grep "train accuracy"
cat "$5"/me_model.stdout | grep "test accuracy"
wc -l "$5"/init_feats
wc -l "$5"/kept_feats