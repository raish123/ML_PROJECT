#in utils.py file we r writing code in a such way that it provide functionality to our  entire application
from src.logger import logging
from src.exception import CustomException
import pymysql
import pandas as pd
from dotenv import load_dotenv
import os,sys
import dill
load_dotenv()  # take environment variables from .env.

host = os.getenv('host')
password = os.getenv('password')
user = os.getenv("user")
db = os.getenv('db')
port = int(os.getenv('port'))


def read_data_sql():
    logging.info('Reading The Data From MYSQL')
    try:
        logging.info('making connecting with database')

        connection = pymysql.connect(
            host = host,
            password=password,
            user=user,
            database=db,
            port = port
        )
        logging.info('Database Connected Successfully',connection)

        df = pd.read_sql_query('select * from college',connection)

        return df

    except Exception as e:
        raise CustomException(e,sys)
    


def save_object(file_path,obj):
    try:
        logging.info('saving the filepath into artifacts folder')
        if not os.path.exists('artifacts'):
            os.makedirs('artifacts',exist_ok=True)

        with open(file_path,'wb') as f:
            dill.dump(obj,f)
    except Exception as e:
        raise CustomException(e,sys)