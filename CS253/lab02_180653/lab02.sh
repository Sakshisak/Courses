#!/bin/bash

function help() {
	echo "Give exactly two files as arguments :\n 1st: input file\n 2nd: output file "
	exit
}

if [ $# != 2 ]
then 
	help
fi
#Command for 2.
if [ -f $1 ];
then
    #Command for 3.
    sed -e 's/;/@/g' $1
    #Command for 4.
    awk 'BEGIN{FS=";"}{if($9 ~ /Japan/){print $1}}' $1 > $2
    #Command for 5.
    awk 'BEGIN{FS=";"}FNR>1{if($6 > 4000){print $1":"$6}}' $1 >> $2
    #Command for 6th.
    awk -f _6.awk $1 >> $2
else 
    echo "$1 does not exist"
fi



