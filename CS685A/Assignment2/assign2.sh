#!/bin/bash

cd python_scripts

for i in {1..9}
do  
    if [ 4==$i ]
    then
        python3 q4a.py
        python3 q4b.py
    else  
        python3 q$i.py
    fi
done
