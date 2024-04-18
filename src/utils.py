#in utils.py file we r writing code in a such way that it provide functionality to our  entire application
from src.logger import logging
from src.exception import CustomException
import pymysql
import pandas as pd
from dotenv import load_dotenv
import os,sys
import dill
from sklearn.metrics import r2_score,mean_squared_error







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
    


def evaluate_model(x_train,y_train,x_test,y_test,models):
    try:
        report={}
        for i in range(len(list(models))):
                model = list(models.values())[i]
                
                #now training the model by 80% of train data
                model.fit(x_train,y_train)
                
                print(list(models.keys())[i])
                #predicting the output
                
                #now training the model by 80% of train_data and predicting the output variable
                y_train_pred = model.predict(x_train)
                #now testing the model by 20% of data and predicting the output variable
                y_test_pred = model.predict(x_test)
                
                #finding the accuracy of training and testing score
                training_score_model = model.score(x_train,y_train)
                testing_score_model = model.score(x_test,y_test)

                report[list(models.keys())[i]] = testing_score_model

                return report
                
               
        
        
    except Exception as e:
        raise CustomException(e,sys)