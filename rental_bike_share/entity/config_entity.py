from collections import namedtuple

Data_Ingestion_Config=namedtuple('Data_Ingestion_Config',['dataset_download_url',
                                         'zip_data_dir','raw_data_dir','ingested_dir','ingested_train_data_dir',
                                         'ingested_test_data_dir'])

Data_Validation_Config=namedtuple('Data_Validation_Config',['schema_file_path','report_file_path',
                                                            'report_page_path'])

Data_Tranformaton_Config=namedtuple('Data_Tranformaton_Config',['transformed_train_dir','transformed_test_dir',
                                                                'pre_processed_obj_file'])

Model_Training_Config=namedtuple('Model_Training_Config',['model_file_path','base_accuracy','model_config_file_path'])

Model_Evaluation_Config=namedtuple('Model_Evaluation_Config',['model_evaluation_file_path','timestamp'])

Model_Pusher_Config=namedtuple('Model_Pusher_Config',['export_dir_path'])

Training_Pipeline_Config=namedtuple('Training_Pipeline_Config',['artifact_dir'])
