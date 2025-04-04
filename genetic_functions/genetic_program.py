import random
from operator import attrgetter
from deap import base, creator, tools, gp, algorithms


def cross_mut(population, toolbox, cxpb, mutpb, elite_pop_size, ngen, gen):
    """
    Performs crossover and mutation operations on a population while preserving elite individuals.
    Parameters
    ----------
    population : list
        List of individuals in current population
    toolbox : deap.base.Toolbox
        DEAP toolbox containing registered genetic operators
    cxpb : float
        Probability of crossover between two individuals (0-1)
    mutpb : float
        Probability of mutation for an individual (0-1) 
    elite_pop_size : int
        Number of top performing individuals to preserve unchanged
    ngen : int
        Total number of generations to run
    gen : int 
        Current generation number
    Returns
    -------
    list
        New population after applying crossover and mutation operators
    Notes
    -----
    - Elite individuals are preserved unchanged at the start of new population
    - Crossover occurs between random pairs of non-elite individuals
    - Mutation rate adapts based on remaining generations
    - Fitness values are deleted after genetic operations to force re-evaluation
    """

    #Elitism:
    elite_pop = [toolbox.clone(ind) for ind in sorted(population, key=attrgetter("fitness"), reverse=True)[:elite_pop_size]]
    offspring = [toolbox.clone(ind) for ind in population]
    for idx, ind in enumerate(elite_pop):
        offspring[idx] = toolbox.clone(ind)
    # Apply crossover and mutation on the offspring
    for i in range(elite_pop_size+1, len(offspring)):
        if random.random() < cxpb:
            bi = random.randint(elite_pop_size+1, len(offspring)-1)
            offspring[bi], offspring[i] = toolbox.mate(offspring[bi],offspring[i])
            del offspring[bi].fitness.values, offspring[i].fitness.values

    for i in range(elite_pop_size+1, len(offspring)):
        if random.random() < mutpb:
            mut_per = ((ngen+1-gen)/(ngen+1-gen))*100
            # print("Before Mut:",str(gp.PrimitiveTree(offspring[i])))
            offspring[i]= toolbox.mutate(offspring[i], mut_per=mut_per)
            # print("After Mut:",str(gp.PrimitiveTree(offspring[i])))
            del offspring[i].fitness.values

    elits_check = []
    for ind,val in enumerate(population):
        elits_check.append(val == offspring[ind])
    # print(elits_check)
    print(sum(elits_check))
    # print(len([i for i in pop if i in offspring]))
    # print("Unique items in pop",set(pop), ' of ',len(pop))
    return offspring

def GPAlgo(population, 
           toolbox, cxpb, 
           mutpb, ngen, 
           elite_pop_size, 
           stats=None,
            halloffame=None, 
            verbose=__debug__
            ):
    """
        Executes a genetic programming algorithm that evolves a population over multiple generations.
        This function implements a genetic programming algorithm that evolves a population
        over multiple generations using selection, crossover, and mutation operations while
        preserving elite individuals.
        Parameters
        ----------
        population : list
            A list of individuals to evolve
        toolbox : deap.base.Toolbox
            A DEAP toolbox containing the evolution operators
        cxpb : float
            The probability of mating two individuals (crossover probability)
        mutpb : float
            The probability of mutating an individual
        ngen : int
            Number of generations to evolve
        elite_pop_size : int
            Number of best individuals to preserve between generations
        stats : deap.tools.Statistics, optional
            A DEAP Statistics object for collecting evolution statistics
        halloffame : deap.tools.HallOfFame, optional
            A DEAP HallOfFame object to record the best individuals
        verbose : bool, optional
            Whether to print the statistics after each generation
        Returns
        -------
        tuple
            A tuple containing:
            - The final population (list)
            - A logbook recording statistics
            - A dictionary storing populations and offspring for each generation
        Notes
        -----
        The function implements elitism by preserving the best individuals across generations.
        It stores the state of evolution in each generation in a dictionary for later analysis.
    """
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    store_generations = {}
    # Begin the generational process
    for gen in range(1, ngen + 1):
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population)-elite_pop_size)

        offspring = cross_mut(population, toolbox, cxpb, mutpb, elite_pop_size, ngen, gen)
        
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # Replace the current population by the offspring
        store_generations[f"gen{gen}"]={
            "pop":population,
            "offspring":offspring
        }
        population[:] = offspring

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

    return population, logbook, store_generations