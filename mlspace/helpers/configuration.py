# import libraries
import os


# Download
url = 'https://zenodo.org/record/6327379/files/'

# Configurate the connection to gremlin
CONFIG_CONNECTION='ws://localhost:8182/gremlin'

# used in download and the create_dataset and train_model.ipynb
file_name = 'mars-express-power-3years'
file_extension = '.zip'
folder = '../data'

NAME_TRAIN_Y_TO_PKL = 'train_y.pkl'
NAME_TRAIN_X_TO_PKL = 'train_x.pkl'

NAME_TRAIN_Y_TO_CSV = 'train_y.csv'
NAME_TRAIN_X_TO_CSV = 'train_x.csv'

NAME_TEST_Y = 'test_y'
NAME_TEST_Y_HAT = 'test_y_hat'


PATH_TO_DATA = os.path.join(folder+ "/", file_name + "/")

# used in the create_dataset and train_model.ipynb
PATH_TRAIN_TO_PKL = PATH_TO_DATA + 'preprocessed/'

# used in the train_model.ipynb
FULL_TRAIN_Y_TO_PKL = os.path.join(PATH_TRAIN_TO_PKL, NAME_TRAIN_Y_TO_PKL)
FULL_TRAIN_X_TO_PKL = os.path.join(PATH_TRAIN_TO_PKL, NAME_TRAIN_X_TO_PKL)

FULL_TEST_Y = os.path.join(PATH_TRAIN_TO_PKL, NAME_TEST_Y)
FULL_TEST_Y_HAT = os.path.join(PATH_TRAIN_TO_PKL, NAME_TEST_Y_HAT)

PATH_MODEL = PATH_TO_DATA + 'model.pkl'
PATH_MODEL_ONNX = PATH_TO_DATA + 'model_rf.onnx'


# used in evaluate.ipynb
PATH_TRAIN_Y = os.path.join(PATH_TO_DATA, NAME_TRAIN_Y_TO_PKL)
PATH_TRAIN_X = os.path.join(PATH_TO_DATA, NAME_TRAIN_X_TO_PKL) 

PATH_TEST_Y = os.path.join(PATH_TO_DATA, 'test_y.npy') 
PATH_TEST_Y_HAT =  os.path.join(PATH_TO_DATA, 'test_y_hat.npy')  

PATH_TO_DATA_GE = os.path.join(PATH_TO_DATA, "great_expectations/")
PATH_TO_DATA_GE_DATASET = os.path.join(PATH_TO_DATA_GE, "estimated_y.csv")

FULL_TRAIN_Y_TO_CSV = os.path.join(PATH_TO_DATA_GE, NAME_TRAIN_Y_TO_CSV)
FULL_TRAIN_X_TO_CSV = os.path.join(PATH_TO_DATA_GE, NAME_TRAIN_X_TO_CSV)


def update_folders():
    """
    update the variables related to folders
    """

    global folder
    global file_name
    global PATH_TO_DATA
    global PATH_TRAIN_TO_PKL
    global FULL_TRAIN_Y_TO_PKL
    global NAME_TRAIN_Y_TO_PKL
    global FULL_TRAIN_X_TO_PKL
    global NAME_TRAIN_X_TO_PKL
    global NAME_TEST_Y
    global NAME_TEST_Y_HAT
    global FULL_TEST_Y
    global FULL_TEST_Y_HAT
    global PATH_MODEL
    global PATH_MODEL_ONNX
    global PATH_TRAIN_Y
    global PATH_TRAIN_X
    global PATH_TEST_Y
    global PATH_TEST_Y_HAT
    global PATH_TO_DATA_GE
    global PATH_TO_DATA_GE_DATASET
    global NAME_TRAIN_Y_TO_CSV
    global NAME_TRAIN_X_TO_CSV
    global FULL_TRAIN_Y_TO_CSV
    global FULL_TRAIN_X_TO_CSV
    

    PATH_TO_DATA = os.path.join(folder+ "/", file_name + "/")

    # used in the create_dataset and train_model.ipynb
    PATH_TRAIN_TO_PKL = PATH_TO_DATA + 'preprocessed/'

    # used in the train_model.ipynb
    FULL_TRAIN_Y_TO_PKL = os.path.join(PATH_TRAIN_TO_PKL, NAME_TRAIN_Y_TO_PKL)
    FULL_TRAIN_X_TO_PKL = os.path.join(PATH_TRAIN_TO_PKL, NAME_TRAIN_X_TO_PKL)

    FULL_TEST_Y = os.path.join(PATH_TRAIN_TO_PKL, NAME_TEST_Y)
    FULL_TEST_Y_HAT = os.path.join(PATH_TRAIN_TO_PKL, NAME_TEST_Y_HAT)

    PATH_MODEL = PATH_TO_DATA + 'model.pkl'
    PATH_MODEL_ONNX = PATH_TO_DATA + 'model_rf.onnx'


    # used in evaluate.ipynb
    PATH_TRAIN_Y = os.path.join(PATH_TO_DATA, NAME_TRAIN_Y_TO_PKL)
    PATH_TRAIN_X = os.path.join(PATH_TO_DATA, NAME_TRAIN_X_TO_PKL) 

    PATH_TEST_Y = os.path.join(PATH_TO_DATA, 'test_y.npy') 
    PATH_TEST_Y_HAT =  os.path.join(PATH_TO_DATA, 'test_y_hat.npy')  

    PATH_TO_DATA_GE = os.path.join(PATH_TO_DATA, "great_expectations/")
    PATH_TO_DATA_GE_DATASET = os.path.join(PATH_TO_DATA_GE, "estimated_y.csv")

    FULL_TRAIN_Y_TO_CSV = os.path.join(PATH_TO_DATA_GE, NAME_TRAIN_Y_TO_CSV)
    FULL_TRAIN_X_TO_CSV = os.path.join(PATH_TO_DATA_GE, NAME_TRAIN_X_TO_CSV)

update_folders()