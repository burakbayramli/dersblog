from multiprocessing import Process
from timeit import default_timer as timer
from datetime import timedelta
import os, numpy as np

def process(afile,bfile,ci,N,obj,skip_lines=0):
    file_size = os.path.getsize(afile)
    obj.afile = afile
    obj.B = np.loadtxt(bfile,delimiter=';')
    obj.ci = ci
    cname = "%s/C-%d.csv" % (os.path.dirname(afile), ci)
    obj.outfile = open(cname, "w")
    
    with open(afile, 'r') as f:
        for j in range(skip_lines): f.readline()
        beg = f.tell()
        f.close()
    chunks = []
    for i in range(N):
        with open(afile, 'r') as f:
            s = int((file_size / N)*(i+1))
            f.seek(s)
            f.readline()
            end_chunk = f.tell()-1
            chunks.append([beg,end_chunk])
            f.close()
        beg = end_chunk+1
    c = chunks[ci]
    with open(afile, 'r') as f:
        f.seek(c[0])
        while True:
            line = f.readline()
            obj.exec(line) # process the line
            if f.tell() > c[1]: break
            #break
        f.close()
        obj.post()

class MultJob:
    def __init__(self):
        self.afile = "" # proccessor sets it
        self.B = "" # proccessor sets it
        self.ci = -1 # proccessor sets it
        self.outfile = None # proccessor sets it
    def exec(self,line):        
        vec = np.array([np.float(x) for x in line.strip().split(";")])
        vec = np.reshape(vec, (len(vec),1))
        res = (vec * self.B).sum(axis=0).tolist()  
        res = ";".join(map(str, res))
        self.outfile.write(res)
        self.outfile.write("\n")
        self.outfile.flush()
    def post(self):
        self.outfile.close()
        
def runjob():
        
    dir = '/mnt/3d1ece2f-6539-411b-bac2-589d57201626/home/burak/Downloads'
    afile = dir + "/" + "A.csv"
    bfile = dir + "/" + "B.csv"

    start = timer()
       
    N = 4 # number of parallel tasks
    ps = [Process(target=process,args=(afile, bfile, i, N, MultJob(),1)) for i in range(N)]
    for p in ps: p.start()
    for p in ps: p.join()
    end = timer()
    print('elapsed time', timedelta(seconds=end-start))

    
runjob()        


# elapsed time 0:00:55.157166 , M = 1*1000*1000; D = 100; N = 30
