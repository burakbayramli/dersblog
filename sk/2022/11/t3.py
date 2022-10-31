import pandas as pd
import os, numpy as np, util

class BucketJob:
    def __init__(self,B,ci):
        self.B = B
        self.ci = ci
        self.bins = np.array([0, 50000, 80000, 130000, 474391])
        print (self.B,self.ci)
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

for B in range(4):
    util.process(file_name='/home/burak/Downloads/input.csv', N=4, hookobj = BucketJob(B,0))
    util.process(file_name='/home/burak/Downloads/input.csv', N=4, hookobj = BucketJob(B,1))
    util.process(file_name='/home/burak/Downloads/input.csv', N=4, hookobj = BucketJob(B,2))
    util.process(file_name='/home/burak/Downloads/input.csv', N=4, hookobj = BucketJob(B,3))
        
