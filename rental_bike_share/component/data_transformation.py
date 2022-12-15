from housing.logger import logging
from housing.exception import Housing_Exception
from housing.entity.config_entity import Data_Transformation_Config
from housing.entity.artifact_entity import (Data_Ingestion_Artifact,Data_Validation_Artifact,
                                            Data_Transformation_Artifact)
from housing.util.util import read_yaml_file,load_data,save_numpy_array_data,save_object
from housing.constants import *
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
import numpy as np
import os,sys


class Feature_Generator(BaseEstimator,TransformerMixin):

   def __init__(self,add_bedroom_per_room=True,total_rooms_ix=3,population_ix=5,households_ix=6,
                     total_bedrooms_ix=4,columns=None):
                     try:
                        self.add_bedroom_per_room=add_bedroom_per_room
                        self.total_rooms_ix=total_rooms_ix
                        self.population_ix=population_ix
                        self.households_ix=households_ix
                        self.total_bedrooms_ix=total_bedrooms_ix
                        self.columns=columns

                        if self.columns is not None:
                           self.total_rooms_ix=self.columns.index(COLUMN_TOTAL_ROOMS)
                           self.population_ix=self.columns.index(COLUMN_POPULATION)
                           self.households_ix=self.columns.index(COLUMN_HOUSEHOLDS)
                           self.total_bedrooms_ix=self.columns.index(COLUMN_TOTAL_BEDROOMS)
                     except Exception as e:
                        raise Housing_Exception(e,sys) from e
   
   def fit(self,X,y=None):
      return self

   def transform(self,X,y=None):
      try:
         rooms_per_household= X[:,self.total_rooms_ix] / X[:,self.households_ix]

         poulation_per_household= X[:,self.population_ix] / X[:,self.households_ix]

         if self.add_bedroom_per_room:
            bedrooms_per_room= X[:,self.total_bedrooms_ix] / X[:,self.total_rooms_ix]
            generated_featues= np.c_[X,rooms_per_household,poulation_per_household,bedrooms_per_room]
         else:
            generated_featues= np.c_[X,rooms_per_household,poulation_per_household]
         return generated_featues
      except Exception as e:
         raise Housing_Exception(e,sys) from e
        
class Data_Transformation:

   def __init__(self,data_transformation_config:Data_Transformation_Config,
                 data_ingestion_artifact:Data_Ingestion_Artifact,
                 data_validaton_artifact:Data_Validation_Artifact):
                 try:
                  logging.info(f"{'=' * 20}Data Transformation log started.{'=' * 20} ")
                  self.data_tranformation_config = data_transformation_config
                  self.data_ingestion_artifact = data_ingestion_artifact
                  self.data_validation_artifact = data_validaton_artifact
                 except Exception as e:
                    raise Housing_Exception(e,sys) from e

   def get_data_transformer_object(self)->ColumnTransformer:
      try:
         schema_file_path=self.data_validation_artifact.schema_file_path

         schema_dataset=read_yaml_file(file_path=schema_file_path)
         
         numerical_columns=schema_dataset[NUMERICAL_COLUMNS_KEY]
         categorical_columns=schema_dataset[CATEGORICAL_COLUMNS_KEY]

         numerical_pipeline=Pipeline(steps=[('imputer',SimpleImputer(strategy='median')),
                                            ('feature_geneator',Feature_Generator(
                                             add_bedroom_per_room=self.data_tranformation_config.add_bedroom_per_room,
                                             columns=numerical_columns)),
                                             ('scalar',StandardScaler())])

         categorical_pipeline=Pipeline(steps=[('imputer',SimpleImputer(strategy="most_frequent")),
                                              ('one_hot_encoder',OneHotEncoder()),
                                              ('scalar',StandardScaler(with_mean=False))])
         
         logging.info(f"Categorical columns: {categorical_columns}")
         logging.info(f"Numerical columns: {numerical_columns}")

         pre_processing=ColumnTransformer([('numerical_pipeline',numerical_pipeline,numerical_columns),
                                       ('categorical_pipelinete',categorical_pipeline,categorical_columns),])
         
         return pre_processing
      except Exception as e:
         raise Housing_Exception(e,sys) from e

   def initiate_data_transformation(self)->Data_Transformation_Artifact:
      try:
         logging.info(f"Obtaining pre_processing object.")
         pre_processing_object=self.get_data_transformer_object()

         logging.info(f"Obtaining training and test file path.")
         training_file_path=self.data_ingestion_artifact.train_file_path
         test_file_path=self.data_ingestion_artifact.test_file_path

         schema_file_path=self.data_validation_artifact.schema_file_path

         logging.info(f"Loading training and test data as pandas dataframe.")
         train_df=load_data(file_path=training_file_path,schema_file_path=schema_file_path)
         test_df=load_data(file_path=test_file_path,schema_file_path=schema_file_path)

         schema_data=read_yaml_file(file_path=schema_file_path)
         target_column=schema_data[TARGET_COLUMN_KEY]

         logging.info(f"Splitting input and target feature from training and testing dataframe.")
         input_features_train_df=train_df.drop(columns=[target_column],axis=1)
         target_faeture_tarin_df=train_df[target_column]

         input_features_test_df=test_df.drop(columns=[target_column],axis=1)
         target_faeture_test_df=test_df[target_column]

         logging.info(f"Applying preprocessing object on training dataframe and testing dataframe")
         input_features_train_array=pre_processing_object.fit_transform(input_features_train_df)
         input_features_test_array=pre_processing_object.transform(input_features_test_df)

         train_array= np.c_[input_features_train_array,np.array(target_faeture_tarin_df)]
         test_array= np.c_[input_features_test_array,np.array(target_faeture_test_df)]

         tranformed_train_dir=self.data_tranformation_config.transformed_train_dir
         tranformed_test_dir=self.data_tranformation_config.transformed_test_dir

         train_file_name=os.path.basename(training_file_path).replace(".csv",".npz")
         test_file_name=os.path.basename(test_file_path).replace(".csv",".npz")

         tranformed_train_file_path=os.path.join(tranformed_train_dir,train_file_name)
         tranformed_test_file_path=os.path.join(tranformed_test_dir,test_file_name)

         logging.info(f"Saving transformed training and testing array.")
         save_numpy_array_data(file_path=tranformed_train_file_path,array=train_array)
         save_numpy_array_data(file_path=tranformed_test_file_path,array=test_array)
         
         pre_processed_object_file_path=self.data_tranformation_config.preprocessed_object_file_path

         logging.info(f"Saving preprocessing object.")
         save_object(file_path=pre_processed_object_file_path,object=pre_processing_object)

         data_transformation_artifact=Data_Transformation_Artifact(
            transformed_train_file_path=tranformed_train_file_path,
            transformed_test_file_path=tranformed_test_file_path,
            pre_processed_object_file_path=pre_processed_object_file_path,
            is_transformed=True,
            message="Data Transformation is Successfull")

         logging.info(f"Data transformationa artifact: {data_transformation_artifact}")

         return data_transformation_artifact
      except Exception as e:
         raise Housing_Exception(e,sys) from e
   
   def __del__(self):
        logging.info(f"{'='*20}Data Transformation log completed.{'='*20} \n\n")
