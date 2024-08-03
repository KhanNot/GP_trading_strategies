import random
from deap import gp

#Mutate entire branch:
def mutBranch(individual, pset, max_per_mutate=50):
    """Replaces a randomly chosen primitive from *individual* by a randomly
    chosen primitive with the same number of arguments from the :attr:`pset`
    attribute of the individual.

    :param individual: The normal or typed tree to be mutated.
    :returns: A tuple of one tree.
    """
    if len(individual) < 2:
        return individual,

    if (max_per_mutate*len(individual)/100) > 1 :
        "If the percentage of nodes that may be mutated is more than one randomly get the index."
        index=0
        while (len(individual) - index) > (max_per_mutate*len(individual)/100):
            "Ensure that maximum mutation portion is not exceeded."
            index = random.randrange(1, len(individual))
    else:
        index = len(individual)
    
    for i in range(index,len(individual)):
        node = individual[i]
        if node.arity == 0:  # Terminal
            term = random.choice(pset.terminals[node.ret])
            individual[i] = term
        else:  # Primitive
            prims = [p for p in pset.primitives[node.ret] if p.args == node.args]
            individual[i] = random.choice(prims)

    return individual,

def mutation_half(individual,mut_per, pset):
    if random.random()<0.5:
        return gp.mutNodeReplacement(individual, pset = pset)
    else:
        return mutBranch(individual, max_per_mutate = mut_per, pset=pset)