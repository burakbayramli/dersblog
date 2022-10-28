import os, numpy as np, util
import pandas as pd

df = pd.read_csv("/tmp/input.csv",index_col=0)

class BucketJob:
    def __init__(self):
        self.ci = -1
        self.res = [] # satirlari burada biriktir
        self.bins = np.array([0, 118597, 237195, 355792, 474391])
    def bucket(self, id):
        return np.argmax(self.bins > id)-1        
    def exec(self,line):
        toks = line.strip().split(',')
        if self.bucket(float(toks[0])) == self.ci:
           self.res.append(toks)
    def post(self):
        df = pd.DataFrame(self.res) # birikmis satirlarla DataFrame yarat
        df[0] = pd.to_numeric(df[0])
        df = df.sort_values(by=0) # hafizada sirala
        # diske yaz
        df.to_csv("/tmp/L-%d.csv" % self.ci,index=None,header=None)
        
util.process(file_name='/tmp/input.csv', ci=0, N=4, hookobj = BucketJob())
