from sklearn import linear_model
from sklearn import model_selection
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import make_pipeline
import pandas as pd
import numpy as np


datafile = 'training-s050.csv'
data_df = pd.read_csv(datafile, header=None)

file_comparison = 'comparison.txt'
f_save = open(file_comparison, 'w')
f_save.write('================================================================\n----------------------------Accuracy----------------------------\n================================================================\n\n')

f_save.write('------------------Multiclass Logistic Regression----------------\n\n')
X = data_df.iloc[:, 1:]
y = data_df.iloc[:, 0]

# Use StandardScaler - Gaussian Distribution [-1,1]
for test_s in {0.1, 0.15, 0.2, 0.25, 0.3}:
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X.to_numpy(), y.to_numpy(), test_size= test_s, random_state = 1)
    lm = make_pipeline(StandardScaler(), linear_model.LogisticRegression(penalty='l2',multi_class="multinomial"))
    
    lm.fit(X_train, y_train)
    accuracy = lm.score(X_test, y_test)
    scale = 'Gaussian'
    f_save.write('Scaling: {0:8} Test Size: {1:2}% ==> {2:.6f}%\n'.format(scale, test_s*100, accuracy*100))

f_save.write('\n')

# Use MinMaxScaler - Normal Distribution [0,1]
for test_s in {0.1, 0.15, 0.2, 0.25, 0.3}:
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X.to_numpy(), y.to_numpy(), test_size= test_s, random_state = 1)
    lm = make_pipeline(MinMaxScaler(), linear_model.LogisticRegression(penalty='l2',multi_class="multinomial"))
    
    lm.fit(X_train, y_train)
    accuracy = lm.score(X_test, y_test)
    scale = 'Normal'
    f_save.write('Scaling: {0:8} Test Size: {1:2}% ==> {2:.6f}%\n'.format(scale, test_s*100, accuracy*100))

f_save.write('\n-------------------Support Vector Classifier--------------------\n\n')

for test_s in {0.1, 0.15, 0.2, 0.25, 0.3}:
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X.to_numpy(), y.to_numpy(), test_size= test_s, random_state = 1)
    clf = SVC()
    
    clf.fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)
    f_save.write('Test Size: {0:2}% ==> {1:.6f}%\n'.format(test_s*100, accuracy*100))

f_save.write('\n')
f_save.write('================================================================\n')


f_save.close()