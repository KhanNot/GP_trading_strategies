import random
from operator import attrgetter
from deap import base, creator, tools, gp, algorithms

def GPAlgo(population, 
           toolbox, cxpb, 
           mutpb, ngen, 
           elite_pop_size, 
           stats=None,
            halloffame=None, 
            verbose=__debug__
            ):
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
        offspring = toolbox.select(population, len(population))

        # Vary the pool of individuals
        # assert (cxpb + mutpb) <= 1.0, (
        # "The sum of the crossover and mutation probabilities must be smaller "
        # "or equal to 1.0.")

        #Elitism:
        elite_pop = sorted(population, key=attrgetter("fitness"), reverse=True)[:elite_pop_size]
        offspring = [toolbox.clone(ind) for ind in population]
        offspring[:elite_pop_size] = elite_pop

        # Apply crossover and mutation on the offspring
        for i in range(elite_pop_size+1, len(offspring)):
            if random.random() < cxpb:
                bi = random.randint(elite_pop_size+1, len(offspring)-1)
                offspring[bi], offspring[i] = toolbox.mate(offspring[bi],
                                                            offspring[i])
                del offspring[bi].fitness.values, offspring[i].fitness.values

        for i in range(elite_pop_size+1, len(offspring)):
            if random.random() < mutpb:
                mut_per = ((ngen+1-gen)/(ngen+1-gen))*100
                # print("Before Mut:",str(gp.PrimitiveTree(offspring[i])))
                offspring[i], = toolbox.mutate(offspring[i], mut_per=mut_per)
                # print("After Mut:",str(gp.PrimitiveTree(offspring[i])))
                del offspring[i].fitness.values

        elits_check = []
        for ind,val in enumerate(population):
            elits_check.append(val == offspring[ind])
        # print(elits_check)
        print(sum(elits_check))
        # print(len([i for i in pop if i in offspring]))
        # print("Unique items in pop",set(pop), ' of ',len(pop))


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