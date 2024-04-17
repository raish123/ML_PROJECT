#these file will read the data from differnt source(like database or cloud storage) and stored raw data into artifact folder 
#then splitting raw data into train,test data in artifacts folder

#so importing all the important libraries which is used in this data_ingestion.py file 
import pandas as pd,numpy as np
from sklearn.model_selection import train_test_split
import os,sys
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass #these class we used to initialize class variable directly by using decorator dataclass
from src.utils import read_data_sql


@dataclass
#creating user defined class in name of data_ingestion_config to store train,test,raw data path in it 
class DataIngestionConfig():
    #now initialize class variable(attribute) as filepath to stored raw,train,test data into artifact folder
    raw_data_path = os.path.join('artifacts','raw_data.csv')
    train_data_path = os.path.join('artifacts','train_data.csv')
    test_data_path = os.path.join('artifacts','test_data.csv')


#creating user defined class to perform data ingestion work
    
class DataIngestion():
    #creating constructor method to initialise  object of DataIngestionConfig class
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()  #will return the path of raw,train,test data in it

    #creating object method to start data_ingestion task in it!!
    def initiate_data_ingestion(self):
        logging.info('Data ingestion started')
        try:
            logging.info('Reading Data from MYSQL Database')
            df = read_data_sql()
            logging.info('Reading completed from database')
            #os.path.dirname will split  the complete path into directory and filename
            #creating artifact directory to stored raw data in it
            os.makedirs(os.path.dirname(self.data_ingestion_config.raw_data_path),exist_ok=True)
            #saving the raw data  into csv format using pandas dataframe object 
            df.to_csv(self.data_ingestion_config.raw_data_path,index=False,header=True)

            #now splitting the raw data(80:20) into train and test data 
            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)

            #saving  the train and test set into artifacts folder
            train_set.to_csv(self.data_ingestion_config.train_data_path,index=False,header=True)

            test_set.to_csv(self.data_ingestion_config.test_data_path,index=False,header=True)

            logging.info('Data ingestion Complted Successfully')

            return (
                self.data_ingestion_config.raw_data_path,
                self.data_ingestion_config.train_data_path,
                self.data_ingestion_config.test_data_path
            )

            
        except Exception as e:
            raise CustomException(e,sys)




