# import libraries
import os

# Download
url = 'https://zenodo.org/record/6327379/files/'


# used in download and the create_dataset and train_model.ipynb
file_name = 'mars-express-power-3years'
file_extension = '.zip'
folder = './data'
PATH_TO_DATA = folder + "/" + file_name + "/"

# used in the create_dataset and train_model.ipynb
PATH_TRAIN_TO_PKL = PATH_TO_DATA + 'preprocessed/'
NAME_TRAIN_Y_TO_PKL = 'train_y.pkl'
NAME_TRAIN_X_TO_PKL = 'train_x.pkl'


# used in the train_model.ipynb
FULL_TRAIN_Y_TO_PKL = os.path.join(PATH_TRAIN_TO_PKL, NAME_TRAIN_Y_TO_PKL)
FULL_TRAIN_X_TO_PKL = os.path.join(PATH_TRAIN_TO_PKL, NAME_TRAIN_X_TO_PKL)

NAME_TEST_Y = 'test_y'
NAME_TEST_Y_HAT = 'test_y_hat'

FULL_TEST_Y = os.path.join(PATH_TRAIN_TO_PKL, NAME_TEST_Y)
FULL_TEST_Y_HAT = os.path.join(PATH_TRAIN_TO_PKL, NAME_TEST_Y_HAT)

PATH_MODEL = PATH_TO_DATA + 'model.pkl'
PATH_MODEL_ONNX = PATH_TO_DATA + 'model_rf.onnx'


# used in evaluate.ipynb
PATH_TRAIN_Y = os.path.join(PATH_TO_DATA, NAME_TRAIN_Y_TO_PKL)
PATH_TRAIN_X = os.path.join(PATH_TO_DATA, NAME_TRAIN_X_TO_PKL) 

PATH_TEST_Y = os.path.join(PATH_TO_DATA, 'test_y.npy') 
PATH_TEST_Y_HAT =  os.path.join(PATH_TO_DATA, 'test_y_hat.npy')  

PATH_TO_DATA_GE_DATASET = folder + "/" + file_name + "/great_expectations/estimated_y.csv"
