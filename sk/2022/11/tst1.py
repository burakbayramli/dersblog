import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

M = 1*1000*1000; D = 100; N = 30

A = np.random.rand(M,D)*10
np.savetxt('/mnt/3d1ece2f-6539-411b-bac2-589d57201626/home/burak/Downloads/A.csv', A, delimiter=';',fmt='%1.6f')
B = np.random.rand(D,N)*10
np.savetxt('/mnt/3d1ece2f-6539-411b-bac2-589d57201626/home/burak/Downloads/B.csv', B, delimiter=';',fmt='%1.6f')
