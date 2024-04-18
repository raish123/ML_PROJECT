import os,sys
from src.logger import logging
from src.exception import CustomException
from src.components.data_ingestion import  DataIngestion,DataIngestionConfig
from src.components.data_transformation import  DataTransformation,DataTransformationConfig
from src.components.model_trainer import  ModelTrainer,ModelTrainerConfig

def main():
    # Call the read_data_sql function to load the DataFrame
    #df = read_data_sql()

    #creating an object of DataIngestion class
    di = DataIngestion()
    raw_path,train_path,test_path = di.initiate_data_ingestion()

    #creating an object data transformation
    dt = DataTransformation()
    train_arr,test_arr,processor_path = dt.initiate_data_transformation(raw_path,train_path,test_path)
    

    mt = ModelTrainer()
    s = mt.initiate_model_trainer(train_arr,test_arr,processor_path)
    print(s)

    # Print the DataFrame to check if it loaded correctly
    #print(df)

if __name__ == "__main__":
    main()
