import numpy as np
import great_expectations as ge
import logging

from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter
from ruamel.yaml import YAML
from pprint import pprint
from enum import Enum
from ast import literal_eval

from abc import ABC, abstractmethod

from mlspace.helpers.features import Features, Feature
from mlspace.helpers.fill_gap_techniques import FillGaps
from mlspace.helpers.algorithms import Algorithm, TypeData

from mlspace.helpers.features import edge_label_hasA

from mlspace.helpers import functions


class QualityCheck(Enum): 
    """
    create an enumerate for the quality check
    """
    QC1 = 1
    QC2 = 2 
    QC3 = 3 
    QC4 = 4

class QualityGate(ABC):
    """
    create the QualityGate interface
    """
    
    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def execute(self):
        pass

# Quality Gate 1
class QualityGate1(QualityGate):
    """
    Class that represents the QualityGate1

    Arguments
    ----------
    name : str 
        name of the quality gate 
    quality_check : Enum 
        enumerate that identify the QualityCheck
    arguments : DataFrame 
        set of arguments required for the QGs
    checkpoint : str 
        name of the checkpoint of the great expectation
    expectation_suite_name : str 
        name of the suite name of the great expectation
    """
    def __init__(self, name, quality_check, arguments, checkpoint='', expectation_suite_name=''):
        """
        initialize the QG1

        Arguments
        ----------
        name : str 
            name of the quality gate 
        quality_check : Enum 
            enumerate that identify the QualityCheck
        arguments : DataFrame 
            set of arguments required for the QGs
        checkpoint : str 
            name of the checkpoint of the great expectation
        expectation_suite_name : str 
            name of the suite name of the great expectation
        """
        if not isinstance(self, QualityGate): raise Exception('Bad interface')
        if not self.version() == '1.0': raise Exception('Bad revision')

        self.name = name
        self.quality_check = quality_check
        self.arguments = arguments

        # for the QC3
        self.checkpoint = checkpoint
        self.expectation_suite_name = expectation_suite_name

    def execute(self):
        """
        function that execute the QG
        """
        if self.quality_check == QualityCheck.QC1:
            qg = QualityGateCheckRange(self.name, self.quality_check, self.arguments)
            
        if self.quality_check == QualityCheck.QC2:
            qg = QualityGateFillGates(self.name, self.quality_check, self.arguments)

        if self.quality_check == QualityCheck.QC3:
            qg = QualityGateGreatExpectation(self.name, self.quality_check, self.arguments, self.checkpoint, self.expectation_suite_name)

        if self.quality_check == QualityCheck.QC4:
            qg = QualityGateCheckExpectedDistribution(self.name, self.quality_check, self.arguments, self.checkpoint, self.expectation_suite_name)
            
        return qg.execute()

class QualityGate2(QualityGate):
    """
    Class that represents the QualityGate2

    Arguments
    ----------
    name : str 
        name of the quality gate 
    quality_check : Enum 
        enumerate that identify the QualityCheck
    arguments : DataFrame 
        set of arguments required for the QGs
    algorithm : str 
        name of the algorithm
    """
    def __init__(self, name, quality_check, arguments, algorithm):
        """
        Function to initialize the QG2

        Arguments
        ----------
        name : str 
            name of the quality gate 
        quality_check : Enum 
            enumerate that identify the QualityCheck
        arguments : DataFrame 
            set of arguments required for the QGs
        algorithm : str 
            name of the algorithm
        """
        if not isinstance(self, QualityGate): raise Exception('Bad interface')
        if not self.version() == '1.0': raise Exception('Bad revision')

        self.name = name
        self.quality_check = quality_check
        self.arguments = arguments
        self.algorithm = algorithm

    def execute(self):
        """
        Function to execute the QGs
        """
        if self.quality_check == QualityCheck.QC1:
            qg = QualityGateAlgorithm(self.name, self.quality_check, self.arguments, self.algorithm)
            
        return qg.execute()

