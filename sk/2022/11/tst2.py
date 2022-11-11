import numpy as np

A = np.array(range(0,20)).reshape(5,4)
k = 2
res = []
for i in range(A.shape[0]):
    np.random.seed(0)
    s = np.zeros(k)
    for e in A[i, :]: s += e*np.random.normal(0,1,k)
    res.append(s)
Y = np.array(res)
print (Y)
