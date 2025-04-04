#Mutate entire branch:
def mutBranch(individual, pset, max_per_mutate=50):
    """
    Mutates a branch of the given individual by replacing nodes with randomly 
    selected terminals or primitives from the provided primitive set (pset).
    Parameters:
        individual (list): The individual (tree representation) to be mutated.
        pset (deap.gp.PrimitiveSet): The primitive set containing terminals and 
            primitives used for mutation.
        max_per_mutate (int, optional): The maximum percentage of nodes in the 
            individual that can be mutated. Defaults to 50.
    Returns:
        tuple: A tuple containing the mutated individual.
    Notes:
        - If the individual has fewer than 2 nodes, no mutation is performed.
        - The mutation process ensures that the maximum mutation portion 
          (defined by `max_per_mutate`) is not exceeded.
        - Terminals are replaced with randomly chosen terminals of the same 
          return type.
        - Primitives are replaced with randomly chosen primitives of the same 
          return type and arity.
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