class QualityGateGreatExpectation(QualityGate):
    """
    Class that represents the Great Expectation Quality Gate

    Arguments
    ----------
    name : str 
        name of the quality gate 
    quality_check : Enum 
        enumerate that identify the QualityCheck
    arguments : DataFrame 
        set of arguments required for the QGs
    checkpoint : str 
        name of the checkpoint of the great expectation
    expectation_suite_name : str 
        name of the suite name of the great expectation
    """
    def __init__(self, name, quality_check, dataset_name, checkpoint, expectation_suite_name):
        """
        Function to initialize the QG

        Arguments
        ----------
        name : str 
            name of the quality gate 
        quality_check : Enum 
            enumerate that identify the QualityCheck
        arguments : DataFrame 
            set of arguments required for the QGs
        checkpoint : str 
            name of the checkpoint of the great expectation
        expectation_suite_name : str 
            name of the suite name of the great expectation
        """
        if not isinstance(self, QualityGate): raise Exception('Bad interface')
        if not self.version() == '1.0': raise Exception('Bad revision')

        self.name = name
        self.quality_check = quality_check
        self.dataset_name = dataset_name
        self.checkpoint = checkpoint
        self.expectation_suite_name = expectation_suite_name
                
        self.yaml = YAML()
        self.context = ge.get_context()

    def execute(self):
        """
        Function to execute the QG
        """
        # Name of the datasource
        datasource_name = "mars_express_power"

        # Name of the checkpoint
        # checkpoint = context.list_checkpoints()[0]

        self.create_checkpoint(self.checkpoint, self.expectation_suite_name, datasource_name, self.dataset_name)

        # check if the checkpoint is inside the list of checkpoints
        if self.checkpoint in self.context.list_checkpoints():

            logging.info("${0} ${1}".format(self.checkpoint, self.context.list_checkpoints()))

            # execute the QG3
            self.context.run_checkpoint(checkpoint_name=self.checkpoint)
            self.context.open_data_docs()
            
            return [True]
        
        return []
        
    def create_checkpoint(self, checkpoint_name, expectation_suite_name, datasource_name, dataset_name):
        """
        Function to create the checkpoint . Create through the IMLO14-QG3

        Arguments
        ----------
        checkpoint : str 
            name of the checkpoint of the great expectation
        expectation_suite_name : str 
            name of the suite name of the great expectation
        datasource_name : str 
            name of the datasource of the great expectation
        dataset_name : str 
            name of the dataset of the great expectation
        """
        #create the yaml configuration file
        yaml_config = self.create_configuration(checkpoint_name, expectation_suite_name, datasource_name, dataset_name)

        logging.info("Generated checkpoint: \n ${0}".format(yaml_config))

        # test checkpoint configuration
        # my_checkpoint = context.test_yaml_config(yaml_config=yaml_config)
        # logging.info(my_checkpoint.get_substituted_config())
        
        # store the checkpoint yaml configuration
        self.context.add_checkpoint(**self.yaml.load(yaml_config))

    # create configuration yaml file
    def create_configuration(self, checkpoint_name, expectation_suite_name, datasource_name, dataset_name):
        """
        Function to generate the YAML configuration content

        Arguments
        ----------
        checkpoint : str 
            name of the checkpoint of the great expectation
        expectation_suite_name : str 
            name of the suite name of the great expectation
        datasource_name : str 
            name of the datasource of the great expectation
        dataset_name : str 
            name of the dataset of the great expectation

        Return
        ----------
        yaml configuration content
        """
        yaml_config = f"""
        name: {checkpoint_name}
        config_version: 1.0
        class_name: SimpleCheckpoint
        run_name_template: "%Y%m%d-%H%M%S-my-run-name-template"
        validations:
        - batch_request:
            datasource_name: {datasource_name}
            data_connector_name: default_inferred_data_connector_name
            data_asset_name: {dataset_name}
            data_connector_query:
                index: -1
          expectation_suite_name: {expectation_suite_name}
        """
        return yaml_config

