
import numpy as np
import matplotlib.pyplot as plt

import itertools
l = list(itertools.permutations([1, 2, 3, 4]))[:10]
for x in l: print (x)
print ('...')

import dhmm

rolls = [1,2,4,5,5,2,6,4,6,2,1,4,6,1,4,6,1,3,6,1,3,6,\
         6,6,1,6,6,4,6,6,1,6,3,6,6,1,6,3,6,6,1,6,3,6,1,\
         6,5,1,5,6,1,5,1,1,5,1,4,6,1,2,3,5,6,2,3,4,4]
rolls = np.array(rolls)-1
a = np.array([[0.95, 0.05],[0.05, 0.95]])
b = np.array([[1/6., 1/6., 1/6., 1/6., 1/6., 1/6.], 
              [1/10.,1/10.,1/10.,1/10.,1/10.,1/2.]])
pi = np.array([0.5, 0.5])

hmm = dhmm.HMM(2,6,pi,a,b)
print (hmm.viterbi_path(rolls))

a = np.array([[0.1,0.4,0.4],[0.4,0.1,0.5],[0.4,0.5,0.1]])
b = np.array([[0.5,0.5],[0.8,0.2],[0.2,0.8]])
pi = np.array([0.5, 0, 0.5])

hmm = dhmm.HMM(3,2,pi,a,b)
print (hmm.viterbi_path([0,1,1]))


a2 = np.array([[0.1,0.4,0.4],[0.2,0.3,0.5],[0.6,0.3,0.1]])
b2 = np.array([[1/6.,1/6.,1/6.,1/6.,1/6.,1/6.],
               [1/10.,1/10.,1/10.,1/10.,1/10.,1/2.],
               [1/8.,1/8.,1/8.,1/8.,1/8.,1/8.]])
pi2 = np.array([0.5,0.2,0.3])
rolls2 = [1,2,4,5,5,2,6,4,6,2,1,4,6,1,4,6,1,3,6,1,3,6,\
          6,6,1,6,6,4,6,6,1,6,3,6,6,1,6,3,6,6,1,6,3,6,1,\
          6,5,1,5,6,1,5,1,1,5,1,4,6,1,2,3,5,6,2,3,4,4]
rolls2 = np.array(rolls2)-1

# Add debug prints to confirm the shapes before initialization
print(f"DEBUG: Shape of 'a2' before hmm2 init: {np.shape(a2)}")
print(f"DEBUG: Shape of 'b2' before hmm2 init: {np.shape(b2)}")
print(f"DEBUG: Shape of 'pi2' before hmm2 init: {np.shape(pi2)}")

# Use the new variables for hmm2
hmm2 = dhmm.HMM(3, 6, pi2, a2, b2) # Pass the new variables
print(f"DEBUG: hmm2.prior before train: {hmm2.prior}")
print(f"DEBUG: type(hmm2.prior) before train: {type(hmm2.prior)}")
hmm2.train([rolls2],iter=20) # Use rolls2 here

print (hmm2.viterbi_path(rolls))
print ('aic', hmm2.aic())
print (hmm2.transmat)
print (hmm2.prior)
print (hmm2.obsmat)

import pandas as pd
df = pd.read_csv('earthquakes.txt',sep='\s*',header=None,index_col=0)
data = df[1]
data.plot()
plt.title('Depremler')
plt.savefig('tser_hmm_04.png')

