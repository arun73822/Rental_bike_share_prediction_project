from rental_bike_share.exception import Rental_bike_share_Exception
import yaml
import sys,os

def read_yaml_file(file_path:str)->dict:

    """ description: read the Yaml file content
        file_path: str
    ============================================
    retun : dictionary"""
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise Rental_bike_share_Exception(e,sys) from e

def write_yaml_file(file_path:str,data:None):

    """description: Creates the yaml file
       file_path: str
       data: dict"""
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as yaml_file:
            if data is None:
                yaml.dump(data,yaml_file)
    except Exception as e:
        raise Rental_bike_share_Exception(e,sys) from e
