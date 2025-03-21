import random
from deap import gp

#Mutate entire branch:
def mutBranch(individual, pset, toolbox, max_per_mutate=50):
    """
    * This function is from a mutation of the function within the DEAP library. *
    Mutates a given individual by replacing a randomly chosen primitive or terminal 
    with another of the same type from the provided primitive set (pset). The mutation 
    is constrained by a maximum percentage of nodes that can be altered.
    Parameters:
        individual (gp.PrimitiveTree): The tree structure (individual) to be mutated.
        pset (deap.gp.PrimitiveSet): The primitive set containing terminals and primitives 
            for mutation.
        toolbox (deap.base.Toolbox): The DEAP toolbox used for genetic programming operations.
        max_per_mutate (int, optional): The maximum percentage of nodes in the tree 
            that can be mutated. Defaults to 50.
    Returns:
        tuple: A tuple containing the mutated individual.
    Notes:
        - If the individual has fewer than 2 nodes, no mutation is performed.
        - The mutation process ensures that the arity (number of arguments) of primitives 
          remains consistent.

    """
    #If the individual is too small to mutate return the unmutated individual
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

    return individual

def mutation_half(individual,mut_per,toolbox, pset):

    if random.random()<0.5:
        return gp.mutNodeReplacement(individual, pset = pset)
    else:
        return mutBranch(individual, max_per_mutate = mut_per,toolbox=toolbox, pset=pset)