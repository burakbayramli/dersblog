import os

def merge_sorted(file1,file2,outfile):
    fout = open(outfile, "w")

    f1 = open(file1, 'r')
    f2 = open(file2, 'r')
    s1 = os.path.getsize(file1)
    s2 = os.path.getsize(file2)
    print (s1,s2)
    
    l1 = f1.readline().strip()
    toks1 = l1.split(',')
    l2 = f2.readline().strip()
    toks2 = l2.split(',')
    
    # herhangi bir dosyada sona gelene kadar donguyu islet
    while (f1.tell() < s1 and f2.tell() < s2):
        ...
        
        
