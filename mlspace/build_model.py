# import library 
import os
import pandas as pd
import logging

from mlspace.helpers import functions
from mlspace.helpers import configuration

from mlspace.helpers.quality_gate import QualityCheck
from mlspace.helpers.quality_gate import QualityGate2


# define class to build the model
class BuildModel():
    """ Build Model
    
    Attributes
    ----------
    path_data : str 
        full path directory of the data X and Y
    algorithm : str 
        name of the algorithm to use
    """

    def __init__(self, path_data, algorithm):
        """
        Create the class BuildModel

        Parameters
        ----------
        path_data : str
            full path directory of the data X and Y
        algorithm : str 
            name of the algorithm to use
        """
        logging.basicConfig(handlers=[logging.FileHandler(filename='logs/mlspace.log', encoding='utf-8', mode='a+')], level=logging.INFO)

        self.path_data = path_data
        self.algorithm = algorithm
        self.check_continue = False

    def build(self):
        """
        Method to analize if the algorithm to use is appropiated or not

        Return 
        ----------
        assign true to the variable self.check_continue if the algorithm is appropiated
        """

        # create the full path
        FULL_TRAIN_Y_TO_PKL = os.path.join(self.path_data, configuration.NAME_TRAIN_Y_TO_PKL)
        FULL_TRAIN_X_TO_PKL = os.path.join(self.path_data, configuration.NAME_TRAIN_X_TO_PKL)

        # read data X and Y
        X = pd.read_pickle(FULL_TRAIN_X_TO_PKL)
        Y = pd.read_pickle(FULL_TRAIN_Y_TO_PKL)

        qg = QualityGate2("QG2-QC1", QualityCheck.QC1, Y, self.algorithm)
        no_appropiate = qg.execute()
        if len(no_appropiate) != 0:
            logging.info("\n\nThe selected algorithm is not appropiate to solve the following features: ${0}".format(no_appropiate))
            print("\n\nThe selected algorithm is not appropiate to solve the following features: ", no_appropiate)
        else:
            logging.info("\n\nThe selected algorithm is appropiate, we can continue with the step 3, Train Model")
            print("\n\nThe selected algorithm is appropiate, we can continue with the step 3, Train Model")
            self.check_continue = True