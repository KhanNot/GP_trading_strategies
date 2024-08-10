from utils.pre_process_data import get_data
from math import ceil
from utils.units import Volume, Dollar
from deap import gp, creator, base, tools
from deap.gp import Terminal
from operator import or_, and_, gt
from fitness_functions import *
from utils.plot_decision_trees import plot_tree
from utils.save_info import save_results
from genetic_functions.cx_functions import cxSubTree
from genetic_functions.mut_functions import mutation_half, mutBranch
from genetic_functions.genetic_program import GPAlgo
import matplotlib.pyplot as plt
import pendulum
import pickle
     
def main_func(
          population_size,
          num_generations,
          directory_path = r"/home/khann/masters",
          parallel_number:int|None= None,
          tc=0.01
    ):

    df = get_data()
    df_train= df.iloc[ : ceil(len(df)*0.7)]
    df_test= df.iloc[ceil(len(df)*0.7) : ]

    arg_names = list(df_train.columns)
    vol_args = [arg for arg in arg_names if "volume" in arg.lower()]
    dol_args = [arg for arg in arg_names if "volume" not in arg.lower()]

    # --- CREATE PRIMITIVE SETS AND TOOLS -----
    pset = gp.PrimitiveSetTyped("main",[Volume]*len(vol_args) + [Dollar]*len(dol_args),bool)
    #Rename the arguments:
    arg_vol_mapping = {f"ARG{ind}": val for ind,val in enumerate(vol_args)}
    pset.renameArguments(**arg_vol_mapping)
    arg_dol_mapping = {f"ARG{len(vol_args)+ind}": val for ind,val in enumerate(dol_args)}
    pset.renameArguments(**arg_dol_mapping)
    #Check that all arguments were renamed:
    unnamed_args=[i for i in pset.arguments if "ARG" in i]
    if  unnamed_args:
        print(f"Some arguments were not renamed: {unnamed_args}")
    pset.addPrimitive(gt, [Dollar,Dollar],bool)
    pset.addPrimitive(lambda x:x ,[Dollar],Dollar, name="dollar placeholder")

    pset.addPrimitive(gt, [Volume,Volume],bool)
    pset.addPrimitive(lambda x:x ,[Volume],Volume, name="volume placeholder")


    #Boolean operators:
    pset.addPrimitive(and_, [bool,bool],bool)
    pset.addPrimitive(or_,[bool,bool],bool)

    for v_arg in vol_args:
            pset.addTerminal(v_arg,Volume)
    for d_arg in dol_args:
            pset.addTerminal(d_arg,Dollar)

    # --- Remove all the ARG terminals ---
    pset.terminals[Volume] = [i for i in pset.terminals[Volume] if "ARG" not in i.name]
    pset.terminals[Dollar] = [i for i in pset.terminals[Dollar] if "ARG" not in i.name]

    def generate(pset):
        run=True
        while run:
            try:
                expr = toolbox.individual()            
                #Remove all the Lambda functions:
                expr=  list(filter(lambda x: x.name!="dollar placeholder", expr))
                expr=  list(filter(lambda x: x.name!="volume placeholder", expr))
                if len(expr)>3:
                    run=False
            except IndexError:
                continue
        # return gp.PrimitiveTree(expr)
        return creator.Individual(expr)

    # --- GP OPERATORS ----

    creator.create("fitness", base.Fitness, weights=(1,))
    creator.create("Individual", gp.PrimitiveTree, fitness= creator.fitness)

    toolbox = base.Toolbox()
    toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=5)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("custom_individual",generate, pset)
    toolbox.register("population", tools.initRepeat, list, toolbox.custom_individual)
    toolbox.register("evaluate", fitness_function, df=df_train,tc=tc, pset=pset)

    toolbox.register("mate",       cxSubTree)
    toolbox.register("select",     tools.selRanked) 
    toolbox.register("mutate",     mutation_half, pset=pset)

    hof   = tools.HallOfFame(maxsize=10)

    #STATS:
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0) 
    stats.register("std", np.std, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    pop = toolbox.population(n=population_size)
    # with open(rf"/home/khann/masters/results/run_1_hof.pkl", 'rb') as file:
    #     pop = pickle.load(file)

    t1 = pendulum.now()
    population, logbook, store_generations = GPAlgo(
        pop, 
        toolbox,
        cxpb=0.7, 
        mutpb=0.6, 
        ngen=num_generations, 
        elite_pop_size= 5,
        stats = stats, 
        halloffame =hof
        )
    t2 = pendulum.now()
    run_time = (t2-t1).seconds

    best_solution=hof.items[0]
    bh_start_train = (1000/df_train.iloc[0]['Open'])*df_train.iloc[-1]['Open']*(1-tc)**2
    strat_train_profit = trading_strat(individual = best_solution, df=df_train,pset=pset)[0]

    bh_start_test = (1000/df_test.iloc[0]['Open'])*df_test.iloc[-1]['Open']*(1-tc)**2
    strat_test_profit = trading_strat(individual = best_solution, df=df_test,pset=pset)[0]

    run_info= pd.DataFrame(columns=['population_number', 'generations', 'run_time', 'best_tree','trading_cost','buy_hold_train','strategy_value_train','buy_hold_test','strategy_value_test'])
    run_info = run_info._append({
         "time":t1,
         "population_number":population_size,
         "generations": num_generations,
         "run_time":run_time,
         "best_tree":str(hof.items[1]),
         "trading_cost":f"{tc*100}%",
         "fitness_value": hof.items[1].fitness.values,
         "buy_hold_train":bh_start_train,
         "strategy_value_train":strat_train_profit,
         "buy_hold_test":bh_start_test,
         "strategy_value_test":strat_test_profit
    },
    ignore_index = True)
    #Save all the run data:
    save_results(
        hof,
        population, 
        logbook, 
        store_generations,
        run_info, 
        parallel_number,
        base_dir="./results_run2/"
        )
    
if __name__=="__main__":
     main_func(
          population_size = 25,
          num_generations= 5,
     )


