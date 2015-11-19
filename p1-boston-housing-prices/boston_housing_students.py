"""
Loading the boston dataset and examining its target (label) distribution.
"""

# Load libraries
import numpy as np
import pylab as pl
import pandas as pd
from ggplot import *
from sklearn import cross_validation
from sklearn.cross_validation import KFold
from sklearn import grid_search
from sklearn import datasets
from sklearn import metrics
from sklearn.tree import DecisionTreeRegressor

################################
### ADD EXTRA LIBRARIES HERE ###
################################
def selected_features():
    # Selecting a few of the features (instead of using all) might improve performance.

    return ["CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PTRATIO", "B", "LSTAT"]

def features_to_string():
    return reduce(lambda x, y: x + ', ' + y, selected_features())

def df_features(housing_features):
        column_names = ["CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PTRATIO", "B", "LSTAT"]

        row_length, col_length = housing_features.shape
        dictionary = {}

        for col_i in range(0,col_length):
          current_column_name = column_names[col_i]
          values = []

          for row_i in range(0,row_length):
            current_feature_value = housing_features[row_i][col_i]
            values.append(current_feature_value)

          dictionary[current_column_name] = values

        df = pd.DataFrame.from_dict(dictionary)

        return df[selected_features()]

def load_data():
        '''Load the Boston dataset.'''

        boston = datasets.load_boston()
        return boston


def explore_city_data(city_data):
        '''Calculate the Boston housing statistics.'''

        # Get the labels and features from the housing data
        housing_prices = city_data.target
        housing_features = city_data.data

        ###################################
        ### Step 1. YOUR CODE GOES HERE ###
        ###################################

        # Please calculate the following values using the Numpy library
        # Size of data?
        # Number of features?
        # Minimum value?
        # Maximum Value?
        # Calculate mean?
        # Calculate median?
        # Calculate standard deviation?

        housing_series = pd.Series(housing_prices)

        print "housing_series.describe"
        print housing_series.describe()
        print "\n"

        # housing_series.describe
        # count    506.000000
        # mean      22.532806
        # std        9.197104
        # min        5.000000
        # 25%       17.025000
        # 50%       21.200000
        # 75%       25.000000
        # max       50.000000

        print "housing_features.shape"
        print housing_features.shape
        print "\n"

def performance_metric(label, prediction):

        '''Calculate and return the appropriate performance metric.'''

        ###################################
        ### Step 2. YOUR CODE GOES HERE ###
        ###################################

        # http://scikit-learn.org/stable/modules/classes.html#sklearn-metrics-metrics

        return metrics.mean_squared_error(label, prediction)

def split_data(city_data):
        '''Randomly shuffle the sample set. Divide it into training and testing set.'''

        # Get the features and labels from the Boston housing data
        X, y = city_data.data, city_data.target

        ###################################
        ### Step 3. YOUR CODE GOES HERE ###
        ###################################

        X_train, X_test, y_train, y_test = cross_validation.train_test_split(df_features(X), y, test_size=0.2, random_state=42)

        # kf = KFold(n=506, n_folds=5, shuffle=True, random_state=True)

        # for train_index, test_index in kf:
           # print("TRAIN:", train_index, "TEST:", test_index)
           # X_train, X_test = X[train_index], X[test_index]
           # y_train, y_test = y[train_index], y[test_index]

        return X_train, y_train, X_test, y_test


def learning_curve(depth, X_train, y_train, X_test, y_test):
        '''Calculate the performance of the model after a set of training data.'''

        # We will vary the training set size so that we have 50 different sizes
        sizes = np.linspace(1, len(X_train), 50)
        train_err = np.zeros(len(sizes))
        test_err = np.zeros(len(sizes))

        print "Decision Tree with Max Depth: "
        print depth

        for i, s in enumerate(sizes):

                # Create and fit the decision tree regressor model
                regressor = DecisionTreeRegressor(max_depth=depth)
                regressor.fit(X_train[:int(s)], y_train[:int(s)])

                # Find the performance on the training and testing set
                train_err[i] = performance_metric(y_train[:int(s)], regressor.predict(X_train[:int(s)]))
                test_err[i] = performance_metric(y_test, regressor.predict(X_test))


        # Plot learning curve graph
        learning_curve_graph(sizes, train_err, test_err, depth)


