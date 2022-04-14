# import libraries
import os
import subprocess
from zipfile import ZipFile
import pandas as pd
from pandas import Timestamp
import logging

from mlspace.helpers import functions
from mlspace.helpers import configuration

from mlspace.helpers.quality_gate import QualityCheck
from mlspace.helpers.quality_gate import QualityGate1

# define class to prepare the dataset
class PrepareData:
    """ Download, analyze and prepare the dataset
    
    Attributes
    ----------
    feature_to_predict : str 
        target data to predict
    power_all : panda table
        contains the train and test of the power consumption
    power_col : list
        contains the column name of the power consumption
    saaf_all : panda table
        contains the train and test of the saaf
    saaf_cols : panda table
        contains the column name of the saaf
    ltdata_all : panda table
        contains the train and test of the ltdata
    ltdata_cols : panda table
        contains the column name of the ltdata
    dmop_all : panda table
        contains the train and test of the dmop
    dmop_cols : panda table
        contains the column name of the dmop
    ftl_all : panda table
        contains the train and test of the ftl
    ftl_cols : panda table
        contains the column name of the ftl
    """

    def __init__(self, feature_to_predict) -> None: 
        """
        Create the class PrepareData

        Parameters
        ----------
        feature_to_predict : str
                        target data to predict
        """
        logging.basicConfig(filename='logs/mlspace.log', encoding='utf-8', level=logging.INFO)

        self.feature_to_predict = feature_to_predict
        self.pass_quality_check = False
        self.skip_test_download = False
        self

    def download(self):
        """
        Function to download the dataset. All the parameters are in the configuration.py
        """
        logging.info("Downloading dataset ...")
        
        if not self.skip_test_download: 
            pass
        
        self.__download_unzip(configuration.url, configuration.file_name + configuration.file_extension, configuration.folder)

        return True

    def __download_unzip(self, url, file_name, folder):
        """
        Download and unzip the dataset

        Parameters
        ----------
        url : str
            link to download the dataset
        file_name : str
            name of the dataset with its extension
        folder: str
            name of the folder to store the dataset
        """
        # create the directory, if folder does not exist
        if os.path.isdir(folder) == False:
            logging.info('Creating the folder %s...' % folder)
            os.mkdir(folder)

        path = folder + '/' + file_name

        # download the file contents in binary format if it does not exist
        if os.path.exists(path) == False:
            logging.info('Downloading from %s, this may take a while...' % url)
            subprocess.call(['wget',
                            '--no-check-certificate',
                            url + file_name, 
                            '-P',
                            folder]) 

            # Create a ZipFile Object and load sample.zip in it
            with ZipFile(path, 'r') as zipObj:
                # Extract all the contents of zip file in directory folder
                zipObj.extractall(folder)

    def load_data(self):
        """
        Function to load the dataset. 
        """
        
        logging.info("Loading dataset ...")

        self.__load_data_power_all()
        self.__load_data_saaf_all()
        self.__load_data_ltdata_all()
        self.__load_data_dmop_all()
        self.__load_data_ftl_all()

        self.all_cols = self.saaf_cols + self.ltdata_cols + self.dmop_cols + self.ftl_cols
    
    def convert_time(self, df):
        """
        Function to convert the utc timestamp to datetime

        Parameters
        ----------
        df : DataFrame
            dataset as a data frame
        """
        df['ut_ms'] = pd.to_datetime(df['ut_ms'], unit='ms')
        return df

    def resample_1H(self, df):
        """
        Function to resample the dataframe to hourly mean

        Parameters
        ----------
        df : DataFrame
            dataset as a data frame
        """
        df = df.set_index('ut_ms')
        df = df.resample('1H').mean()
        return df

    def parse_ts(self, filename, dropna=True):
        """
        Function to read a csv file and resample to hourly consumption

        Parameters
        ----------
        filename : str
            name of the file
        dropna : bool
            if True remove rows with null values
        """
        df = pd.read_csv(configuration.PATH_TO_DATA + '/' + filename)
        df = self.convert_time(df)
        df = self.resample_1H(df)
        if dropna:
            df = df.dropna()
        return df

    def parse_ltdata(self, filename):
        """
        Function to read the ltdata files

        Parameters
        ----------
        filename : str
            name of the file
        """
        df = pd.read_csv(configuration.PATH_TO_DATA + '/' + filename)
        df = self.convert_time(df)
        df = df.set_index('ut_ms')
        return df

    def parse_dmop(self, filename):
        """
        Function to parse the dmop

        Parameters
        ----------
        filename : str
            name of the file
        """
        df = pd.read_csv(configuration.PATH_TO_DATA + '/' + filename)
        df = self.convert_time(df)

        subsystems = sorted({s[1:4] for s in df['subsystem'] if s[0] == 'A'})
        
        df_expansion = [
            [when] + [(1 if cmd[1:4]==syst else 0) for syst in subsystems]
            for (when, cmd) in df.values
            if cmd[0]=='A']
        
        df = pd.DataFrame(df_expansion, columns=['ut_ms'] + subsystems)
        df = df.set_index('ut_ms')
        
        # get one row per hour, containing the boolean values indicating whether each
        # subsystem was activated in that hour;
        # hours not represented in the file have all columns with 0.
        # df = df.resample('1H').max().fillna(0)
        # cells represent number of times intructions were issued to that subsystem in that hour
        df = df.resample('1H').sum().fillna(0)
        
        return df
        
    def parse_ftl(self, filename):
        """
        Function to read the FTL files and convert the columns to datetime

        Parameters
        ----------
        filename : str
            name of the file
        """
        df = pd.read_csv(configuration.PATH_TO_DATA + '/' + filename)
        df['utb_ms'] = pd.to_datetime(df['utb_ms'], unit='ms')
        df['ute_ms'] = pd.to_datetime(df['ute_ms'], unit='ms')
        return df

    def parse_ftl_all(self, filenames, hour_indices):
        """
        Function to parse all the ftl files

        Parameters
        ----------
        filename : str
            name of the file
        hour_indices : int
            indexes of the hours
        """
        ftl_all = pd.concat([self.parse_ftl(f) for f in filenames])
        
        types = sorted(set(ftl_all['type']))
        ftl_df = pd.DataFrame(index=hour_indices, columns=['flagcomms'] + types).fillna(0)
        
        # hour indices of discarded events, because of non-ocurrence in `hour_indices`
        ix_err = []

        for (t_start, t_end, p_type, comms) in ftl_all.values:
            floor_beg = Timestamp(t_start).floor('1h')
            floor_end = Timestamp(t_end).floor('1h')
            
            try:
                ftl_df.loc[floor_beg]['flagcomms'] = ftl_df.loc[floor_end]['flagcomms'] = int(comms)
                ftl_df.loc[floor_beg][p_type]      = ftl_df.loc[floor_end][p_type]      = 1
            except KeyError:
                ix_err.append((floor_beg, floor_end))
        
        logging.warning('Warning: discarded %d FTL events' % len(ix_err))
        
        return ftl_all, ftl_df

    def __load_data_power_all(self):
        """
        Private Function to load the power consumption. 
        """
        ## Load the power files: they are the columns that need to be predicted (predicted value)
        pow_train1 = self.parse_ts('/train_set/power--2008-08-22_2010-07-10.csv')
        pow_train2 = self.parse_ts('/train_set/power--2010-07-10_2012-05-27.csv')
        pow_train3 = self.parse_ts('/train_set/power--2012-05-27_2014-04-14.csv')

        # Load the test sample submission file as template for prediction
        pow_test = self.parse_ts('power-prediction-sample-2014-04-14_2016-03-01.csv', False)

        # Concatenate the files
        self.power_all = pd.concat([pow_train1, pow_train2, pow_train3, pow_test])

        # Extract the column names
        self.power_cols = list(self.power_all.columns)

    def __load_data_saaf_all(self):
        """
        Private Function to load the saaf files. 
        """
        # Load the saaf files: train samples
        saaf_train1 = self.parse_ts('/train_set/context--2008-08-22_2010-07-10--saaf.csv')
        saaf_train2 = self.parse_ts('/train_set/context--2010-07-10_2012-05-27--saaf.csv')
        saaf_train3 = self.parse_ts('/train_set/context--2012-05-27_2014-04-14--saaf.csv')
        
        # Load the test sample submission file 
        saaf_test = self.parse_ts('/test_set/context--2014-04-14_2016-03-01--saaf.csv')

        # Concatenate the files
        self.saaf_all = pd.concat([saaf_train1, saaf_train2, saaf_train3, saaf_test])

        # Extract the columns name
        self.saaf_cols = list(self.saaf_all.columns)

    def __load_data_ltdata_all(self):
        """
        Private Function to load the ltdata files. 
        """
        # Load the ltdata files: train samples
        ltdata_train1 = self.parse_ltdata('/train_set/context--2008-08-22_2010-07-10--ltdata.csv')
        ltdata_train2 = self.parse_ltdata('/train_set/context--2010-07-10_2012-05-27--ltdata.csv')
        ltdata_train3 = self.parse_ltdata('/train_set/context--2012-05-27_2014-04-14--ltdata.csv')
        
        # Load the test sample submission file 
        ltdata_test = self.parse_ltdata('/test_set/context--2014-04-14_2016-03-01--ltdata.csv')

        # Concatenate the files
        self.ltdata_all = pd.concat([ltdata_train1, ltdata_train2, ltdata_train3, ltdata_test])

        # Extract the columns name
        self.ltdata_cols = list(self.ltdata_all.columns)

    def __load_data_dmop_all(self):
        """
        Private Function to load the dmop files. 
        """
        # Load the dmop files: train samples
        dmop_train1 = self.parse_dmop('/train_set/context--2008-08-22_2010-07-10--dmop.csv')
        dmop_train2 = self.parse_dmop('/train_set/context--2010-07-10_2012-05-27--dmop.csv')
        dmop_train3 = self.parse_dmop('/train_set/context--2012-05-27_2014-04-14--dmop.csv')
        
        # Load the test sample submission file 
        dmop_test = self.parse_dmop('/test_set/context--2014-04-14_2016-03-01--dmop.csv')

        # Concatenate the files
        self.dmop_all = pd.concat([dmop_train1, dmop_train2, dmop_train3, dmop_test]).fillna(0)

        # Extract the columns name
        self.dmop_cols = list(self.dmop_all.columns)

    def __load_data_ftl_all(self):
        """
        Private Function to load the ftl files. 
        """
        self.df = self.power_all

        # Load the ftl files: train samples
        ftl_fnames = [
            '/train_set/context--2008-08-22_2010-07-10--ftl.csv',
            '/train_set/context--2010-07-10_2012-05-27--ftl.csv',
            '/train_set/context--2012-05-27_2014-04-14--ftl.csv',
            '/test_set/context--2014-04-14_2016-03-01--ftl.csv',
            ]
        self.ftl_all, self.ftl_df = self.parse_ftl_all(filenames=ftl_fnames, hour_indices=self.df.index)
        
        # Extract the columns name
        self.ftl_cols = list(self.ftl_all.columns)

    def analyze_data(self):    
        pass

    def check_quality_gate(self):
        
        if not self.pass_quality_check:

            # apply QG1-QC1
            (power_risks_range, power_unknown) = self.__check_range(self.power_all)
            (saaf_risks_range, saaf_unknown) = self.__check_range(self.saaf_all)
            (ltdata_risks_range, ltdata_unknown) = self.__check_range(self.ltdata_all)
            (dmop_risks_range, dmop_unknown) = self.__check_range(self.dmop_all)
            (ftl_risks_range, ftl_unknown) = self.__check_range(self.ftl_df)

            self.__print_risks_range("Power", power_risks_range, power_unknown)
            self.__print_risks_range("Saaf", saaf_risks_range, saaf_unknown)
            self.__print_risks_range("Ltdata", ltdata_risks_range, ltdata_unknown)
            self.__print_risks_range("Dmop", dmop_risks_range, dmop_unknown)
            self.__print_risks_range("Ftl", ftl_risks_range, ftl_unknown)


            # apply QG1-QC2
            self.__check_fill_gaps()


            # apply QG1-QC3
            # Name of the expectation suite
            expectation_suite_name = "mars_express_power_train_x.demo"

            # Name of the checkpoint
            checkpoint = "mars_express_power_train_x.demo" 

            # Name of the dataset to evaluate
            dataset_name = "train_x.csv"

            self.__check_great_expectation(dataset_name, checkpoint, expectation_suite_name)


            # apply QG1-QC4
            name_exp_dist = "power_expected_distribution"
            
            result = self.__check_expected_distribution(self.power_cols, self.power_all, name_exp_dist)

            logging.info(result["NPWD2401"])


            # if every quality check pass succesfully, we join all the explanatory features
            self.df = self.df.join(self.saaf_all)
            self.df = self.df.join(self.ltdata_all)
            self.df = self.df.join(self.dmop_all)
            self.df = self.df.join(self.ftl_df_sel)
            self.df.shape

            self.pass_quality_check = True


    # define the function to call the quality gate check range
    def __check_range(self, dataset_column):
        qg = QualityGate1("QG1-QC1", QualityCheck.QC1, dataset_column)
        return qg.execute()

    # function to print risks
    def __print_risks_range(self, text, risks, unknown):
        logging.info(text, ":")
        if len(risks) != 0:
            logging.warning(" -> risks range: \n", risks)
        if len(unknown) != 0:
            logging.warning(" -> the following feature are not inside the ontology:\n", unknown)


    # define the function to fill gaps
    def __check_fill_gaps(self):
        
        # saaf and LTDATA
        qg = QualityGate1("QG1-QC2", QualityCheck.QC2, "nearest")
        if qg.execute():
            # Make sure that saaf has the same sampling as the power, fill gaps with nearest value
            self.saaf_all = self.saaf_all.reindex(self.df.index, method=qg.arguments)
            self.ltdata_all = self.ltdata_all.reindex(self.df.index, method=qg.arguments)

        # DMOP files
        qg = QualityGate1("QG1-QC2", QualityCheck.QC2, "zero")
        if qg.execute():
            # Make sure that dmop_all has the same sampling as the power, fill NA with zero value
            self.dmop_all = self.dmop_all.reindex(self.df.index).fillna(0)
            # dmop_all = dmop_all.reindex(df.index, fill_value=0)


    # define the function to call the great expectation
    def __check_great_expectation(self, dataset_name, checkpoint, expectation_suite_name):
        qg = QualityGate1("QG1-QC3", QualityCheck.QC3, dataset_name, checkpoint, expectation_suite_name)
        return qg.execute()


    # define the function to call the expected distribution
    def __check_expected_distribution(self, power_cols, power_all, name_exp_dist):
        qg = QualityGate1("QG1-QC4", QualityCheck.QC4, power_cols, power_all, name_exp_dist)
        return qg.execute()


    # define function to save files
    def save_to_file(self):
        # TODO select features to predict 
        Y = self.df[self.power_cols] 

        # TODO select explanatory features from the relationships
        X = self.df.drop(self.power_cols, axis=1)

        # if the directory does not exist, we create it
        if not os.path.exists(configuration.PATH_TRAIN_TO_PKL):
            os.mkdir(configuration.PATH_TRAIN_TO_PKL)

        FULL_TRAIN_Y_TO_PKL = os.path.join(configuration.PATH_TRAIN_TO_PKL, configuration.NAME_TRAIN_Y_TO_PKL)
        FULL_TRAIN_X_TO_PKL = os.path.join(configuration.PATH_TRAIN_TO_PKL, configuration.NAME_TRAIN_X_TO_PKL)

        Y.to_pickle(FULL_TRAIN_Y_TO_PKL)
        X.to_pickle(FULL_TRAIN_X_TO_PKL)


def rmse():
    return functions.RMSE(2, 3)
