#!/bin/bash -v

# print the day if the week in a numeric form
# Monday is 1, Tuesday is 2, ..., Sunday is 7

function help() {
	echo "Usage: $0 weekday"
	echo "   weekday is one of Monday, Tuesday, ..., Sunday"
}

echo "Which day?[quit to quit] : "
read d
d=$(echo $d | tr A-Z a-z)

while [ $d != "quit" ]
do
	case $d in
		monday)     echo 1;;
		tuesday)    echo 2;;
		wednesday)  echo 3;;
		thursday)   echo 4;;
		friday)     echo 5;;
		saturday)   echo 6;;
		sunday)     echo 7;;
		*)          echo "Bad Day in Input"
			    help	;;
	esac
	echo "Which day?[quit to quit] : "
	read d
	d=$(echo $d | tr A-Z a-z)
done
