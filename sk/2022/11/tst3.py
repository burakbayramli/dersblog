import os, numpy as np, util

class RandomProjJob:
    def __init__(self,ci):
        self.ci = ci
        self.k = 7
        self.outfile = open("/tmp/Y-%d.csv" % self.ci, "w")        
    def exec(self,line):
        s = np.zeros(self.k)
        toks = line.strip().split(';')
        row = np.array([np.float(x) for x in toks[1:]])
        # degisik veri parcalari degisik rasgele matrisler uretsin
        np.random.seed(0) 
        for elem in row: s += elem*np.random.normal(0,1,self.k) 
        s = ";".join(map(str, s))
        self.outfile.write(s)
        self.outfile.write("\n")
        self.outfile.flush()
        
    def post(self):
        self.outfile.close()

util.process(file_name='../../../linear/linear_app10rndsvd/w1.dat', N=2, hookobj = RandomProjJob(0))
util.process(file_name='../../../linear/linear_app10rndsvd/w1.dat', N=2, hookobj = RandomProjJob(1))
