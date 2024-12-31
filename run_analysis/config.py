"""
Configuration File
- Stores the following information: 
    a) API Information
    b) Application Settings
    c) Logger
    d) Constants
    e) Access Keys
    f) Path and File Directories
"""
import logging
import datetime as dt
from pathlib import Path

"""
Variables for our Database
"""
db_parameters = {
    "host": "localhost",
    "dbname": "sql_practice_1",
    "user": "postgres",
    "password": 2792,
    "port": 5433,
}


"""
FilePaths for Our Project
"""
# Project root; leads to data_job_analysis
current_directory = Path(__file__).parent.parent

# Paths to CSV Files
comp_dim = current_directory.joinpath('data_files', 'csv_files', 'company_dim.csv')
job_postings = current_directory.joinpath('data_files', 'csv_files', 'new_job_postings_fact.csv')

# Path to project logs
project_logs_path = current_directory.joinpath('project_logs')

# Path to SQL files
sql_1 = current_directory.joinpath('data_files', 'sql_files', '1_top_paying_jobs.sql')
sql_2 = current_directory.joinpath('data_files', 'sql_files', '2_skills_for_top_paying_jobs.sql')
sql_3b = current_directory.joinpath('data_files', 'sql_files', '3b_highest_demand_skills_by_remote_job.sql')
sql_4 = current_directory.joinpath('data_files', 'sql_files', '4_most_important_skills_to_learn.sql')
sql_5 = current_directory.joinpath('data_files', 'sql_files', '5_skills_to_salaries.sql')

# list of all of our sql files
sql_query_list = [
    sql_1,
    sql_2,
    sql_3b,
    sql_4,
    sql_5
]

# list of all of our file paths for the project
all_file_paths = {
    comp_dim,
    job_postings,
    project_logs_path,
    sql_1,
    sql_2,
    sql_3b,
    sql_4
}

# quick function to check all filepaths exist
def check_file_path(files=all_file_paths) -> None:
    
    for file_path in files:
        if file_path.exists():
            logging.info(f'File path for {file_path} exists!')
        else:
            logging.error(f"File path for {file_path} does not exist! Please review the path.")



"""
Initialize the Logger
"""
log_date = dt.datetime.now().strftime("%B %d, %Y")
#print(log_date)

# configuration for our logger
logging.basicConfig(
    level=logging.DEBUG,
    filename=f'{project_logs_path}/script_log_{log_date}',
    filemode='w',
    format='%(asctime)s::%(levelname)s::%(module)s::%(lineno)d::%(message)s'
)