"""
Module: multi_run
This module provides functionality for running genetic programming (GP) trading strategies 
in parallel using the `multiprocessing` module. It includes methods for initializing and 
executing the main function with or without a predefined population, as well as handling 
data preprocessing.
Functions:
    - initialise_main: Initializes and executes the main function for a single process.
    - parallel_run: Runs multiple instances of the main function in parallel processes.
    - main_with_pre_pop: Executes the main function with a predefined population loaded from a file.
    - parallel_run_pre_pop: Runs multiple instances of the main function in parallel processes, 
      each using a predefined population from a specified directory.
Dependencies:
    - os: For file and directory operations.
    - multiprocessing: For creating and managing parallel processes.
    - pandas: For handling data in DataFrame format.
    - pickle: For loading predefined populations from serialized files.
    - main.main_func: The main function to be executed in parallel.
    - utils.pre_process_data.get_data: A utility function for data preprocessing.
Usage:
    This module is designed to be executed as a standalone script. It retrieves data using 
    the `get_data` function, and then runs either `parallel_run` or `parallel_run_pre_pop` 
    to execute the main function in parallel processes.
Example:
    To execute the script, ensure all dependencies are properly set up and run:
        python multi_run.py
    - The directory paths for predefined populations are hardcoded and should be updated 
      if the file locations change.
    - Ensure that the `main_func` and `get_data` functions are implemented and accessible 
      in the specified modules.
"""

import os
import multiprocessing
import pandas as pd
from main import main_func
from utils.common import *
from utils.pre_process_data import get_data
import pickle

def initialise_main(id: int, df):
    main_func(
            population_size =100,
            num_generations= 100,
            parallel_number = id,
            df =df
            )

def parallel_run(df):
    """
    Executes the `initialise_main` function in parallel using multiple processes.
    This function creates 24 separate processes, each running the `initialise_main` 
    function with a unique index and the provided dataframe (`df`) as arguments. 
    It ensures all processes are started and waits for their completion.
    Args:
        df (pandas.DataFrame): The dataframe to be passed as an argument to the 
            `initialise_main` function in each process.
    Note:
        - The `initialise_main` function must be defined elsewhere in the code.
        - The `multiprocessing` module is used to create and manage processes.
    """
    processes = []
    for i in range(24):
        p = multiprocessing.Process(target=initialise_main, args=(i,df))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


def main_with_pre_pop(id: int,file_name:str, df: pd.DataFrame):
    """
    Executes the main function with a predefined population loaded from a file.
    Args:
        id (int): An identifier for the parallel process or run.
        file_name (str): The name of the file containing the predefined population.
        df (DataFrame): The input data frame to be used in the main function.
    Raises:
        FileNotFoundError: If the specified file does not exist.
        pickle.UnpicklingError: If there is an error while loading the pickle file.
    Notes:
        The function reads a predefined population from a pickle file located at a specific path,
        and then passes it to the `main_func` along with other parameters.
    """

    with open(os.path.join(REPO_DIRECTORY_PATH,"results_run2_gen3",file_name), 'rb') as file:
        pop = pickle.load(file)
        file.close()

    main_func(
            population_size =20,
            num_generations= 100,
            parallel_number = id,
            df =df,
            population_predefined = pop
            )



def parallel_run_pre_pop(df):
    """
    Executes the `main_with_pre_pop` function in parallel processes for each file in a specified directory.
    Args:
        df (pandas.DataFrame): A DataFrame passed as an argument to the `main_with_pre_pop` function.
    Behavior:
        - Retrieves a list of files from a specific directory.
        - Creates a separate process for each file in the directory.
        - Each process runs the `main_with_pre_pop` function with the file index, file name, and the provided DataFrame as arguments.
        - Waits for all processes to complete before exiting.
    Note:
        - The directory path is hardcoded and should be updated if the location changes.
        - Ensure that the `main_with_pre_pop` function and the `multiprocessing` module are properly imported.
    """

    processes = []
    run_list = os.listdir(os.path.join(REPO_DIRECTORY_PATH,"results","results_run2_gen3"))
    
    for i,pop_file in enumerate(run_list):
        p = multiprocessing.Process(target=main_with_pre_pop, args=(i,pop_file, df))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
        

if __name__ == '__main__':
    df = get_data()
    # for i in range(10):
    #     parallel_run(df)
    parallel_run_pre_pop(df)

    print("Finished")
    