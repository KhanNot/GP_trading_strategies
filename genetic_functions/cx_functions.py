import random 

def get_sub_trees(ind):
    """
    Extract terminal subtrees from a decision tree representation.

    This function identifies terminal subtrees in a decision tree and returns
    a list of dictionaries, where each dictionary contains the starting index
    of the subtree and the subtree itself.

    Args:
        ind: A list representing the decision tree, where each element has an
             `arity` attribute indicating the number of arguments it takes.

    Returns:
        list: A list of dictionaries, where each dictionary has the following keys:
              - "start_index": The starting index of the subtree in the decision tree.
              - "primitive": A list of elements representing the subtree.
    """
    ind_subs = []
    for i in range(0,len(ind)):
        if [elem.arity for elem in ind][i:i+3]==[2,0,0]:
            ind_subs.append({
                "start_index":i,
                "primitive":[elem for elem in ind][i:i+3]
                })
    return ind_subs

def cxSubTree(ind1,ind2, toolbox):
    """
    Perform subtree crossover between two individuals.
    This function selects random subtrees from two individuals and swaps them
    to create two new offspring. The subtrees are identified using the 
    `get_sub_trees` function, and the individuals are cloned before modification
    to preserve the originals.
    Args:
        ind1: The first individual (typicCreate a dictionary containing the terminal sub-trees and the their starting index in the decision tree.ally a tree-based representation).
        ind2: The second individual (typically a tree-based representation).
        toolbox: A DEAP toolbox object that provides the `clone` method for 
                    duplicating individuals.
    Returns:
        tuple: A tuple containing two new individuals (ind1c, ind2c) resulting 
                from the subtree crossover.
    Note:
        - The `get_sub_trees` function is expected to return a list of subtrees
            with each subtree represented as a dictionary containing at least 
            "start_index" and "primitive" keys.
        - The length of the subtree being swapped is assumed to be 3.
    """
    r1 = random.randrange(0,len(get_sub_trees(ind1)))
    r2 = random.randrange(0,len(get_sub_trees(ind2)))

    i1= get_sub_trees(ind1)[r1]["start_index"]
    i2= get_sub_trees(ind2)[r2]["start_index"]

    ind1c = toolbox.clone(ind1)
    ind2c = toolbox.clone(ind2)
    ind1c[i1:i1+3] = get_sub_trees(ind2)[r2]["primitive"]
    ind2c[i2:i2+3] = get_sub_trees(ind1)[r1]["primitive"]

    return ind1c, ind2c