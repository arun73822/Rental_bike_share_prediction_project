from rental_bike_share.logger import logging
from rental_bike_share.exception import Rental_bike_share_Exception
from rental_bike_share.entity.config_entity import ( Data_Ingestion_Config,Data_Tranformaton_Config,
                                                     Data_Validation_Config,Model_Training_Config,
                                                     Model_Evaluation_Config,Model_Pusher_Config,
                                                     Training_Pipeline_Config)
from rental_bike_share.util.util import read_yaml_file
from rental_bike_share.constants import *
import os,sys

class Configuration:

    def __init__(self,config_file_path:str=CONFIG_FILE_PATH,timestamp:str=CURRENT_TIME_STAMP)->None:
        try:
            self.config_info=read_yaml_file(file_path=config_file_path)
            self.training_pipeline_config=self.get_training_pipeline_config()
            self.timestamp=timestamp
        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e

    def get_data_ingestion_config(self)->Data_Ingestion_Config:
        try:
            logging.info(f"{'>>'*8}data ingestion config started{'>>'*8}")
            artifact_dir=self.training_pipeline_config.artifact_dir

            data_ingestion_config_info=self.config_info[DATA_INGESTION_CONFIG_KEY]

            data_ingestion_artifact=os.path.join(artifact_dir,
                                                 DATA_INGESTION_ARTIFACT_DIR,
                                                 self.timestamp)

            dataset_download_url=data_ingestion_config_info[DATA_INGESTION_DATASET_DOWNLOAD_URL]
            zip_data_dir=os.path.join(data_ingestion_artifact,
                                      data_ingestion_config_info[DATA_INGESTION_ZIP_DATA_DIR])

            raw_data_dir=os.path.join(data_ingestion_artifact,
                                      data_ingestion_config_info[DATA_INGESTION_RAW_DATA_DIR])
            
            ingested_dir=os.path.join(data_ingestion_artifact,
                                      data_ingestion_config_info[DATA_INGESTION_INGESTED_DIR])

            ingested_train_data_dir=os.path.join(data_ingestion_artifact,
                                                 data_ingestion_config_info[DATA_INGESTION_INGESTED_DIR],
                                                 data_ingestion_config_info[DATA_INGESTION_TRAIN_DATA_DIR])

            ingested_test_data_dir=os.path.join(data_ingestion_artifact,
                                                data_ingestion_config_info[DATA_INGESTION_INGESTED_DIR],
                                                data_ingestion_config_info[DATA_INGESTION_TEST_DATA_DIR])

            data_ingestion_config=Data_Ingestion_Config(dataset_download_url=dataset_download_url,
                                                        zip_data_dir=zip_data_dir,
                                                        raw_data_dir=raw_data_dir,
                                                        ingested_dir=ingested_dir,
                                                        ingested_train_data_dir=ingested_train_data_dir,
                                                        ingested_test_data_dir=ingested_test_data_dir)

            logging.info(f"data_ingestion_config : {data_ingestion_config}")
            #logging.info(f"{'>>'*8}data ingestion config successfully completed{'>>'*8}\n\n")

            return data_ingestion_config
        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e

    def get_data_validation_config(self)->Data_Validation_Config:
        try:
            logging.info(f"{'>>'*8}data validation config started{'>>'*8}")
            artifact_dir=self.training_pipeline_config.artifact_dir

            data_validation_config_info=self.config_info[DATA_VALIDATION_CONFIG_KEY]

            data_validation_artifact=os.path.join(artifact_dir,
                                                  DATA_VALIDATION_ARTIFACT_DIR,
                                                  self.timestamp)
            
            schema_file_path=os.path.join(data_validation_artifact,
                                          data_validation_config_info[DATA_VALIDATION_SCHEMA_DIR],
                                          data_validation_config_info[DATA_VALIDATION_SCHEMA_FILE_NAME])
            
            report_file_path=os.path.join(data_validation_artifact,
                                          data_validation_config_info[DATA_VALIDATION_REPORT_FILE_NAME])

            report_page_path=os.path.join(data_validation_artifact,
                                          data_validation_config_info[DATA_VALIDATION_REPORT_PAGE_NAME])

            data_validation_config=Data_Validation_Config(schema_file_path=schema_file_path,
                                                          report_file_path=report_file_path,
                                                          report_page_path=report_page_path)
            
            logging.info(f"data_validation_config : {data_validation_config}")
            logging.info(f"{'>>'*8}data validation config successfully completed{'>>'*8}\n\n")

            return data_validation_config

        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e

    def  get_data_transformation_config(self)->Data_Tranformaton_Config:
        try:
            logging.info(f"{'>>'*8}data transformation config started{'>>'*8}")
            artifact_dir=self.training_pipeline_config.artifact_dir

            data_transformation_config_info=self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]

            data_transformation_artifact=os.path.join(artifact_dir,
                                                      DATA_TRANSFORMATION_ARTIFACT_DIR,
                                                      self.timestamp)

            transformed_train_dir=os.path.join(data_transformation_artifact,
                                    data_transformation_config_info[DATA_TRANSFORMATION_TRANSFORMED_DIR],
                                    data_transformation_config_info[DATA_TRANSFORMATION_TRAIN_TRANSFORMED_DIR])

            transformed_test_dir=os.path.join(data_transformation_artifact,
                                    data_transformation_config_info[DATA_TRANSFORMATION_TRANSFORMED_DIR],
                                    data_transformation_config_info[DATA_TRANSFORMATION_TEST_TRANSFORMED_DIR]) 

            pre_processed_obi_file=os.path.join(data_transformation_artifact,
                                    data_transformation_config_info[DATA_TRANSFORMATION_PRE_PROCESSED_OBJ_DIR],
                                    data_transformation_artifact[DATA_TRANSFORMATION_PRE_PROCESSED_OBJ_FILE])

            data_transformation_config=Data_Tranformaton_Config(transformed_train_dir=transformed_train_dir,
                                                                transformed_test_dir=transformed_test_dir,
                                                                pre_processed_obj_file=pre_processed_obi_file)

            logging.info(f"data_transformation_config : {data_transformation_config}")
            logging.info(f"{'>>'*8}data transformation config successfully completed{'>>'*8}\n\n")

            return data_transformation_config

        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e

    def get_model_training_config(self)->Model_Training_Config:
        try:
            logging.info(f"{'>>'*8}model training config started{'>>'*8}")
            artifact_dir=self.training_pipeline_config.artifact_dir

            model_training_config_info = self.config_info(MODEL_TRAINING_CONFIG_KEY)

            model_training_artifact=os.path.join(artifact_dir,MODEL_TRAINING_ARTIFACT_DIR,self.timestamp)

            model_file_path=os.path.join(model_training_artifact,
                                         model_training_config_info[MODEL_TRAINING_TRAINED_MODEL_DIR],
                                         model_training_config_info[MODEL_TRAINING_MODEL_FILE_NAME])

            base_accuracy=model_training_config_info[MODEL_TRAINING_BASE_ACCURACY]
            
            model_config_file_path=os.path.join(model_training_config_info[MODEL_TRAINING_MODEL_CONFIG_DIR],
                                          model_training_config_info[MODEL_TRAINING_MODEL_CONFIG_FILE_NAME])

            model_training_config=Model_Training_Config(model_file_path=model_file_path,
                                                        base_accuracy=base_accuracy,
                                                        model_config_file_path=model_config_file_path)

            logging.info(f"model_training_config : {model_training_config}")
            logging.info(f"{'>>'*8}model training config successfully completed{'>>'*8}\n\n")

            return model_training_config

        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e

    def get_model_evaluation_config(self)->Model_Evaluation_Config:
        try:
            logging.info(f"{'>>'*8}model evaluation config started{'>>'*8}")
            artifact_dir=self.training_pipeline_config.artifact_dir

            model_evaluation_config_info=self.config_info[MODEL_EVALUATION_CONFIG_KEY]

            model_evaluation_artifact=os.path.join(artifact_dir,
                                                   MODEL_EVALUATION_ARTIFACT_DIR,
                                                   self.timestamp)
            model_evaluation_file_path=os.path.join(model_evaluation_artifact,
            model_evaluation_config_info[MODEL_EVALUATION_MODEL_EVALUATION_FILE_NAME])

            model_evaluation_config=Model_Evaluation_Config(model_evaluation_file_path=model_evaluation_file_path,
                                                            timestamp=self.timestamp)

            logging.info(f"model_evaluation_config : {model_evaluation_config}")
            logging.info(f"{'>>'*8}model evaluation config successfully completed{'>>'*8}\n\n")

            return model_evaluation_config
            
        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e

    def  get_model_pusher_config(self)->Model_Pusher_Config:
        try:
            logging.info(f"{'>>'*8}model pusher config started{'>>'*8}")
            artifact_dir=self.training_pipeline_config.artifact_dir

            model_pusher_config_info=self.config_info[MODEL_PUSHER_CONFIG_KEY]

            model_pusher_artifact=os.path.join(artifact_dir,
                                               MODEL_PUSHER_ARTIFACT_DIR,
                                               self.timestamp)
            export_dir_path=os.path.join(model_pusher_artifact,
                                         model_pusher_config_info[MODEL_PUSHER_EXPORT_DIR])

            model_pusher_config=Model_Pusher_Config(export_dir_path=export_dir_path)

            logging.info(f"model_pusher_config : {model_pusher_config}")
            logging.info(f"{'>>'*8}model pusher config successfully completed{'>>'*8}\n\n")

            return model_pusher_config

        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e

    def get_training_pipeline_config(self)->Training_Pipeline_Config:
        try:
            logging.info(f"{'>>' * 8}training pipeline config started{'>>' * 8}")

            training_pipeline_config_info=self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir=os.path.join(ROOT_DIR,training_pipeline_config_info[TRAINING_PIPELINE_NAME],
                                               training_pipeline_config_info[TRAINING_PIPELINE_ARTIFACT_DIR])

            training_pipeline_config=Training_Pipeline_Config(artifact_dir=artifact_dir)

            logging.info(f"training_pipeline_config : {training_pipeline_config}")
            logging.info(f"{'>>'*8}training pipeline config ended{'>>'*8}")
            return training_pipeline_config
        except Exception as e:
            raise Rental_bike_share_Exception(e,sys) from e
