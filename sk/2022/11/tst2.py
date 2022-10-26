from multiprocessing import Process
from timeit import default_timer as timer
from datetime import timedelta
import os, numpy as np, util

class ATAJob:
    def __init__(self,D):
        self.C = np.zeros((D,D))
        self.ci = -1
    def exec(self,line):
        tok = line.split(';')
        vec = np.array([float(x) for x in tok])
        self.C = self.C + np.outer(vec, vec)
    def post(self):
        outfile = "/tmp/C-%d.csv" % self.ci
        print (self.ci)
        np.savetxt(outfile, self.C, delimiter=';',fmt='%1.6f')
        
util.process(file_name='/tmp/A.csv', ci=0, N=2, hookobj = ATAJob(20))
util.process(file_name='/tmp/A.csv', ci=1, N=2, hookobj = ATAJob(20))

C0 = np.loadtxt("/tmp/C-0.csv",delimiter=';')
C1 = np.loadtxt("/tmp/C-1.csv",delimiter=';')

C = C0 + C1

np.savetxt("/tmp/C-final.csv", C, delimiter=';',fmt='%1.6f')
