import os
import pendulum
import pickle

def save_results(
        hof,
        population, 
        logbook, 
        store_generations,
        run_info,
        parallel_number, 
        base_dir:str):
    date = pendulum.now().format('YYYY-MM-DD_hh-mm')
    if parallel_number==None:
        folder_name = rf'{base_dir}run_{date}/'
    else:
        folder_name = rf'{base_dir}run_p{parallel_number}_{date}/'
    os.makedirs(folder_name)

    with open(rf"{folder_name}hof.pkl", 'wb') as file:
    # Serialize the object and write it to the file
        pickle.dump(hof, file)

    with open(rf"{folder_name}population.pkl", 'wb') as file:
    # Serialize the object and write it to the file
        pickle.dump(population, file)

    with open(rf"{folder_name}logbook.pkl", 'wb') as file:
    # Serialize the object and write it to the file
        pickle.dump(logbook, file)

    run_info.to_csv(rf"{folder_name}run_info.csv")
