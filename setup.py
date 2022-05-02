from setuptools import find_packages, setup

setup(
    name='mlspace',
    packages=find_packages(include=['mlspace', 'mlspace.*']),
    version='0.1.0',
    description='MlSpaceOps - Python library',
    author='Dr. Cesar Guzman',
    license='MIT',
    install_requires=[ ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.5'],
    test_suite='tests',
)