class QualityGateCheckRange(QualityGate):
    """
    Function to initialize the QualityGateCheckRange

    Arguments
    ----------
    name : str 
        name of the quality gate 
    quality_check : Enum 
        enumerate that identify the QualityCheck
    arguments : DataFrame 
        set of arguments required for the QGs
    """
    def __init__(self, name, quality_check, arguments):
        """
        Function to initialize the QualityGateCheckRange

        Arguments
        ----------
        name : str 
            name of the quality gate 
        quality_check : Enum 
            enumerate that identify the QualityCheck
        arguments : DataFrame 
            set of arguments required for the QGs
        """
        if not isinstance(self, QualityGate): raise Exception('Bad interface')
        if not self.version() == '1.0': raise Exception('Bad revision')

        self.name = name
        self.quality_check = quality_check
        self.arguments = arguments

    def execute(self):
        """
        Function to execute the QG
        """
        return self.check_range(self.arguments)

    def check_range(self, features):
        """
        Function to check the range values

        Arguments
        ----------
        features : DataFrame 
            set of features to check the range considering the Ontology
        """

        list_warnings_risks_range = []
        list_warnings_unknown = []

        # for each feature f
        for f in features:

            # get the feature f in the ML Space Ontology
            feature = Feature(f)
            feature.find()

            # if we found the feature
            if feature.exist():

                # get the values min and max of the current feature f and check if they are valid
                if features[f].min() < float(feature.MinValue) or features[f].max() > float(feature.MaxValue):
                    list_warnings_risks_range.append(f)
            
            else:
                list_warnings_unknown.append(f)

        return list_warnings_risks_range, list_warnings_unknown

class QualityGateFillGates(QualityGate):
    """
    Function to initialize the QualityGateFillGates

    Arguments
    ----------
    name : str 
        name of the quality gate 
    quality_check : Enum 
        enumerate that identify the QualityCheck
    gap_name : str 
        name of the gap 
    """
    def __init__(self, name, quality_check, gap_name):
        """
        Function to initialize the QualityGateFillGates

        Arguments
        ----------
        name : str 
            name of the quality gate 
        quality_check : Enum 
            enumerate that identify the QualityCheck
        gap_name : str 
            name of the gap 
        """
        if not isinstance(self, QualityGate): raise Exception('Bad interface')
        if not self.version() == '1.0': raise Exception('Bad revision')

        self.name = name
        self.quality_check = quality_check
        self.gap_name = gap_name

    def execute(self):
        """
        Function to execute the QG
        """        
        gap = FillGaps(self.gap_name)
        gap.find()

        return gap.exist()


