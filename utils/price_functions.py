import matplotlib.pyplot as plt
from scipy.misc import electrocardiogram
from scipy.signal import find_peaks
import numpy as np
import random

class price_functions():
    def __init__(self):
        pass
    def moving_average(self, ts, lag):
        return ts.rolling(lag).mean()

    def lagged_price(self,ts,lag):
        return ts.shift(lag)

    def percentage_of_value(self, value, random_number = random.random()):
        return value*random_number
    
