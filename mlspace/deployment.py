# import library 
import logging

from mlspace.helpers.quality_gate import QualityCheck
from mlspace.helpers.quality_gate import QualityGate1


# define class to deployment the model
class DeploymentModel():
    """ Deployment Model
    
    Attributes
    ----------
    pass_quality_check : bool 
        inform if the deployment pass the quality check
    expectation_suite_name : str 
        name of the suite name of the great expectation
    checkpoint : str 
        name of the checkpoint of the great expectation
    dataset_name : str 
        name of the dataset of the great expectation
    """

    def __init__(self):
        """
        Create the class DeploymentModel
        """
        logging.basicConfig(handlers=[logging.FileHandler(filename='logs/mlspace.log', encoding='utf-8', mode='a+')], level=logging.INFO)

        self.pass_quality_check = False
        
        # Name of the expectation suite
        self.expectation_suite_name = "mars_express_power_consumption_y.demo"

        # Name of the checkpoint
        self.checkpoint = "checkpoint_power_consumption.demo" 

        # Name of the dataset to evaluate
        self.dataset_name = "estimated_y.csv"

    def check_quality_gate(self):
        """
        Execute the QG
        """
        
        if not self.pass_quality_check:

            # apply QG3-QC1
            (output_no_deployment) = self.__check_great_expectation(self.dataset_name, self.checkpoint, self.expectation_suite_name)

            if len(output_no_deployment) != 0:
                logging.info("\n\nThe selected model is appropiate to deployment")
                print("\n\nThe selected model is appropiate to deployment")
                self.pass_quality_check = True
            else:
                logging.info("\n\nThe selected model is not appropiate to deployment")
                print("\n\nThe selected model is not appropiate to deployment")

    
    # define the function to call the great expectation
    def __check_great_expectation(self, dataset_name, checkpoint, expectation_suite_name):
        """
        Private function to execute the great expectation
    
        Attributes
        ----------
        dataset_name : str 
            name of the dataset of the great expectation
        checkpoint : str 
            name of the checkpoint of the great expectation
        expectation_suite_name : str 
            name of the suite name of the great expectation

        Return
        ----------
        if the model is not appropiated for deployment
        """
        qg = QualityGate1("QG3-QC1", QualityCheck.QC3, dataset_name, checkpoint, expectation_suite_name)
        return qg.execute()