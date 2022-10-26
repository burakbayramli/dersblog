from multiprocessing import Process
from timeit import default_timer as timer
from datetime import timedelta
import os, numpy as np

def process(file_name,ci,N,hookobj):
    file_size = os.path.getsize(file_name)
    beg = 0
    chunks = []
    hookobj.ci = ci
    for i in range(N):
        with open(file_name, 'r') as f:
            s = int((file_size / N)*(i+1))
            f.seek(s)
            f.readline()
            end_chunk = f.tell()-1
            chunks.append([beg,end_chunk])
            f.close()
        beg = end_chunk+1
    c = chunks[ci]
    with open(file_name, 'r') as f:
        f.seek(c[0])
        while True:
            line = f.readline()
            hookobj.exec(line)
            if f.tell() > c[1]: break
        f.close()
        hookobj.post()
        
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
        
process(file_name='/tmp/A.csv', ci=0, N=2, hookobj = ATAJob(20))
process(file_name='/tmp/A.csv', ci=1, N=2, hookobj = ATAJob(20))

C0 = np.loadtxt("/tmp/C-0.csv",delimiter=';')
C1 = np.loadtxt("/tmp/C-1.csv",delimiter=';')

C = C0 + C1

np.savetxt("/tmp/C-final.csv", C, delimiter=';',fmt='%1.6f')
