#these file raise the customException during run time execution of code!
from src.logger import logging
import sys #this library we used to get error_message occur during run time execution of code


def get_error_message(error,error_details:sys):
    _,_,exc_tb = error_details.exc_info()  
    #It returns a tuple containing information about the exception type, the exception value, and the traceback
    filename = exc_tb.tb_frame.f_code.co_filename #get the name of current python file in which error occurred 
    lineno = exc_tb.tb_lineno #get line number where error occurred 

    error_message = f"Error occured in this python script {filename} at the line {lineno} error message will be {str(error)}"

    return error_message





class CustomException(Exception):
    #now creating constructor object of CustomException class
    def __init__(self, error,error_details:sys):
        #calling parent class constructor i.e., Exception class constructor to get error occured during exception
        super().__init__(error)

        #whaterver error we r getting from parent class exception we r passing parameter to the function
        self.error = get_error_message(error,error_details  = error_details)



    #__str__ is special method  in python which returns string representation of an object
    def __str__(self):
       return f"Custom Exception Occured : {self.error}"
    



if __name__ == '__main__':
    try:
        a=1/0

    except Exception as e:
        logging.info(e)
        raise CustomException(e,sys)