from rental_bike_share.component.data_ingestion import Data_Ingestion
from rental_bike_share.component.data_validation import Data_validation
from rental_bike_share.exception import Rental_bike_share_Exception
from rental_bike_share.logger import logging
from rental_bike_share.config.configuration import Configuration
from rental_bike_share.entity.artifact_entity import (Data_Ingestion_Artifact,Data_Validaton_Artifact,
                                                      Data_Transformation_Artifact,Model_Training_Artifact,
                                                      Model_Evaluation_Artifact,Model_Pusher_Artifact)
import os,sys

class Pipeline:

    def __init__(self,config: Configuration = Configuration()):
        try:
            self.config=config
        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e
    
    def start_data_ingestion(self)->Data_Ingestion_Artifact:
        try:
            data_ingestion=Data_Ingestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e
    
    def start_data_validation(self,data_ingestion_artifact:Data_Ingestion_Artifact)->Data_Validaton_Artifact:
        try:
            data_validation=Data_validation(data_validation_config=self.config.get_data_validation_config(),
                                            data_ingestion_artifact=data_ingestion_artifact)
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e

    def run_pipeline(self):
        try:
            logging.info("run pipeline getting started")
            # data ingestion
            data_ingestion_artifact=self.start_data_ingestion()
            #data validation
            data_validation=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e
