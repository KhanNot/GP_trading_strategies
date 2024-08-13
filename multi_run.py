import os
import multiprocessing
import pandas as pd
from main import main_func
from utils.pre_process_data import get_data
import pickle

def jou_funksie(id: int, df):
    main_func(
            population_size =100,
            num_generations= 100,
            parallel_number = id,
            df =df
            )

def parallel_run(df):
    processes = []
    for i in range(24):
        p = multiprocessing.Process(target=jou_funksie, args=(i,df))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


def main_with_pre_pop(id: int,file_name:str, df):
    with open(rf"/home/khann/masters/results_run2_gen2/start_pop/{file_name}", 'rb') as file:
        pop = pickle.load(file)

    main_func(
            population_size =100,
            num_generations= 50,
            parallel_number = id,
            df =df,
            population_predefined = pop
            )



def parallel_run_pre_pop(df):
    processes = []
    run_list = os.listdir("/home/khann/masters/results_run2_gen2/start_pop")
    
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
    