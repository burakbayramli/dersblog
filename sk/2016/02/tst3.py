import os, threading
from multiprocessing import Process

def process(file_name,ci,N,hookobj):
    file_size = os.path.getsize(file_name)
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
            hookobj.exec(line)
            if f.tell() > c[1]: break
        f.close()
        hookobj.post()

if __name__ == "__main__":

    class SimpleJob:
        def __init__(self):
            self.res = []
        def exec(self,line):
            tok = line.split(',')
            self.res.append(tok)
        def post(self):
            print (self.res)

    
    thread1 = threading.Thread(target=process(file_name='in2.csv', ci=0, N=2, hookobj = SimpleJob()))
    thread2 = threading.Thread(target=process(file_name='in2.csv', ci=1, N=2, hookobj = SimpleJob()))
    
    thread1.start()
    thread2.start()
    
    p1 = Process(target=process(file_name='in2.csv', ci=0, N=2, hookobj = SimpleJob()))
    p2 = Process(target=process(file_name='in2.csv', ci=1, N=2, hookobj = SimpleJob()))
    p1.start()
    p2.start()
