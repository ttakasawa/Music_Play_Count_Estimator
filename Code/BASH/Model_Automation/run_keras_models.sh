#!/bin/bash
for i in `seq $2 $3`;
do
    python3 keras_model.py $1 $i
done
