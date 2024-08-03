from prefect import task, flow
import pendulum
from main import main_func


@task(task_run_name = "generation_run_{date}")
def run_main(date = pendulum.now().format("YYYYMMDD_hh-mm"),p :int|None = None):
    main_func(
            population_size =10,
            num_generations= 2,
            parallel_number = p
            )
    
@flow(flow_run_name = "parallel_generation_run_{date}")
def parallel_run_main(date = pendulum.now().format("YYYYMMDD_hh-mm")):
    run_main.submit(p=1)
    run_main.submit(p=2)
    # run_main.submit()
    # run_main.submit()

if __name__ =="__main__":
    parallel_run_main()


