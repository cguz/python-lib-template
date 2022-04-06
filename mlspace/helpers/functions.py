# import libraries
import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter

import nest_asyncio
nest_asyncio.apply()

from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

import mlspace.helpers.configuration as configuration

# create remote connection on the graph database using Gremlin
graph = Graph()
g = graph.traversal().withRemote(DriverRemoteConnection(configuration.CONFIG_CONNECTION, 'g'))

# Function to plot the data
def plot_features(X):    
    """
    Plot the features

    Parameters
    ----------
    X : set of features 
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

    Parameters
    ----------
    dataset : set of values to calculate the hist and bins
    draw : bool
        true value that indicates if we draw the histogram
    bins : specify the bins
    
    Returns
    ----------
    tuple
        - the histogram, 
        - the bins, 
        - percent point function and 
        - cumulative distribution function
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
    
    Parameters
    ----------
    x: real numbers
        set of expected values
    y: real numbers
        set of current valiues

    Return
    ----------
    tuple
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
    
    Parameters
    ----------
    g: gremlin graph
    label: str
        name of the label
    """
    for f in g.V().hasLabel(label).toList():
        print(g.V(f.id).values("Name").next())
        g.V(f.id).drop().iterate()

def print_labels(g, label):
    """
    print labels from the gremmlin graph
    
    Parameters
    ----------
    g: gremlin graph
    label: str
        name of the label
    """
    for f in g.V().hasLabel(label).toList():
        print(g.V(f.id).values("Name").next())

def print_requirement(g, id, name):
    """
    print the related expectations to a given Feature Name with the arguments
    
    Parameters
    ----------
    g: gremlin graph
    id: int
        id of the node in graph
    label: str
        name of the label
    """
    # Feature hasA Expectation(Name=name) that contains Arguments
    search = g.V(id).outE("hasA").inV().has("Name", name).outE("contains").inV().toList()

    print("Requirement: ", name)

    for i in search:
        print(g.V(i).values("Name").next(), g.V(i).values("Value").next())

def RMSE(val, pred) -> float:
    """
    metric Root Mean Square Error
    
    Parameters
    ----------
    val : real number
        original values
    pred : real number
        predicted values

    Return 
    ----------
    float
        root mean square error
    """
    diff = (val - pred) ** 2
    rmse = np.mean(diff) ** 0.5
    return rmse