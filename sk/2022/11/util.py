import random, pandas as pd, string, uuid
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
        

def create_sort_synthetic(N):
    M = len(string.ascii_letters)
    ids = [int(np.abs(np.random.randn()*100000)) for i in range(N)]
    def stringify(x):
       return "".join([string.ascii_letters[x % M] for i in range(20)])
    names = [stringify(id) for id in ids]
    d = {"id": ids, "name": names, "address": names}
    df = pd.DataFrame(d)
    df.to_csv('/tmp/input.csv',index=None)    

   
