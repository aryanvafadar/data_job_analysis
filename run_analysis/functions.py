import config
import psycopg
import pandas as pd
import numpy as np

from typing import Dict

# Function to convert each 1 sql query to a pandas dataframe.
def sql_query_to_dataframe(file_1: str, db_params: set) -> pd.DataFrame:
    try:
        # Connect to our postgres database
        with psycopg.connect(**db_params) as connection:
            
            # Read sql file
            with open(file=file_1, mode='r') as file:
                
                sql_file = file.read()
                
                frame = pd.read_sql_query(sql=sql_file, con=connection)
                
                config.logging.info(f"Successfully created pandas dataframe from sql file {file_1}")
                
                return frame
            
    except Exception as e:
        config.logging.error(f"Unable to create DataFrame from SQL query. Received error {e}")






#TODO: FIX THIS FUNCTION. IT DOES NOT WORK
# Function to convert a dict / list of SQL files into individual pandas dataframe
def multiple_sql_queries_to_dataframe(sql_files: list, db_params: set) -> Dict[int, pd.DataFrame]:
    
    frames = {} # empty dictionary where our frames will go into
    
    try:
        
        # Validate user input for sql files
        if not isinstance(sql_files, list):
            config.logging.error("sql_files must be a dictionary or a list of file paths.")
            raise TypeError("sql_files must be a dictionary or a list of file paths.")
        
        # Validate user input for db_params
        if not isinstance(db_params, set):
            config.logging.error("db_params must be a set of database parameters.")
            raise TypeError("db_params must be a set of database parameters.")
        
        # Connect to our postgres sql database
        with psycopg.connect(**db_params) as connection:
            
            # iterate through the sql_files dict and track our iteration with enumerate
            for index, sql_file in enumerate(sql_files, start=1):
                
                # open each sql file in reading mode
                with open(file=sql_file, mode='r') as file:
                    
                    # read the file and store in the query variable
                    query = file.read()
                    
                    # create the dataframe
                    frame = pd.read_sql_query(sql=query, con=connection)
                    print(f"Sample of Dataframe_{index}: {frame.head(3)}")
                    
                    # add the dataframe to our dictionary
                    if not frame.empty:
                        frames[index] = frame
                        config.logging.info(f"DataFrame successfully created for SQL File {file}")
                    else:
                        config.logging.error(f"Frame_{index} has not been added to the dictionary as the DataFrame is empty.")
                     
    except Exception as e:
        config.logging.error(f"Unable to generate dataframes. Received error {e}")
    
    # log the success
    config.logging.info("Dataframes successfully created and stored in the frames dictionary.")
    
    return frames
