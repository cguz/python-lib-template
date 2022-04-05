# MLSpaceOps - Python Library

## Requirements

Python 3.8 or higher with the "liblzma-dev" package installed.

    > root$ apt install python3-pip 

    > python3 -m ensurepip

    > pip3 install -r requirements.txt

## Run tests

    > python setup.py pytest

## Build the library

    > python setup.py bdist

our wheel file is stored in the “dist” folder. 

## Install library

    > pip install dist/mlspace-{VERSION}-py3-none-any.whl

    For instance, VERSION can be 0.1.0

## Use 

Once it is installed, we can import it using:

    import mlspace
    from mlspace import myfunctions