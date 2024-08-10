import pandas as pd
import matplotlib.pyplot as plt
from scipy.misc import electrocardiogram
from scipy.signal import find_peaks
import numpy as np
import random

from deap import gp, creator, base, tools
import operator
from operator import or_, and_, gt

def maximum_theoretical_value(df: pd.DataFrame, val: int|float =1000, tc: int|float = 0.01):
    df_open = df['Open']
    x = df_open.reset_index()['Open']

    # Get peaks and troughs
    peaks, _ = find_peaks(x)
    troughs, _ = find_peaks(-x)

    peaks_troughs = list(peaks)+list(troughs)
    #Add the enedpoints to the local maximum and minimums.
    if 0 not in peaks_troughs:
        peaks_troughs.append(0)
    if len(df_open)-1 not in peaks_troughs:
        peaks_troughs.append(len(df_open)-1)

    peaks_troughs = sorted(peaks_troughs)
    peaks_troughs

    #Work out maximum theoretical value using an nitial investement of $1000 by default.
    profit=0
    val = 1000
    no_tc_val = 1000
    for ind,price in enumerate(df_open.iloc[peaks_troughs]):
        if ind>1 and price > df_open.iloc[peaks_troughs].iloc[ind-1]:
            # Calculate 
            pot_val= (val*price/df_open.iloc[peaks_troughs].iloc[ind-1])*(1-tc)**2
            if pot_val>val:
                val=pot_val        
    # no_tc
    if ind>1 and price > df_open.iloc[peaks_troughs].iloc[ind-1]:
        no_tc_val = (no_tc_val*price/df_open.iloc[peaks_troughs].iloc[ind-1])
        
    return val 

def trading_strat(individual, df:pd.DataFrame,pset, start_value=1000, transaction_cost = 0.01, strat_df:bool=False):
    tc = transaction_cost
    val = start_value
    ts_val = [val]
    ts_df = pd.DataFrame(columns = ["value"])
    long = False
    delayed_signal = False

    function = gp.compile(expr=gp.PrimitiveTree(individual),pset=pset)

    signal_df  = pd.DataFrame(index=df.index)
    signal_df['Signal'] = function(df = df)
    signal_df["Open"] = df['Open']
    if strat_df:
        signal_df['Buy'] = [True]+[False]*(len(df)-1)
        signal_df['Sell'] = [False]*len(df)

    for cnt,row in enumerate(signal_df.iterrows()):

        if (delayed_signal) == True and not long:
            # print("Buy at: ",row[1]['Open'])
            #Buy/hold signal
            shares = ((1-tc)*val)/row[1]['Open']
            long=True
            if strat_df:
                signal_df[row[0],'Buy']=True
        if (delayed_signal) == False and long:
            # print("Sell at: ",row[1]['Open'])
            val = (1-tc)*shares*row[1]['Open']
            long=False
            if strat_df:
                signal_df[row[0],'Sell']=True
            ts_val.append(val)
        if cnt == len(df) and long:
            val = shares*row[1]['Open']
        ts_df.loc[row[0]] = val

        delayed_signal = row[1]['Signal']
        

    #Calculate the MDD:
    try:
        mdd = min([v-ts_val[ind-1] for ind, v in enumerate(ts_val) if ind>0])
    except:
        mdd = 0
    if strat_df:
        return val, mdd, ts_val, signal_df
    else:
        return val, mdd, ts_val
    

def fitness_function(individual, df,tc, pset):
    val, mdd, ts_val = trading_strat(individual = individual, df = df,transaction_cost=tc,pset=pset)
    mtv = maximum_theoretical_value(df, tc=tc)
    #Using the FF below results in the MDD having a much larger weight than the Value of the final value of the strategy.
    # return [(val/mtv)-mdd]
    return [(val+mdd)]