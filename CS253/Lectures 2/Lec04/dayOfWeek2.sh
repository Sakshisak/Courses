#!/bin/bash

# print the day if the week in a numeric form
# Monday is 1, Tuesday is 2, ..., Sunday is 7

function help() {
	echo "Usage: $0 weekday"
	echo "   weekday is one of Monday, Tuesday, ..., Sunday"
	exit
}

if [ $# != 1 ]
then
	help
fi

d=$1

case $d in
	Monday)     echo 1;;
	Tuesday)    echo 2;;
	Wednesday)  echo 3;;
	Thursday)   echo 4;;
	Friday)     echo 5;;
	Saturday)   echo 6;;
	Sunday)     echo 7;;
        *)          echo "Bad Day in Input"
	            help	;;
esac

