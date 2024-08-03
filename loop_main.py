from main import main_func

def loop_over_main(run_numbers):
    for i in range(0,run_numbers):
        main_func(
            population_size =100,
            num_generations= 50,
            )
