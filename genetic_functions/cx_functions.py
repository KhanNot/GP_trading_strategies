import random 

def cxSubTree(ind1,ind2):
    def get_sub_trees(ind):
        """"Create a dictionary containing the terminal sub-trees and the their starting index in the decision tree."""
        ind_subs = []
        for i in range(0,len(ind)):
            if [elem.arity for elem in ind][i:i+3]==[2,0,0]:
                ind_subs.append({
                    "start_index":i,
                    "primitive":[elem for elem in ind][i:i+3]
                    })
        return ind_subs

    r1 = random.randrange(0,len(get_sub_trees(ind1)))
    r2 = random.randrange(0,len(get_sub_trees(ind2)))

    i1= get_sub_trees(ind1)[r1]["start_index"]
    i2= get_sub_trees(ind2)[r2]["start_index"]

    ind1c = ind1.copy()
    ind2c = ind2.copy()
    ind1c[i1:i1+3] = get_sub_trees(ind2)[r2]["primitive"]
    ind2c[i2:i2+3] = get_sub_trees(ind1)[r1]["primitive"]

    return ind1c, ind2c