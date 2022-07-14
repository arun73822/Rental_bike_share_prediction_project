from typing import List
from setuptools import setup,find_packages
from rental_bike_share.constants import *

REQUIREMENT_FILE_NAME="requirements.txt"

def get_requirements_list()->List[str]:

    "List the all required packages for project"

    with open(REQUIREMENT_FILE_NAME) as requirements:
        return requirements.readlines().remove("-e .")


setup(name=PROJECT_NAME,version=VERSION,description=DESCRIPTION,AUTHOR=AUTHOR,packages=find_packages(),
      install_requires=get_requirements_list())
