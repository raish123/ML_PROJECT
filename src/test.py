from src.utils import read_data_sql
import pandas as pd,numpy as np
from sklearn.model_selection import train_test_split
import os,sys
from src.logger import logging
from src.exception import CustomException
from src.utils import read_data_sql
from src.components.data_ingestion import  DataIngestion,DataIngestionConfig

def main():
    # Call the read_data_sql function to load the DataFrame
    #df = read_data_sql()

    #creating an object of DataIngestion class
    di = DataIngestion()
    di.initiate_data_ingestion()
    
    # Print the DataFrame to check if it loaded correctly
    #print(df)

if __name__ == "__main__":
    main()