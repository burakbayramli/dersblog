
from datetime import timedelta
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

start = timer()
A = np.loadtxt("/tmp/A.csv",delimiter=';')
B = np.loadtxt("/tmp/B.csv",delimiter=';')
C = np.dot(A,B)
np.savetxt('/tmp/C2.csv', C, delimiter=';',fmt='%1.6f')
end = timer()
print('elapsed time', timedelta(seconds=end-start))
print (C.shape)

#  elapsed time 0:01:24.053847, M = 1*1000*1000; D = 100; N = 30
