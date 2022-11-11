import os, sys

if len(sys.argv) == 1 or sys.argv[1] == 'tex':
    os.system("pdflatex linpar4.tex")
if len(sys.argv) == 1 or sys.argv[1] == 'zip':
    os.system("zip -r /home/burak/Downloads/linpar6.zip PRIMEarxiv.sty linpar4.tex mapreduce1.jpg mult1.jpg splitprocess.jpg")
       