def learning_curve_graph(sizes, train_err, test_err, depth):
        '''Plot training and test error as a function of the training size.'''

        pl.figure()
        pl.title('Decision Trees: Performance vs Training Size - Depth ' + str(depth) + ', f: ' + features_to_string())
        pl.plot(sizes, test_err, lw=2, label = 'test error')
        pl.plot(sizes, train_err, lw=2, label = 'training error')
        pl.legend()
        pl.xlabel('Training Size')
        pl.ylabel('Error')
        pl.savefig('dt-perf-vs-ts-' + features_to_string())
        pl.show()


def model_complexity(X_train, y_train, X_test, y_test):
        '''Calculate the performance of the model as model complexity increases.'''

        print "Model Complexity: "

        # We will vary the depth of decision trees from 2 to 25
        max_depth = np.arange(1, 25)
        train_err = np.zeros(len(max_depth))
        test_err = np.zeros(len(max_depth))

        for i, d in enumerate(max_depth):
                # Setup a Decision Tree Regressor so that it learns a tree with depth d
                regressor = DecisionTreeRegressor(max_depth=d)

                # Fit the learner to the training data
                regressor.fit(X_train, y_train)

                # Find the performance on the training set
                train_err[i] = performance_metric(y_train, regressor.predict(X_train))

                # Find the performance on the testing set
                test_err[i] = performance_metric(y_test, regressor.predict(X_test))

        # Plot the model complexity graph
        model_complexity_graph(max_depth, train_err, test_err)


def model_complexity_graph(max_depth, train_err, test_err):
        '''Plot training and test error as a function of the depth of the decision tree learn.'''

        pl.figure()
        pl.title('Decision Trees: Performance vs Max Depth, f: ' + features_to_string())
        pl.plot(max_depth, test_err, lw=2, label = 'test error')
        pl.plot(max_depth, train_err, lw=2, label = 'training error')
        pl.legend()
        pl.xlabel('Max Depth')
        pl.ylabel('Error')
        pl.show()


def fit_predict_model(city_data):
        '''Find and tune the optimal model. Make a prediction on housing data.'''

        # Get the features and labels from the Boston housing data
        X, y = city_data.data, city_data.target

        # Setup a Decision Tree Regressor
        regressor = DecisionTreeRegressor()

        parameters = {'max_depth':(1,2,3,4,5,6,7,8,9,10)}

        ###################################
        ### Step 4. YOUR CODE GOES HERE ###
        ###################################

        # 1. Find the best performance metric
        # should be the same as your performance_metric procedure
        # http://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html

        # 2. Use gridearch to fine tune the Decision Tree Regressor and find the best model
        # http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html#sklearn.grid_search.GridSearchCV


        reg = grid_search.GridSearchCV(regressor, parameters, scoring='mean_squared_error')
        # Fit the learner to the training data
        print "Final Model: "
        print reg.fit(df_features(X), y)
        # print reg.fit(X, y)

    # Use the model to predict the output of a particular sample
        df_x = pd.DataFrame.from_dict(
            {
                'CRIM': [11.95],
                'ZN': [0.00],
                'INDUS': [18.100],
                'CHAS': [0],
                'NOX': [0.6590],
                'RM': [5.6090],
                'AGE': [90.00],
                'DIS': [1.385],
                'RAD': [24],
                'TAX': [680.0],
                'PTRATIO': [20.20],
                'B': [332.09],
                'LSTAT': [12.13] })

        x = df_x[selected_features()]
        print "x "
        print x
        print "\n"

        y = reg.predict(x)
        print "House: " + str(x)
        print "Prediction: " + str(y)

        print "reg.best_estimator_"
        print reg.best_estimator_
        print "\n"



def main():
        '''Analyze the Boston housing data. Evaluate and validate the
        performanance of a Decision Tree regressor on the Boston data.
        Fine tune the model to make prediction on unseen data.'''

        # Load data
        city_data = load_data()

        # Explore the data
        explore_city_data(city_data)

        # Training/Test dataset split
        X_train, y_train, X_test, y_test = split_data(city_data)

        # Learning Curve Graphs
        max_depths = [1,2,3,4,5,6,7,8,9,10]
        for max_depth in max_depths:
            learning_curve(max_depth, X_train, y_train, X_test, y_test)

        # Model Complexity Graph
        model_complexity(X_train, y_train, X_test, y_test)

        # Tune and predict Model
        fit_predict_model(city_data)

main()

