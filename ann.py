
#Part 1 - Data Preprocessing

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder,StandardScaler
from sklearn.model_selection import train_test_split
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from sklearn.metrics import confusion_matrix
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV

# Importing the dataset
dataset = pd.read_csv('Churn_Modelling.csv')
X = dataset.iloc[:, 3:13].values
y = dataset.iloc[:, 13].values

# Encoding categorical data

labelencoder_X_Country = LabelEncoder()
X[:, 1] = labelencoder_X_Country.fit_transform(X[:, 1])
labelencoder_X_Gender = LabelEncoder()
X[:, 2] = labelencoder_X_Gender.fit_transform(X[:, 2])

onehotencoder = OneHotEncoder(categorical_features = [1])
X = onehotencoder.fit_transform(X).toarray()
X = X[:, 1:]


# Splitting the dataset into the Training set and Test set

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)


#Scalling of training data and testing
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Intializing ANN
classifier = Sequential()

#Adding input layer and first hidden layer
#input_dim layer is required in first layer as no layer is created which denotes number of independent variables
#kernel_initializer is used to give initial weights
#activate function is relu which is rectifier function
# units denotes number of noded in hidden layer by standard we can take it as average of number of nodes in input layer and output layer
classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu', input_dim=11))

#Adding Second Layer
classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu'))

#Output Layer
#Since we have only one output node we need to change units to 1
#We will keep kernel_intializer to uniform
#For output Layer we will change activation function from rectifier to signmoid function
# If we have dependent variable which has more than 2 classes then we need to make  activation function to softmax function and
# change units to number of classes
classifier.add(Dense(units=1, kernel_initializer='uniform', activation='sigmoid'))


#Compiling ANN
#Optimizer parameter is algorithm we want to use to optimize weights , adam is a form of stochastic gradient function
#loss is loss function in stochastic gradient function which we have to optimize.



classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

#Fitting ANN into Training Set
classifier.fit(X_train, y_train, batch_size=10, epochs=100)


#Making Prediction
y_pred = classifier.predict(X_test)

# If probability is less than 0.5 then mark it as false and if it is more than 0.5 mark it as Tru
y_pred=(y_pred > 0.5)
cm = confusion_matrix(y_test, y_pred)

new_prediction = classifier.predict(sc.transform(np.array([[0, 0, 600, 1, 40, 3, 60000, 2, 1, 1, 50000]])))
new_prediction = (new_prediction > 0.5)
print(new_prediction)

#Evaluating improving and tunning of ANN

#Evaluating ANN

def build_classifier():
    classifier = Sequential()
    classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu', input_dim=11))
    #Adding dropout to first layer improve performance of ANN. range is from 0 to 1 where fraction denotes number of neurons that will be
    #disabled in layer in each iteration.
    classifier.add(Dropout(rate=0.1))
    classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu'))
    classifier.add(Dense(units=1, kernel_initializer='uniform', activation='sigmoid'))
    classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return classifier

classifier = KerasClassifier(build_fn = build_classifier, batch_size = 10, epochs = 100)
accuracies = cross_val_score(estimator = classifier, X=X_train, y=y_train, cv=10, n_jobs=1)
mean = accuracies.mean()
variance = accuracies.std()


#Tunning ANN
#Parameter Tuning with Grid Search

def build_classifier(optimizer):
    classifier = Sequential()
    classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu', input_dim=11))
    #Adding dropout to first layer improve performance of ANN. range is from 0 to 1 where fraction denotes number of neurons that will be
    #disabled in layer in each iteration.
    classifier.add(Dropout(rate=0.1))
    classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu'))
    classifier.add(Dense(units=1, kernel_initializer='uniform', activation='sigmoid'))
    classifier.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
    return classifier


classifier = KerasClassifier(build_fn=build_classifier)
parameters = {'batch_size': [25, 32],
              'epochs': [100, 500],
              'optimizer': ['adam', 'rmsprop']}


grid_search = GridSearchCV(classifier, parameters, cv=10, scoring='accuracy')
grid_search = grid_search.fit(X_train, y_train)
best_parameters = grid_search.best_params_;
best_accuracy = grid_search.best_score_;


