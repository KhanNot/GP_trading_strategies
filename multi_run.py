import multiprocessing
from main import main_func

def jou_funksie(id: int):
    main_func(
            population_size =100,
            num_generations= 50,
            parallel_number = id
            )

if __name__ == '__main__':
    processes = []
    for i in range(100):
        p = multiprocessing.Process(target=jou_funksie, args=(i,))
        processes.append(p)
        p.start()

for p in processes:
    p.join()

    print("Fuck yes")