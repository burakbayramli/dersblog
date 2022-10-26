import numpy as np

M = 3000; D = 20
A = np.random.rand(M,D)*10
np.savetxt('/tmp/A.csv', A, delimiter=';',fmt='%1.6f')

C = np.dot(A.transpose(),A)
print (C.shape)
np.savetxt('/tmp/C.csv', C, delimiter=';',fmt='%1.6f')
