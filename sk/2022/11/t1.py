import pandas as pd
import os, numpy as np, util

class BucketJob:
    def __init__(self,B):
        self.ci = -1
        self.B = B
        M = 474391
        P = int(M / 4)
        self.bins = np.array([0, P, 2*P, 3*P, M])
        self.fout = open("/tmp/B-%d-%d.csv" % (self.B,self.ci), "w")
    def bucket(self, id): # id hangi kutuya ait?
        return np.argmax(self.bins > id)-1        
    def exec(self,line):
        toks = line.strip().split(',')
        if self.bucket(float(toks[0])) == self.B:
           self.fout.write(line)
    def post(self):
        # diske yaz
        self.fout.close()


class BucketSortJob:
    def __init__(self,B):
        self.ci = -1
        self.res = [] # satirlari burada biriktir
    def exec(self,line):
        toks = line.strip().split(',')
        self.res.append(toks)
    def post(self):
        df = pd.DataFrame(self.res) # birikmis satirlarla DataFrame yarat
        df[0] = pd.to_numeric(df[0])
        df = df.sort_values(by=0) # hafizada sirala
        # diske yaz
        df.to_csv("/tmp/B-%d-sorted.csv" % (self.ci),index=None,header=None)



util.process(file_name='/tmp/input.csv', ci=0, N=4, hookobj = BucketJob(B))
        
# seri isledi ama nihai ortamda paralel isler
#for B in range (4):
#    util.process(file_name='/tmp/input.csv', ci=0, N=4, hookobj = BucketJob(B))
#    util.process(file_name='/tmp/input.csv', ci=1, N=4, hookobj = BucketJob(B))
#    util.process(file_name='/tmp/input.csv', ci=2, N=4, hookobj = BucketJob(B))
#    util.process(file_name='/tmp/input.csv', ci=3, N=4, hookobj = BucketJob(B))
