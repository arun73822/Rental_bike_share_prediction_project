from collections import namedtuple

Data_Ingestion_Artifact=namedtuple('Data_Ingestion_Artifact',['train_file_path','test_file_path',
                                   'is_ingested','message'])

Data_Validaton_Artifact=namedtuple('Data_Validaton_Artifact',['schema_file_path','report_file_path',
                                   'report_page_path','is_validated','message'])

Data_Transformation_Artifact=namedtuple('Data_Transformation_Artifact',['transformed_train_file_path',
                                                                        'transformed_test_file_path',
                                                                        'pre_processed_obj_file_path',
                                                                        'is_transformed','message'])

Model_Training_Artifact=namedtuple('Model_Training_Artifact',['trained_model_path','train_accuracy',
                                                              'test_accuracy','train_rmse','test_rmse',
                                                              'model_accuracy','is_trained','message'])

Model_Evaluation_Artifact=namedtuple('Model_Evaluation_Artifact',['eveluated_model_file_path','is_evaluated',
                                                                  'message'])

Model_Pusher_Artifact=namedtuple('Model_Pusher_Artifact',['export_model_file_path','is_model_pushed','message'])
                                               