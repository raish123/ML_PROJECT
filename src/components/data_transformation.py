#in this file we r converting object to numeric using pipelines and column tansformation
#and doing scaling to the input variable and concatenating  them with target variable.

#importing all the important module which is used in data_transformation
import pandas as pd,numpy as np
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from sklearn.impute import SimpleImputer #this class we used to fill null value by mean/median/mode
from sklearn.pipeline import Pipeline #this class will create chain of steps in sequential form so that first step of output used as 2nd step of input 
from sklearn.compose import ColumnTransformer #this class will combine all the pipe_line in sequential manner
from src.exception import CustomException
from src.logger import logging
from sklearn.preprocessing import StandardScaler
from src.components.data_ingestion import  DataIngestion
from dataclasses import dataclass
import os,sys
from sklearn.base import BaseEstimator, TransformerMixin
from src.utils import save_object




#step1: first initializing the preprocessor.pkl file and storing those file to artifacts folder
@dataclass
class DataTransformationConfig():
    preprocessor_obj_filepath:str = os.path.join('artifacts','preprocessor.pkl')


class MultiColumnLabelEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        x_encoded = np.empty(x.shape, dtype=object)
        for i in range(x.shape[1]):
            le = LabelEncoder()
            x_encoded[:, i] = le.fit_transform(x[:, i])
        return x_encoded


#now transforming the train,test_df changing object to numeric ---then doing scaling to input variable
class DataTransformation():
    #now creating constructor method to initilalize DataTransformationConfig class and it will automatically call itself when we create this class object
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_obj(self):
        logging.info('Data transformation initiating')
        try:
            di = DataIngestion()
            raw_path,train_path,test_path = di.initiate_data_ingestion()

            raw_df = pd.read_csv(raw_path)

            target = 'math_score'

            #selecting input and output variable
            x = raw_df.drop(target,axis=1)
            y = raw_df[target]

            #getting numerical_features_column and categorical_features_column

            logging.info('getting numeric and categorical feature from df object')

            numerical_features = x.select_dtypes(exclude = 'object').columns.to_list()
            categorical_features = x.select_dtypes(include = 'object').columns.to_list()

            logging.info('creating pipeline to perform task sequentially')

            #now creating numeric pipelines
            numeric_pipeline = Pipeline(steps=[
                ('imputer',SimpleImputer(strategy='median')), #filling null by median
                ('scaling',StandardScaler(with_mean=False))])   #standardising the features

            #now creating categorical pipelines
            categorical_pipeline = Pipeline(steps=[
                ('imputer',SimpleImputer(strategy= 'most_frequent')), #for missing value we are filling it with most frequent element in
                ('labeling',MultiColumnLabelEncoder()), #converting label into numbers
                ('scaling',StandardScaler(with_mean=False))
            
            ])

            logging.info('Pipeline created Successfully')

            #now combining both pipe line by using columntransformer
            preprocessor = ColumnTransformer(transformers=[
                ('numerical',numeric_pipeline,numerical_features),
                ('categorical',categorical_pipeline,categorical_features)
            ])


            return preprocessor


        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,raw_path,train_path,test_path): #getting from dataingestion file 
        '''in this method we select input and out variable from train and test path
        and converting object to numeric and doing scaling using preprocessor object
        then creating preprocessor object pickle file
        final creating train_array and test_array file
        '''
        logging.info('initiating data  transformation process')
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('read the csv file successfully')

            logging.info('obtaining preprocessor object')

            preprocessing_obj = self.get_data_transformer_obj()

            #selecting input and output variable
            target = 'math_score'

            logging.info('selecting input and output variable from both train and test df object')
            input_feature_train_df = train_df.drop(target,axis=1)
            target_feature_train_df = train_df[target]

            input_feature_test_df = test_df.drop(target,axis=1)
            target_feature_test_df = test_df[target]
            logging.info('successfully selected input and output variable from both train and test df object')

            logging.info('applying preprocessing object to train and test df object')

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            logging.info('preprocessing  is done for both training and testing set')

            #now preparing test_arry df object and train_array df object by using np.c_[] function
            #used to concatinate two array horizontally
            logging.info('Preparing train and test array dataset')

            train_array = np.c_[input_feature_train_arr,np.array(target_feature_train_df)]

            test_array =  np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            logging.info('saving the preprocessor object')

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_filepath,
                obj = preprocessing_obj
            )


            return (
                train_array,
                test_array,
                self.data_transformation_config.preprocessor_obj_filepath
            )

        except Exception as e:
            raise CustomException(e,sys)


    
