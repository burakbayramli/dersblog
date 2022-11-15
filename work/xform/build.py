import os, sys

if len(sys.argv) == 1 or sys.argv[1] == 'tex':
    os.system("pdflatex xform1.tex")
if len(sys.argv) == 1 or sys.argv[1] == 'zip':
    os.system("zip -r /home/burak/Downloads/inva.zip PRIMEarxiv.sty xform1.tex ")
       
