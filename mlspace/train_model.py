# input is the path: configuration.PATH_TRAIN_TO_PKL

# import libraries
import os
import pandas as pd
import numpy as np
from pandas import Timestamp
import logging

import joblib

from sklearn.ensemble import RandomForestRegressor

from mlspace.helpers import functions
from mlspace.helpers import configuration


# define class to train the model
class TrainModel():
    """ Train Model
    
    Attributes
    ----------
    path_data : str 
        full path directory of the data X and Y
    """

    def __init__(self, path_data) -> None:
        """
        Create the class TrainModel

        Parameters
        ----------
        path_data : str
            full path directory of the data X and Y
        """
        logging.basicConfig(handlers=[logging.FileHandler(filename='logs/mlspace.log', encoding='utf-8', mode='a+')], level=logging.INFO)

        self.path_data = path_data
        self

    def train(self):

        # create the full path of the tain data
        FULL_TRAIN_Y_TO_PKL = os.path.join(self.path_data, configuration.NAME_TRAIN_Y_TO_PKL)
        FULL_TRAIN_X_TO_PKL = os.path.join(self.path_data, configuration.NAME_TRAIN_X_TO_PKL)

        # create the full path to store the data
        FULL_TEST_Y = os.path.join(self.path_data, configuration.NAME_TEST_Y)
        FULL_TEST_Y_HAT = os.path.join(self.path_data, configuration.NAME_TEST_Y_HAT)

        # read data X and Y
        X = pd.read_pickle(FULL_TRAIN_X_TO_PKL)
        Y = pd.read_pickle(FULL_TRAIN_Y_TO_PKL)

        # we split the data in two sets:
        trainset = ~Y.iloc[:,0].isnull()

        # 1) Y value are not null ( for training )
        X_train, Y_train = X[trainset], Y[trainset]

        # 2) Y value are null ( for test )
        X_test, Y_test = X[~trainset], Y[~trainset]


        # **************************************************** #
        # **************** TO CROSSVALIDATION **************** #
        # **************************************************** #
        # (trains on two years; leaves the 3rd for validation) #
        cv_split = X_train.index < '2012-05-27'
        X_train_cv, Y_train_cv = X_train[cv_split], Y_train[cv_split]
        X_val_cv, Y_val_cv = X_train[~cv_split], Y_train[~cv_split]

        logging.info("{0} {1}".format(X_train.shape, Y_train.shape))

        n_estimators = 100
        n_jobs = -1
        min_samples_leaf = 5

        # build the model
        self.model = RandomForestRegressor(n_estimators=n_estimators, n_jobs=n_jobs, min_samples_leaf=min_samples_leaf)

        # train the model
        self.model.fit(X_train_cv, Y_train_cv)

        # evaluate the model
        Y_val_cv_hat = self.model.predict(X_val_cv)
        rmse =  functions.RMSE(Y_val_cv, Y_val_cv_hat)

        print("Local prediction error: {}\n".format(rmse))
        print("Feature importances:")
        for feature, importance in sorted(zip(self.model.feature_importances_, X_train.columns), key=lambda x: x[0], reverse=True):
            print(feature, importance)


        # train and test the model with the complete dataset
        self.model.fit(X_train, Y_train)

        Y_test_hat = self.model.predict(X_test)

        # store predicted value and real value
        np.save(FULL_TEST_Y_HAT, Y_test_hat)
        np.save(FULL_TEST_Y, Y_test)

        # store the model
        joblib.dump(self.model, configuration.PATH_MODEL)