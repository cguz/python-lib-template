# Template to create a library in Python

The source code is in the folder "src/pythonlibrary/".

## Requirements

- pip install wheel setuptools

## Run tests

Go to the folder "src/pythonlibrary/", and execute:

    > python setup.py pytest

## Build the library

    > python setup.py bdist

our wheel file is stored in the “dist” folder. 

## Install library

    > pip install dist/namepythonlib-0.1.0-py3-none-any.whl

## Use 

Once it is installed, we can import it using:

    import namepythonlib
    from namepythonlib import myfunctions