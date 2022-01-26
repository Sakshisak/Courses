Answer 1: Anomaly Detection

The directory structure is as follows:
.
├── anomaly.py
├── anomaly-s050.dat
├── anomaly-s050.sh
├── answer-s050.dat
├── comparison.ipynb
├── makefile
└── README.txt

As asked in the assignment: the main files are:
.
├── makefile
├── README.txt
└── anomaly-s050.sh

Makefile: makefile has two options:
    - make run : calls the shell script anomaly-s050.sh
    - make clean : removes the answer file (answer-s050.dat)

Shell Script:
    anomaly-s050.sh is the shell script. It can run by the following command:
        $ chmod +x anomaly-s050.sh
        $ ./anomaly-s050.sh 
    
    anomaly-s050.sh internally makes call the anomaly.py 

    It generates the output file containing 100*100 data points showing whether that data was an outlier or not. Each row contains 100 space separated data points:
    .
    └── answer-s050.dat


####################### HOW TO RUN ######################

For running these files the following are the dependencies
sklearn
numpy
pandas
matplotlib

Using makefile:

1. $ make clean
2. $ make run

==> Generates answer-s050.dat

Using shell script

1. chmod +x anomaly-s050.sh
2. ./anomaly-s050.sh

==> Generates answer-s050.dat


###################### ADDITIONAL FILES ######################

There is an additional files:
    .
    ├── comparison.ipynb

comparison.ipynb is a python notebook running various outlier detection methods like Histogram, BoxPlot, Statistical method using mean and standard deviation, Tukey's method and Z-score method.
Based on the result I chose the Z-score model to find the outliers



