from cmath import e
from tkinter import E
from rental_bike_share.constants import NUMERICAL_COLUMNS
from rental_bike_share.exception import Rental_bike_share_Exception
from rental_bike_share.logger import logging
from rental_bike_share.config.configuration import Configuration
from rental_bike_share.entity.config_entity import Data_Validation_Config
from rental_bike_share.entity.artifact_entity import Data_Ingestion_Artifact,Data_Validaton_Artifact
from rental_bike_share.util.util import read_yaml_file,load_json_data
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import pandas as pd
import json
import os,sys

class Data_validation:

    def __init__(self,data_validation_config:Data_Validation_Config,
                 data_ingestion_artifact:Data_Ingestion_Artifact):
        try:
            logging.info(f"{'<<'*8}data validation log started{'<<'*8}")
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e
    
    def is_train_test_df_exits(self)->bool:
        try:
            logging.info(f"{'<<'*8}checking the train,test dataframe are available are not{'<<'*8}")
            train_test_df_exits=False

            train_df_path=self.data_ingestion_artifact.train_file_path
            test_df_path=self.data_ingestion_artifact.test_file_path
            
            if os.path.exists(train_df_path):
                train_df_exits=True

            if os.path.exists(test_df_path):
                test_df_exits=True

            train_test_df_exits= train_df_exits and test_df_exits

            if train_test_df_exits==False:
                error_message=f"""please check the train file is {[train_df_path]} or 
                                  test file is {[test_df_path]} is not avaible"""
                raise Exception(error_message)

            logging.info(f"{'<<'*8}train and test dataframe are exits is {[ train_test_df_exits ]}{'<<'*8}")
            return train_test_df_exits
        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e

    def get_train_test_df(self):
        try:
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            logging.info("Successfully getting the train and test dataframe")
            return train_df,test_df
        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e
    
    def validate_the_dataset_schema(self)->bool:
        try:
            validation_status=False
            # checking the number of columns
            train_df,test_df=self.get_train_test_df()
            schema_file_path=self.data_validation_config.schema_file_path
            schema_file_info=read_yaml_file(file_path=schema_file_path)
            schema_file_columns=schema_file_info[NUMERICAL_COLUMNS]

            train_df_number_of_columns=False
            test_df_number_of_columns=False

            if len(train_df.columns)== len(schema_file_columns):
                train_df_number_of_columns=True

            if train_df_number_of_columns==False:
                error_message=f"""please check the number of columns in train dataframe,schema file columns.
                In the train dataframe number of columns are {[ len(train_df.columns) ]} are not equal to
                in schema file columns are {[ len(schema_file_columns) ]}"""
                raise Exception(error_message)
            logging.info(f"Number of columns in train dataframe and schema file are same is? {train_df_number_of_columns}")

            if len(test_df.columns)== len(schema_file_columns):
                test_df_number_of_columns=True
        
            if test_df_number_of_columns==False:
                error_message=f"""please check the number of columns in test dataframe,schema file columns.
                In the test dataframe number of columns are {[ len(test_df.columns) ]} are not equal to
                in schema file columns are {[ len(schema_file_columns) ]}"""
                raise Exception(error_message)
            logging.info(f"Number of columns in test dataframe and schema file are same is? {test_df_number_of_columns}")

            train_columns_names=False
            test_columns_names=False
            
            # checking the columns names
            if list(train_df.columns)==schema_file_columns:
                train_columns_names=True
            
            if train_columns_names==False:
                error_message=f"""please check the columns in train dataframe,schema file columns.
                In the train dataframe number of columns are {[ (train_df.columns) ]} are not equal to
                in schema file columns are {[ (schema_file_columns) ]}"""
                raise Exception(error_message)
            logging.info(f"The columns names in train dataframe and schema file are same is? {train_columns_names}")

            if list(test_df.columns)==schema_file_columns:
                test_columns_names=True
            
            if test_columns_names==False:
                error_message=f"""please check the columns in test dataframe,schema file columns.
                In the test dataframe number of columns are {[ (test_df.columns) ]} are not equal to
                in schema file columns are {[ (schema_file_columns) ]}"""
                raise Exception(error_message)
            logging.info(f"The columns names in test dataframe and schema file are same is? {test_columns_names}")

            validation_status= train_df_number_of_columns and train_columns_names and test_df_number_of_columns and test_columns_names
            logging.info(f"schema file validation status is?{validation_status}")
            return validation_status
        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e

    def get_and_save_drift_report_file(self)->dict:
        try:
            logging.info('generating the drift report file started')
            profile=Profile(sections=[DataDriftProfileSection()])
            train_df,test_df=self.get_train_test_df()
            profile.calculate(train_df,test_df)
            report=json.loads(profile.json())
            
            report_file_path=self.data_validation_config.report_file_path
            report_dir=os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)
            logging.info(f"Successfully generated the drift report file and saving the drift report file is started")
            load_json_data(file_path=report_file_path,data=report)
            """
            with open(report_file_path,'w') as report_file:
                json.dump(report,report_file,indent=6)
            """
            logging.info(f"Successfully saved the drift report file and path is {[ report_file_path ]}")
            return report
        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e
    
    def get_and_save_drift_report_page(self):
        try:
            logging.info('generating the drift report page started')
            dashboard=Dashboard(tabs=[DataDriftTab()])
            train_df,test_df=self.get_train_test_df()
            dashboard.calculate(train_df,test_df)

            report_page_file_path=self.data_validation_config.report_page_path
            report_page_dir=os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)
            logging.info(f"Successfully generated the drift report page and saving the drift report page is started")
            dashboard.save(report_page_file_path)
            logging.info(f"Successfully saved the drift report page and path is {[ report_page_file_path ]}")
        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e

    def is_drift_found(self):
        try:
            report=self.get_and_save_drift_report_file()
            self.get_and_save_drift_report_page()
            return True
        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e
    
    def initiate_data_validation(self)->Data_Validaton_Artifact:
        try:
            self.is_train_test_df_exits()
            self.validate_the_dataset_schema()
            self.is_drift_found()
            data_validation_artifact=Data_Validaton_Artifact(
                             schema_file_path=self.data_validation_config.schema_file_path,
                             report_file_path=self.data_validation_config.report_file_path,
                             report_page_path=self.data_validation_config.report_page_path,
                             is_validated=True,
                             message="Successfully data validation completed")
            logging.info(f"data_validation_artifact is {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e
    
    def __del__(self):
        logging.info(f"{'>>'*10}Data validation log completed.{'<<'*10} \n\n")
