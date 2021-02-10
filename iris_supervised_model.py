# Check the versions of libraries
# Python version

import joblib
import pickle
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix)
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import sys

# import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import scipy
import sklearn
from sklearn import model_selection

print('======================================')
print('Python:      {}'.format(sys.version))
print('scipy:       {}'.format(scipy.__version__))
print('numpy:       {}'.format(np.__version__))
print('matplotlib:  {}'.format(matplotlib.__version__))
print('pandas:      {}'.format(pd.__version__))
print('sklearn:     {}'.format(sklearn.__version__))
print('======================================')


# Load dataset
data = 'sample_data.csv'
column_headers = ['sepal-length', 'sepal-width',
                  'petal-length', 'petal-width', 'class']
df = pd.read_csv(data, names=column_headers)

data = df.values
X = data[:, 0:4]
y = data[:, 4]
validation_size = 0.20
seed = 12345
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(
    X, y, test_size=validation_size, random_state=seed)

# We will use 10-fold cross validation to estimate accuracy.
print('X_train: {}'.format(X_train.shape))
print('X_validation: {}'.format(X_validation.shape))
print('Y_train: {}'.format(Y_train.shape))
print('Y_validation: {}'.format(Y_validation.shape))
print('======================================')

#import models

scoring = 'accuracy'

# Spot Check Algorithms
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))

results = []
names = []
with open('output.txt', 'w') as f:
	for name, model in models:
		kfold = model_selection.KFold(n_splits=5, random_state=None)
		cv_results = model_selection.cross_val_score(
			model, X_train, Y_train, cv=kfold, scoring=scoring)
		results.append(cv_results)
		names.append(name)
		msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
		f.write(msg)
		f.write('\n')
		print(msg)
