
```python
import numpy.linalg as lin
import pandas as pd
from scipy.spatial.distance import cdist
t = 'euclid'
k = 7
df = pd.read_csv("/home/burak/Documents/classnotes/linear/linear_app10rndsvd/w1.dat",sep=';',header=None)
A = np.array(df)[:,1:]
print (A.shape)
d1 = cdist(A,A,metric=t)
d1 = d1 / np.sum(d1)
print (np.mean(d1),d1.shape)
Y = np.dot(A, np.random.normal(0,1,(A.shape[1],k)))
d2 = cdist(Y,Y,metric=t)
d2 = d2 / np.sum(d2)
print (np.mean(d2),d2.shape)
print (np.abs(d1-d2))
```

```text
(71, 30)
0.00019837333862328903 (71, 71)
0.00019837333862328903 (71, 71)
[[0.00000000e+00 2.67470260e-06 2.21094867e-05 ... 1.20967312e-05
  2.35787521e-05 1.38117910e-05]
 [2.67470260e-06 0.00000000e+00 2.47023382e-06 ... 1.32325710e-05
  3.57408226e-06 5.31530346e-06]
 [2.21094867e-05 2.47023382e-06 0.00000000e+00 ... 1.52615473e-05
  5.67120513e-06 8.50054118e-06]
 ...
 [1.20967312e-05 1.32325710e-05 1.52615473e-05 ... 0.00000000e+00
  8.05078505e-06 4.29970690e-06]
 [2.35787521e-05 3.57408226e-06 5.67120513e-06 ... 8.05078505e-06
  0.00000000e+00 5.99962681e-06]
 [1.38117910e-05 5.31530346e-06 8.50054118e-06 ... 4.29970690e-06
  5.99962681e-06 0.00000000e+00]]
```



