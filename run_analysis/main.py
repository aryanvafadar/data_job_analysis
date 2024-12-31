import config
from functions import  sql_query_to_dataframe

def main():
    
    # dataframes created for each sql query.
    frame_sql_1 = sql_query_to_dataframe(file_1=config.sql_1, db_params=db_params)
    frame_sql_2 = sql_query_to_dataframe(file_1=config.sql_2, db_params=db_params)
    frame_sql_3 = sql_query_to_dataframe(file_1=config.sql_3b, db_params=db_params)
    frame_sql_4 = sql_query_to_dataframe(file_1=config.sql_4, db_params=db_params)
    

    
    
    
    
    


if __name__ == "__main__":
    
    # ensure all file paths exist
    try:
        config.check_file_path()
    except Exception as e:
        config.logging.error(f"Error in filepaths. Please review config file. Received error {e}")
    
    # database connection paramaters
    db_params = config.db_parameters
    
