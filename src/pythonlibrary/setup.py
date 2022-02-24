from setuptools import find_packages, setup

setup(
    name='namepythonlib',
    packages=find_packages(include=['namepythonlib']),
    version='0.1.0',
    description='Template of Python library',
    author='Dr. Cesar Guzman',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.5'],
    test_suite='tests',
)