import pandas as pd, numpy as np, random
import matplotlib.pyplot as plt
import numpy.linalg as lin
import pandas as pd
from scipy.spatial.distance import cdist

k = 7 
df = pd.read_csv("/home/burak/Documents/classnotes/linear/linear_app10rndsvd/w1.dat",sep=';',header=None)
A = np.array(df)[:,1:]
print (A.shape)
d1 = cdist(A,A,metric='euclid')
d1 = d1 / np.sum(d1)

res = []
for i in range(A.shape[0]):
    s = np.zeros(k)
    row = (A[i, :])
    np.random.seed(0)
    for elem in row: s += elem*np.random.normal(0,1,k)
    res.append(s)
Y = np.array(res)
print (Y.shape)

d2 = cdist(Y,Y,metric='euclid')
d2 = d2 / np.sum(d2)
print (np.mean(d1),d1.shape)
print (np.mean(d2),d2.shape)

print (np.abs(d1-d2))
