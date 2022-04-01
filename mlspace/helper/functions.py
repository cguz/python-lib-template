# import libraries
import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter


# used in the create_dataset and train_model.ipynb
file_name = 'mars-express-power-3years'
folder = '../data'
PATH_TO_DATA = folder + "/" + file_name + "/"

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



# Function to plot the data
def plot_features(X):    
    """
    Plot the features

    :param X set of features 
    """
    f, ax = plt.subplots(1,1,figsize=(18,4))
    boxplot = X.boxplot(ax=ax)
    plt.xticks(rotation=90)
    plt.title('Features')


def gen_histogram(dataset, draw, bins = ''):
    """
    Generate from an array:
     - the histogram
     - bins: range or placement on the number line
     - ppf: percent point function
     - cdf: cumulative distribution function. Not yet used.

    :param dataset set of values to calculate the hist and bins
    :param draw true value that indicates if we draw the histogram
    :param bins specify the bins
    :return the histogram, the bins, percent point function and cumulative distribution function
    """
    if bins == '':
        hist, bins = np.histogram(dataset)
    else:
        hist, bins = np.histogram(dataset, bins)

    ppf = hist / sum(hist)

    cdf = np.cumsum(ppf)

    # printing histogram
    print()
    print("H:", hist) 
    print("ppf:", ppf) 
    print("bins:", bins) 

    if draw:
        # Creating plot
        fig = plt.figure(figsize =(10, 7))
        
        plt.hist(dataset, bins) #, weights=[1/len(dataset)] *len(dataset)) 

        # plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
        
        plt.title("Numpy Histogram") 

        # plotting PPF and CDF
        plt.plot(bins[1:], ppf, color="red", label="PPF")
        # plt.plot(bins[1:], cdf, label="CDF")
        plt.legend()
        
        # show plot
        plt.show()
    
    return hist, bins, ppf, cdf

def get_indices_with_wrong_range(x, y, percentage=False):
    """
    Calculating indices with wrong range against the expected histogram
    
    :param x: set of expected values
    :param y: set of current valiues

    :return
      - index subset
      - for each index the remain amount of value (in percentage) to reach the expected histogram
    """

    diff = x - y
    index_subset = np.where(diff < 0)

    if percentage: 
        return index_subset, diff[index_subset]*-100
    else:
        return index_subset, diff[index_subset]

def remove_labels(g, label):
    """
    remove labels from the gremmlin graph
    
    :param g: gremlin graph
    :param label: name of the label
    """
    for f in g.V().hasLabel(label).toList():
        print(g.V(f.id).values("Name").next())
        g.V(f.id).drop().iterate()

def print_labels(g, label):
    """
    print labels from the gremmlin graph
    
    :param g: gremlin graph
    :param label: name of the label
    """
    for f in g.V().hasLabel(label).toList():
        print(g.V(f.id).values("Name").next())

def print_requirement(g, id, name):
    """
    print the related expectations to a given Feature Name with the arguments
    
    :param g: gremlin graph
    :param id: id of the node in graph
    :param label: name of the label
    """
    # Feature hasA Expectation(Name=name) that contains Arguments
    search = g.V(id).outE("hasA").inV().has("Name", name).outE("contains").inV().toList()

    print("Requirement: ", name)

    for i in search:
        print(g.V(i).values("Name").next(), g.V(i).values("Value").next())

def RMSE(val, pred) -> float:
    """
    metric Root Mean Square Error
    
    :param val: original values
    :param pred: predicted values
    """
    diff = (val - pred) ** 2
    rmse = np.mean(diff) ** 0.5
    return rmse