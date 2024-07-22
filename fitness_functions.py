import pandas as pd
import matplotlib.pyplot as plt
from scipy.misc import electrocardiogram
from scipy.signal import find_peaks
import numpy as np
import random

from deap import gp, creator, base, tools
import operator
from operator import or_, and_, gt

class Volume:
    def __init__(self, value: float):
        self.value = value

class Dollar:
    def __init__(self, value: float):
        self.value = value


def maximum_theoretical_value(df: pd.DataFrame, val: int|float =1000, tc: int|float = 0.01):
    btc_ts_open = df['Open']
    x = btc_ts_open.reset_index()['Open']

    # Get peaks and troughs
    peaks, _ = find_peaks(x)
    troughs, _ = find_peaks(-x)

    peaks_troughs = list(peaks)+list(troughs)
    #Add the enedpoints to the local maximum and minimums.
    if 0 not in peaks_troughs:
        peaks_troughs.append(0)
    if len(btc_ts_open)-1 not in peaks_troughs:
        peaks_troughs.append(len(btc_ts_open)-1)

    peaks_troughs = sorted(peaks_troughs)
    peaks_troughs

    #Work out maximum theoretical value using an nitial investement of $1000 by default.
    profit=0
    val =1000
    for ind,price in enumerate(btc_ts_open.iloc[peaks_troughs]):
        if ind>1 and price*(1+tc) > btc_ts_open.iloc[peaks_troughs].iloc[ind-1]:
            profit += price*(1+tc) - btc_ts_open.iloc[peaks_troughs].iloc[ind-1]

            shares_buy = val*(1-tc)/btc_ts_open.iloc[peaks_troughs].iloc[ind-1]
            val = shares_buy*price*(1-tc)
            
    return val 

def trading_strat(individual, df:pd.DataFrame,pset, start_value=1000, transaction_cost = 0.01):
    tc = transaction_cost
    val = start_value
    ts_val = [val]
    long = False

    function = gp.compile(expr=gp.PrimitiveTree(individual),pset=pset)

    signal_df  = pd.DataFrame(index=df.index)
    print(function(df = df))
    signal_df['Signal'] = function(df = df)
    signal_df["Open"] = df['Open']
    print(signal_df)

    for cnt,row in enumerate(signal_df.iterrows()):
        if (row[1]['Signal']) == True and not long:
            # print("Buy at: ",row[1]['Open'])
            #Buy/hold signal
            shares = ((1-tc)*val)/row[1]['Open']
            long=True
        if (row[1]['Signal']) == False and long:
            # print("Sell at: ",row[1]['Open'])
            val = (1-tc)*shares*row[1]['Open']
            ts_val.append(val)
            long=False
        if cnt == len(df) and long:
            val = shares*row[1]['Open']

    #Calculate the MDD:
    try:
        mdd = min([v-ts_val[ind-1] for ind, v in enumerate(ts_val) if ind>0])
    except:
        mdd = 0
    return val, mdd
    

def fitness_function(individual, df, pset):
    val, mdd = trading_strat(individual = individual, df = df,pset=pset)
    mtv = maximum_theoretical_value(df)
    return [(val/mtv)-mdd]