import multiprocessing
from main import main_func

def jou_funksie(id: int):
    main_func(
            population_size =10,
            num_generations= 2,
            parallel_number = id
            )

if __name__ == '__main__':
    processes = []
    for i in range(5):
        p = multiprocessing.Process(target=jou_funksie, args=(i,))
        processes.append(p)

    joiner = [
        p.join() for p in processes
    ]

    print("Fuck yes")