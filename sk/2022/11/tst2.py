import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy.linalg as lin
import pandas as pd
from scipy.spatial.distance import cdist

A = np.array(range(0,20)).reshape(5,4)
B = np.array(range(20,40)).reshape(4,5)
multres = np.zeros((5,5))
for i in range(A.shape[0]):
    s = np.zeros(5)
    row = (A[i, :])
    multres += row.reshape(1,4).T * B
print (multres.shape)

