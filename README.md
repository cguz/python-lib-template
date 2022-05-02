# MLSpaceOps - Python Library

## Requirements

Python 3.8 or higher with the "liblzma-dev" package installed.

    > root$ apt install python3-pip 

    > python3 -m ensurepip

    > pip3.8 install -r requirements.txt

Running the Gremlin database. Internally we execute:

    kubectl port-forward deployment/dims-deployment 8080:8080 8182:8182 -n offops

## Run tests

    > python setup.py pytest

## Build the library

    > python setup.py bdist

our wheel file is stored in the “dist” folder. 

## Install library

    > pip install dist/mlspace-{VERSION}-py3-none-any.whl

    For instance, VERSION can be 0.1.0

    If it does not work, we can install it directly from the current directory:

    > pip install .

## Use 

Once it is installed, we can import it using:

    import mlspace
    from mlspace import myfunctions

## Document code

- [] quality_gate
- [] requirement
- [] fill_gap_techniques
- [] features
- [] expected_distribution
- [] algorithms

