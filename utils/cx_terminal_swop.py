import random

def cxTerminalSwop(ind1,ind2):
    def get_terminals(ind):
        teminal_list = []
        for i,elem in enumerate(ind):
            if elem.arity==0:
                teminal_list.append({
                    "index":i,
                    "unit": "volume" if "volume"in elem.name.lower() else "dollar",
                    "ternimal": elem
                })
        return teminal_list

    t1 = get_terminals(ind1)
    t2 = get_terminals(ind2)

    #check wether both trees contain all units:
    u1 = set([i["unit"] for i in t1])
    u2 = set([i["unit"] for i in t2])
    if len(u2)==1:
        unit=[i for i in u2][0]
        t1 = [ter for ter in t1 if ter["unit"]==unit]
        if t1==[]:
            return ind1,ind2

    if len(u1)==1:
        unit=[i for i in u1][0]
        t2 = [ter for ter in t2 if ter["unit"]==unit]
        if t2==[]:
            return ind1,ind2

    r1 = random.randrange(0,len(t1))
    r2 = random.randrange(0,len(t2))

    ind1[t1[r1]["index"]] = t2[r2]["ternimal"]
    ind2[t2[r2]["index"]] = t1[r1]["ternimal"]
    return ind1,ind2