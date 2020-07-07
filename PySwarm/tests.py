import itertools
import numpy as np
import pandas as pd
from controller import controller


a = np.array([True, True, False, False])
b = np.array([True, True, False, True])

c = np.multiply(a,b)

sum = np.sum(c)

print(sum)
