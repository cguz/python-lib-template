# import library 
import os
import pandas as pd
import numpy as np
import logging

from mlspace.helpers import functions
from mlspace.helpers import configuration


# define class to evaluate the model
class EvaluateModel():
    """ Evaluate Model
    
    Attributes
    ----------
    path_data : str 
        full path directory of the data X and Y
    metric_rmse : real
        metric root mean square error to store in mlflow
    """

    def __init__(self, path_data) -> None:
        """
        Create the class EvaluateModel

        Parameters
        ----------
        path_data : str
            full path directory of the data X and Y
        """
        self.path_data = path_data
        self.check_finish = False
        self

    def evaluate(self):

        # create the full path to store the data
        FULL_TEST_Y = os.path.join(self.path_data, configuration.NAME_TEST_Y+'.npy')
        FULL_TEST_Y_HAT = os.path.join(self.path_data, configuration.NAME_TEST_Y_HAT+'.npy')

        # load the estimated and real values
        Y_test = np.load(FULL_TEST_Y)
        Y_test_hat = np.load(FULL_TEST_Y_HAT)

        # load the metric rmse
        self.metric_rmse = functions.RMSE(Y_test, Y_test_hat)
        logging.info("Local prediction error: {}\n".format(self.metric_rmse))

        df = pd.DataFrame(Y_test_hat[0])
        df.rename(columns={0: 'NPWD2372'}, inplace=True)

        # create the folder if it does not exist
        if not os.path.exists(configuration.PATH_TO_DATA_GE):
            os.mkdir(configuration.PATH_TO_DATA_GE)
        
        # store it in the great expectation folder
        df.to_csv(configuration.PATH_TO_DATA_GE_DATASET, index=False) # save to new csv file

        self.check_finish = True

        