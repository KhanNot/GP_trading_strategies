import multiprocessing
import pandas as pd
from main import main_func
from utils.pre_process_data import get_data

def jou_funksie(id: int, df):
    main_func(
            population_size =100,
            num_generations= 50,
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

        

if __name__ == '__main__':
    df = get_data()
    for i in range(10):
        parallel_run(df)
    print("Finished")
    