# Check Expected Distribution Quality Gate
class QualityGateCheckExpectedDistribution(QualityGate):
    """
    Function to Check Expected Distribution Quality Gate

    Arguments
    ----------
    name : str 
        name of the quality gate 
    quality_check : Enum 
        enumerate that identify the QualityCheck
    name_cols : str 
        name of the features
    all_cols : DataFrame 
        set of features
    name_exp_dist : str 
        name of the expected distribution 
    """
    def __init__(self, name, quality_check, name_cols, all_cols, name_exp_dist):
        if not isinstance(self, QualityGate): raise Exception('Bad interface')
        if not self.version() == '1.0': raise Exception('Bad revision')

        self.name = name
        self.quality_check = quality_check
        self.name_cols = name_cols
        self.all_cols = all_cols
        self.name_exp_dist = name_exp_dist

    def execute(self):
        """
        Function to execute the QG
        """
        exp_distribution = None
        exp_hist = []
        exp_bins = []
        exp_ppf  = []
        exp_cdf  = []

        result_exp_dist = {}

        # for each feature of power consumption
        for name in self.name_cols:
            
            # get the feature from the ML Space Ontology
            feature = Feature(name)
            feature.find()

            # if the feature exist
            if feature.exist():
                # check if there is a relationship between the Feature and the expected distribution
                # TODO: we can simplify to add the expected distribution from the ML Ontology
                if feature.exist_relationship(self.name_exp_dist, edge_label_hasA):
                    # if there is a relationship, we get the expected distribution
                    # NOTE: in this example, we get the same ED for all the Features.
                    if exp_distribution == None:
                        exp_distribution = feature.get_expected_distribution(self.name_exp_dist)
                        exp_hist = literal_eval(exp_distribution.Hist)
                        exp_bins = literal_eval(exp_distribution.Bins)
                        exp_ppf  = literal_eval(exp_distribution.Ppf)
                        exp_cdf  = literal_eval(exp_distribution.Cdf)

                    # considering the exp_bins, we calculate the actual ppf or hist
                    act_hist, _, act_ppf, _ = functions.gen_histogram(self.all_cols[name], False, exp_bins)

                    # get indeces with wrong range
                    # make the difference between the exp_ppf and the actual ppf or exp_hist and the actual hist
                    index_sub_set = functions.get_indices_with_wrong_range(act_ppf, exp_ppf)

                    # store the subset 
                    result_exp_dist[name] = index_sub_set

                    logging.info("Calculating ${0} for ${1} ".format(exp_distribution.Name, feature.Name))
                    #logging.info("exp ppf: ", exp_ppf[0])
                    #logging.info("actual ppf:", act_ppf[0])
                    #logging.info(index_sub_set)

        return result_exp_dist

class QualityGateAlgorithm(QualityGate):
    """
    Class that represents the QualityGateAlgorithm. Check if the algorithm is appropiated, depending on the type of features.

    Arguments
    ----------
    name : str 
        name of the quality gate 
    quality_check : Enum 
        enumerate that identify the QualityCheck
    features : DataFrame 
        set of features required for the QGs
    algorithm : str 
        name of the algorithm
    """
    def __init__(self, name, quality_check, features, algorithm):
        """
        Initialize the QG

        Arguments
        ----------
        name : str 
            name of the quality gate 
        quality_check : Enum 
            enumerate that identify the QualityCheck
        features : DataFrame 
            set of features required for the QGs
        algorithm : str 
            name of the algorithm
        """
        if not isinstance(self, QualityGate): raise Exception('Bad interface')
        if not self.version() == '1.0': raise Exception('Bad revision')

        self.name = name
        self.quality_check = quality_check
        self.features = features
        self.algorithm = algorithm

    def execute(self):
        """
        Function to execute the QG
        """        
        list_warnings_no_appropiate = []

        # TODO: They should come from the Ontology
        list_algorithms_continous=self.get_algorithms_continous()
        list_algorithms_discrete=self.get_algorithms_discrete()

        # for each feature f
        for f in self.features:

            # get the f in the ML Space Ontology
            feature = Feature(f)
            feature.find()

            # if we found the feature
            if feature.exist():
            
                # get the values min and max of the current feature f and check if they are valid
                if feature.TypeData == "Continuous":
                    if self.algorithm not in list_algorithms_continous:
                        list_warnings_no_appropiate.append(f)
                else:
                    if self.algorithm not in list_algorithms_discrete:
                        list_warnings_no_appropiate.append(f)

        return list_warnings_no_appropiate

    def get_algorithms_continous(self):
        """
        Function to retrieve the appropiated algorithms for Continuous Data Type
        """
        return TypeData("Continuous").get_appropiate_algorithms_str()
        # return ["RandomForest", "LinearRegression", "NeuralNetworkRegression", "RigdeRegression", "KNN", "SVM"]

    def get_algorithms_discrete(self):
        """
        Function to retrieve the appropiated algorithms for Continuous Data Type
        """
        return TypeData("Discrete").get_appropiate_algorithms_str()
        # return ["RandomForest", "LogisticRegression", "NaiveBayes", "DecisionTree", "SVM", "StochasticGradientDescent", "KNearest"]