from sklearn import model_selection
from sklearn.svm import SVC
import pandas as pd
import numpy as np
import sys


train_file = 'training-s050.csv' 
n_args = len(sys.argv)
# print(sys.argv)
test_file = sys.argv[1] if n_args>1 else 'testing-s050.csv'

data_df = pd.read_csv(train_file, header=None)
test_data_df = pd.read_csv(test_file,header=None)
test_data_df = test_data_df.iloc[:, 1:]

X = data_df.iloc[:, 1:]
y = data_df.iloc[:, 0]

# test size chosen on the basis of comparative analysis done before
X_train, X_test, y_train, y_test = model_selection.train_test_split(X.to_numpy(), y.to_numpy(), test_size= 0.15, random_state = 1)
clf = SVC()

clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)
print("Accuray on train-test partition: ",accuracy*100)

result = list(clf.predict(test_data_df.to_numpy()))

f_save = 'answer-s050.csv'
f_save = open(f_save,'w')

for x in result:
    f_save.write(x+'\n')

f_save.close()

