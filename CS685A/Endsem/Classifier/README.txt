Answer 2: Classifier

The directory structure is as follows:
.
├── answer-s050.csv
├── compare_models.py
├── comparison.txt
├── makefile
├── README.txt
├── classifier-s050.sh
├── SVC_train.py
└── training-s050.csv

As asked in the assignment: the main files are:
.
├── makefile
├── README.txt
└── classifier-s050.sh

Makefile: makefile has two options:
    - make run <test_input.csv> : calls the shell script classifier-s050.sh with the command line argument of test_file name as input
    - make clean : removes the answer file (answer-s050.csv)

Shell Script:
    classifier-s050.sh is the shell script. It can run by the following command:
        $ chmod +x classifier-s050.sh
        $ ./classifier-s050.sh <test_file> 
    
    classifier-s050.sh internally makes call the SVC_train.py file with command line argument as name of test_file

    It generates the output file containing 100 rows of classes:
    .
    └── answer-s050.csv


####################### HOW TO RUN ######################

For running these files the following are the dependencies
    - sklearn
    - numpy
    - pandas
    - matplotlib

Using makefile:

1. $ make clean
2. $ make run <test_file>

==> Generates answer-s050.csv

Using shell script

1. chmod +x classifier-s050.sh
2. ./classifier-s050.sh <test_file>

==> Generates answer-s050.csv


###################### ADDITIONAL FILES ######################

There are two additional files:
    .
    ├── compare_models.py
    └── comparison.txt

compare_models.py is a python file running SVC and Multiclass Logistic Regression Models with different parameters.
It generates the file comparison.txt which contains the summary of the comparative analysis.
Based on the result I chose the SVC training model as the two didn't differ much in accuracy.



