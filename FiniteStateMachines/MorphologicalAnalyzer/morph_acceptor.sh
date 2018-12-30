#!/bin/sh

python3 expand_morph_fsm.py "$1" "$2" "$3"

# redirect stderr
exec 2> /dev/null

cat "$4" | sed -E 's/([^[:space:]])/\"\1\" /g' > carmel.in

# save carmel output
carmel -bOE -k 1 carmel.in "$3" | sed 's/^/ => /' | sed 's/0$/*NONE*/' | sed -E 's/\"|(1$)//g' > carmel.out

# merge input file with carmel output
paste "$4" carmel.out > "$5"