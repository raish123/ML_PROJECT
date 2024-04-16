#logger.py file used to log the program activities files
#logging module we used to track down the error or exception occur during  the execution of the code and stored those
#.txt file into some specific folder


import logging
import os
from datetime import datetime


#creating a specific folder to stored the logs files

folder = 'LOGS'
if not os.path.exists(folder):
    os.makedirs(folder,exist_ok=True)



logs_filename = f"LOGS-{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"

path_log_filname = os.path.join(folder,logs_filename)

#creating an object of basicConfig class of logging module

logging.basicConfig(
    filename = path_log_filname,
    filemode='w',
    datefmt='%(asctime)s - %(levelname)s -%(lineno)d- %(message)s',  # Log message format
    level=logging.INFO              # Logging level threshold
)



    