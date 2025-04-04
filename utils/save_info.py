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
    """
    Saves the results of a genetic programming run to a specified directory.
    This function serializes and stores the hall of fame (hof), population, 
    and logbook objects as pickle files. Additionally, it saves run information 
    as a CSV file. The results are stored in a uniquely named folder based on 
    the current date and time, and optionally a parallel run identifier.
    Args:
        hof:                The hall of fame object containing the best individuals.
        population:         The population of individuals at the end of the run.
        logbook:            The logbook object containing the evolutionary history.
        store_generations:  Unused parameter (reserved for future use).
        run_info:           A pandas DataFrame containing run-specific information.
        parallel_number:    An integer representing the parallel run number, or 
                                None if not applicable.
        base_dir (str):     The base directory where the results folder will be created.
    Raises:
        OSError:            If the directory creation fails.
        Exception:          If there is an issue during file serialization or saving.
    """
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
