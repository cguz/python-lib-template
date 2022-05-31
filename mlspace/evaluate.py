# import library 
import os
import pandas as pd
import numpy as np
import logging

from mlspace.helpers import functions
from mlspace.helpers import configuration

class EvaluateModel():
    """ 
    define class to evaluate the model 
    
    Attributes
    ----------
    path_data : str 
        full path directory of the data X and Y
    metric_rmse : real
        metric root mean square error to store in mlflow
    """

    def __init__(self, path_data):
        """
        Create the class EvaluateModel

        Parameters
        ----------
        path_data : str
            full path directory of the data X and Y
        """
        logging.basicConfig(handlers=[logging.FileHandler(filename='logs/mlspace.log', encoding='utf-8', mode='a+')], level=logging.INFO)

        self.path_data = path_data
        self.check_finish = False

    def evaluate(self):
        """
        Function to evaluate the model
        """
        # create the full path to store the data
        FULL_TEST_Y = os.path.join(self.path_data, configuration.NAME_TEST_Y+'.npy')
        FULL_TEST_Y_HAT = os.path.join(self.path_data, configuration.NAME_TEST_Y_HAT+'.npy')

        # load the estimated and real values
        Y_test = np.load(FULL_TEST_Y)
        self.Y_test_hat = np.load(FULL_TEST_Y_HAT)

        # load the metric rmse
        self.metric_rmse = functions.RMSE(Y_test, self.Y_test_hat)
        logging.info("Local prediction error: ${0}\n".format(self.metric_rmse))

        self.__store_to_file_csv()

        self.check_finish = True

    def __store_to_file_csv(self):
        """
        Private function to stor the estimated Y value to csv file
        """
        df = pd.DataFrame(self.Y_test_hat[0])
        df.rename(columns={0: 'NPWD2372'}, inplace=True)

        # create the folder if it does not exist
        if not os.path.exists(configuration.PATH_TO_DATA_GE):
            os.mkdir(configuration.PATH_TO_DATA_GE)
        
        # store it in the great expectation folder
        df.to_csv(configuration.PATH_TO_DATA_GE_DATASET, index=False)