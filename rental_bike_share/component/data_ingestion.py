from rental_bike_share.logger import logging
from rental_bike_share.exception import Rental_bike_share_Exception
from rental_bike_share.entity.config_entity import Data_Ingestion_Config
from rental_bike_share.entity.artifact_entity import Data_Ingestion_Artifact
from rental_bike_share.config.configuration import Configuration
from sklearn.model_selection import StratifiedShuffleSplit
from six.moves import urllib
from zipfile import ZipFile
import pandas as pd
import numpy as np
import os,sys

class Data_Ingestion:

    def __init__(self,data_ingestion_config:Data_Ingestion_Config):
        try:
            logging.info(f"{'>>'*10}Data Ingestion log started.{'<<'*10}")
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e
    
    def download_the_rental_bike_share_data(self)->str:
        try:
            download_url=self.data_ingestion_config.dataset_download_url

            zip_data_dir=self.data_ingestion_config.zip_data_dir

            if os.path.exists(zip_data_dir):
                os.remove(zip_data_dir)
            
            os.makedirs(zip_data_dir,exist_ok=True)

            rental_bike_share_file_name=os.path.basename(download_url)

            zip_data_file_path=os.path.join(zip_data_dir,rental_bike_share_file_name)
            urllib.request.urlretrieve(download_url,zip_data_file_path)
            logging.info(f"successfully download the data and the data location path is {[ zip_data_file_path ]}")

            return zip_data_file_path

        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e
    
    def extract_zip_file_data(self,zip_data_file_path:str)->str:
        try:
            raw_data_dir=self.data_ingestion_config.raw_data_dir
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok=True)

            logging.info(f"Extracting tgz file: [{zip_data_file_path}] into dir: [{raw_data_dir}]")
            with ZipFile(zip_data_file_path,'r') as zip_file:
                zip_file.extractall(path=raw_data_dir)
                logging.info(f"Successfully extracted the zip file and extracted file location is {[ raw_data_dir ]}")

                return raw_data_dir

        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e
    
    def split_data_as_train_and_test(self,raw_data_dir:str)->Data_Ingestion_Artifact:
        try:
            file_name=os.listdir(raw_data_dir)[1]
            rental_bike_share_file_path=os.path.join(raw_data_dir,file_name)
            rental_bike_share_df=pd.read_csv(rental_bike_share_file_path)

            rental_bike_share_df['humidity_cat']=pd.cut(rental_bike_share_df['hum'],
                                                        bins=[-(np.inf),0.2,0.4,0.6,0.8,1.0],
                                                        labels=[1,2,3,4,5])
            logging.info("splitting started")
            split=StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=34)

            start_train_set = None
            start_test_set = None

            for train_ix,test_ix in split.split(rental_bike_share_df,rental_bike_share_df['humidity_cat']):
                start_train_set = rental_bike_share_df.loc[train_ix].drop(['humidity_cat'],axis=1)
                start_test_set = rental_bike_share_df.loc[test_ix].drop(['humidity_cat'],axis=1)
            
            train_file_path=os.path.join(self.data_ingestion_config.ingested_train_data_dir,file_name)

            test_file_path=os.path.join(self.data_ingestion_config.ingested_test_data_dir,file_name)

            if start_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_data_dir,exist_ok=True)
                start_train_set.to_csv(train_file_path,index=False)
                logging.info(f"Exporting training dataset to file is Successful and path is: [{[ train_file_path ]}]")

            if start_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_data_dir,exist_ok=True)
                start_test_set.to_csv(test_file_path,index=False,)
                logging.info(f"Exporting testing dataset to file is Successful and path is: [{[ test_file_path ]}]")

            data_ingestion_artifact=Data_Ingestion_Artifact(train_file_path=train_file_path,
                                                            test_file_path=test_file_path,
                                                            is_ingested=True,message="Successfully data ingested")

            logging.info(f"data ingestion artifact is:{data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e
    
    def initiate_data_ingestion(self)->Data_Ingestion_Artifact:
        try:
            logging.info('initiated_the_data_ingestion')
            zip_data_file_path=self.download_the_rental_bike_share_data()
            self.extract_zip_file_data(zip_data_file_path=zip_data_file_path)
            return self.split_data_as_train_and_test(raw_data_dir=self.data_ingestion_config.raw_data_dir)
        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e
    
    def __del__(self):
        logging.info(f"{'>>'*10}Data Ingestion log completed.{'<<'*10} \n\n")
