#these setup.py file we used to create our project as package !!
#so importing all the important library used to create setup file

from setuptools import setup,find_packages
from typing import List

def get_requirements(filepath:str)->list[str]:
    requirements = []
    #now opening the requirements.txt file
    with open(filepath) as f:
        rows = f.read().split('\n')

        for row in rows:
            if '-e .' in row:
                continue
            else:
                requirements.append(row)

    return requirements
    




#creating an object of setup class of setuptool library
setup(
    name= "Student Performance Prediction ML Project",
    version='0.0.1',
    long_description = open('README.md').read(),
    author="Raees Azam Shaikh",
    author_email='shaikhraishazam@gmail.com',
    url = 'https://github.com/raish123/ML_PROJECT/',
    packages=find_packages(),
    install_requirements = get_requirements('requirements.txt')

)
