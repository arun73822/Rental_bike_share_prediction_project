from datetime import datetime
import os

# Setup.py file related variables
PROJECT_NAME="Rental_bike_share_prediction"
VERSION="0.0.1"
AUTHOR="Arun Kumar"
DESCRIPTION="This is my first project"

# Logger file related variables
CURRENT_TIME_STAMP=f"{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}"
LOG_DIR="logs"
LOG_FILE_NAME=f"log_{CURRENT_TIME_STAMP}.log"
LOG_FILE_PATH=os.path.join(LOG_DIR,LOG_FILE_NAME)

# some constants
ROOT_DIR= os.getcwd()
CONFIG_DIR='config'
CONFIG_FILE_NAME='config.yaml'
CONFIG_FILE_PATH= os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)

# training pipeline related variables
TRAINING_PIPELINE_CONFIG_KEY='Training_Pipeline_Config'
TRAINING_PIPELINE_NAME='pipeline_name'
TRAINING_PIPELINE_ARTIFACT_DIR='artifact_dir'

# data ingestion config related variables
DATA_INGESTION_CONFIG_KEY='Data_Ingestion_Config'
DATA_INGESTION_ARTIFACT_DIR='data_ingestion'
DATA_INGESTION_DATASET_DOWNLOAD_URL='dataset_download_url'
DATA_INGESTION_ZIP_DATA_DIR='zip_data_dir'
DATA_INGESTION_RAW_DATA_DIR='raw_data_dir'
DATA_INGESTION_INGESTED_DIR='ingested_data_dir'
DATA_INGESTION_TRAIN_DATA_DIR='ingested_train_dir'
DATA_INGESTION_TEST_DATA_DIR='ingested_test_dir'

# data validation config related variables
DATA_VALIDATION_CONFIG_KEY='Data_Validation_Config'
DATA_VALIDATION_ARTIFACT_DIR='data_validation'
DATA_VALIDATION_SCHEMA_DIR='schema_file_dir'
DATA_VALIDATION_SCHEMA_FILE_NAME='schema_file_name'
DATA_VALIDATION_REPORT_FILE_NAME='report_file_name'
DATA_VALIDATION_REPORT_PAGE_NAME='report_page_name'

# data transformation config related variables
DATA_TRANSFORMATION_CONFIG_KEY='Data_Transformation_Config'
DATA_TRANSFORMATION_ARTIFACT_DIR='data_transformation'
DATA_TRANSFORMATION_TRANSFORMED_DIR='transformed_dir'
DATA_TRANSFORMATION_TRAIN_TRANSFORMED_DIR='transformed_train_dir'
DATA_TRANSFORMATION_TEST_TRANSFORMED_DIR='transformed_test_dir'
DATA_TRANSFORMATION_PRE_PROCESSED_OBJ_DIR='pre_processed_object_dir'
DATA_TRANSFORMATION_PRE_PROCESSED_OBJ_FILE='pre_processed_object_file'

# model training related variables
MODEL_TRAINING_CONFIG_KEY='Model_Training_Config'
MODEL_TRAINING_ARTIFACT_DIR='model_training'
MODEL_TRAINING_TRAINED_MODEL_DIR='trained_model_dir'
MODEL_TRAINING_MODEL_FILE_NAME='model_file_name'
MODEL_TRAINING_BASE_ACCURACY='base_accuacy'
MODEL_TRAINING_MODEL_CONFIG_DIR='model_config_dir'
MODEL_TRAINING_MODEL_CONFIG_FILE_NAME='model_config_file_name'

# model evaluation related variables
MODEL_EVALUATION_CONFIG_KEY="Model_Evaluation_Config"
MODEL_EVALUATION_ARTIFACT_DIR='model_evaluation'
MODEL_EVALUATION_MODEL_EVALUATION_FILE_NAME='model_evaluation_file_name'

# model pusher related variables
MODEL_PUSHER_CONFIG_KEY='Model_Pusher_Config'
MODEL_PUSHER_ARTIFACT_DIR='model_pusher'
MODEL_PUSHER_EXPORT_DIR='model_export_dir'
