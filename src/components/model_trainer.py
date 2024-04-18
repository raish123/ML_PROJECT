#this file we used to train the model and finding out best model for the given dataset 
#and best model file we r storing into artifacts folder

#so importing all the important library which is used in model_training mei!!!
import pandas as pd,numpy as np
from sklearn.linear_model import LinearRegression,Lasso,Ridge
#below class we used to find the accuracy of model
from sklearn.metrics import r2_score,mean_squared_error
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object,evaluate_model
from sklearn.model_selection import GridSearchCV
from dataclasses import dataclass
import sys,os



@dataclass
class ModelTrainerConfig():
    trained_model_path:str = os.path.join('artifacts','model.pkl')




class ModelTrainer():
    #creating constructor method to intialize ModelTrainerConfig class and it will automatically call itself when we create this class object
    def __init__(self):
        self.model_trainer_config_path = ModelTrainerConfig()

    #now starting the model training
    def initiate_model_trainer(self,train_arr,test_arr,preprocessor_path):
        logging.info('initiating the model training process')
        try:
            logging.info('splitting the train and test array into x_train,x_test,y_train,y_test mei')
            x_train,y_train,x_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            logging.info('define all models in dicatonary')

            models = {
                'linear_regression':LinearRegression(),
                'lasso':Lasso(),
                'ridge':Ridge()
            }

            model_report:dict = evaluate_model(x_train,y_train,x_test,y_test,models)


            #to get the best score from model_report dictatonary
            best_score_model = max(sorted(model_report.values()))

            #to get best model name from dicatonary
            best_model_name = list(model_report.keys())[list(model_report.values()).index (best_score_model)]

            best_model = models[best_model_name]

            if best_score_model<=0.6:
                raise CustomException('no best model found')
            
            logging.info('best model found on both training and testing dataset')

            save_object(
                file_path = self.model_trainer_config_path.trained_model_path,
                obj = best_model

            )
            logging.info('saving best model into artifact folder')

            predict = best_model.predict(x_test)

            # Renaming the variable to avoid conflict with the function name
            r2_score_value = r2_score(y_test, predict)

            return r2_score_value

        except Exception as e:
            raise CustomException(e,sys)


