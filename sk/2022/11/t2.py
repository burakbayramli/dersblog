import pandas as pd, glob
import os, numpy as np, util

for B in range(4):
    dfs = [pd.read_csv('/tmp/B-%d-%d.csv' % (B,i),header=None) for i in range(4)]
    df = pd.concat(dfs,axis=0)
    df = df.sort_values(by=0)
    df.to_csv("/tmp/B-%d-sorted.csv" % B, header=None,index=None)
