import os, sys

def process(file_name,ci,N,lineobj):
    file_size = os.path.getsize(file_name)
    print (file_size)
    beg = 0
    chunks = []
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
            lineobj.exec(line)
            if f.tell() > c[1]: break
        f.close()
        lineobj.post()

if __name__ == "__main__":

    class Job:
        def __init__(self):
            self.res = []
        def exec(self,line):
            tok = line.split(',')
            self.res.append(tok)
        def post(self):
            print (self.res)
    
    file_name = sys.argv[1]
    ci = int(sys.argv[2])
    N = int(sys.argv[3])
    #process(file_name,ci,N,print)
    j = Job()
    process(file_name,ci,N,j)
    
