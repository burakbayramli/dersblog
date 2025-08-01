import codecs, re, os, sys, shutil, json
import util, markdown2, glob, subprocess, numpy as np

dirs = ['algs','calc_multi','chaos','compscieng',
        'func_analysis','linear','ode', 'stat',
        'tser','vision','phy']

def doc_dirs(topdirs):
    curr = os.getcwd()
    print (curr)
    for topdir in topdirs:
        print (topdir)
        for subdir in sorted(os.listdir(curr + "/" + topdir)):
            print (subdir)
            if not os.path.isdir(curr + "/" + topdir + "/" + subdir): continue
            if "cover" in subdir or "000" in subdir : continue
            os.chdir(curr + "/" + topdir + "/" + subdir)
            mdfile = curr + "/" + topdir + "/" + subdir + "/" + subdir + ".md"
            shutil.copy(mdfile,"/tmp/out.md")
            title = get_title_from_md("/tmp/out.md")
            cmd = 'pandoc --template=/home/burak/Documents/classnotes/template.html -M title="%s" --mathjax=https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS_HTML-full -f markdown -t html /tmp/out.md -o /tmp/out.html' % title
            os.system(cmd)            
            cmd = "pandoc %s /home/burak/Documents/classnotes/metadata.yaml -t latex  -fmarkdown-implicit_figures -o %s" % ("/tmp/out.md","/tmp/out.pdf")
            os.system(cmd)
            pdffile = curr + "/" + topdir + "/" + subdir + "/" + subdir + ".pdf"
            htmlfile = curr + "/" + topdir + "/" + subdir + "/" + subdir + ".html"
            print ("copying to", mdfile)            
            shutil.copy("/tmp/out.pdf", pdffile) 
            shutil.copy("/tmp/out.html", htmlfile) 
            #break

def copy_files_and_dirs(fr,to,ignore_list):
    if ignore_list == None:
        ignore_list = []
    else:
        ignore_list = ignore_list.split(',')
    frdirs,frfiles =  ls(fr,ignore_list)
    todirs,tofiles = ls(to)

    tofilesdict = dict(tofiles)
    print ('create dirs')
    todirs_tmp = dict([(x.replace(fr,to),0) for x in todirs])
    diff = [x for x in frdirs if x.replace(fr,to) not in todirs_tmp]
    for x in diff:
        x=x.replace(fr,to)
        if os.path.exists(x) == False:            
            os.mkdir(x)

    print ('1 a files not in b')
    for (x,size) in frfiles:
        x_to=x.replace(fr,to)
        if x_to in tofilesdict and tofilesdict[x_to] != size: 
            print ('copying %s %s' % (x,x_to))
            shutil.copy(x,x_to)
        elif x_to not in tofilesdict: 
            print ('copying %s %s' % (x,x_to))
            shutil.copy(x,x_to)
            
    return frdirs, todirs

def ls(d,ignore_list=[]):
    print ('ls ignore lst', ignore_list)
    dirs = []; files = []
    for root, directories, filenames in os.walk(d):
        for directory in directories:
            path = os.path.join(root, directory)
            do_add = True
            for ignore in ignore_list:
                if ignore in path:
                    print ('ignoring', path); do_add = False
            if do_add: dirs.append(path)
        for filename in filenames: 
            path = os.path.join(root,filename)
            do_add = True
            for ignore in ignore_list:
                if ignore in path: do_add = False
            if do_add: files.append((path, os.path.getsize(path)))
    return dirs, files

def get_title_from_md(f):
    fin = codecs.open(f, encoding='utf8')
    line = fin.readline()
    fin.close()
    return line[2:].strip()

def title_sci(to):
    lecs = json.loads(open("lecs.conf").read())
    for dir in dirs:
        out = to + "/" + dir + "/index.html"
        fout = codecs.open(out,mode="w",encoding="utf-8")
        fout.write(util.html_head.replace("[title]",lecs['titles'][dir]))
        fout.write("<a href='%s'>PDF</a><br/><br/>" % lecs['pdfs'][dir])
        for subdir in sorted(os.listdir(dir)):
            if not os.path.isdir(dir + "/" + subdir): continue
            if "cover" in subdir or "000" in subdir : continue
            # read tex file, get header
            md = subdir + ".md"
            title = get_title_from_md(dir + "/" + subdir + "/" + md)
            html = subdir + "/" + util.filename_from_title(title) + ".html"        
            fout.write("<p><a href='%s'>%s</a><p/>" % (html,title))
        fout.write("<br/><a href='../index.html'>Yukarı</a><br/>")


def gen_html_sk():
    dirs, files = ls(os.getcwd() + "/sk")
    for (f,size) in files:
        if ".md" in f:
            path = os.path.dirname(f)
            fmd = os.path.basename(f)
            fhtml = os.path.basename(f).replace(".md",".html")
            update = True
            if os.path.isfile(path + "/" + fhtml):
                mdtime = os.path.getmtime(path + "/" + fmd)
                htmltime = os.path.getmtime(path + "/" + fhtml)
                if htmltime > mdtime: update = False
            if update:
                print ('Generating html for', f)
                title = get_title_from_md(f)
                content = open(path + "/" + fmd).read()
                res = util.html_head.replace("[title]","")
                res += markdown2.markdown(content, extras=['fenced-code-blocks'])
                res += util.bottom
                fout = open(path + "/" + fhtml, "w")
                fout.write(res)
                fout.close()
        
def title_sk(to):
    d = "sk"
    for year in range(2000,2026):
        if year == 2007: continue
        out = d + "/" + str(year) + "/index.md"
        fout = codecs.open(out,mode="w",encoding="utf-8")
        fout.write("# %s\n\n" % str(year))
        for f in sorted(glob.glob(d + "/" + str(year) + "/*/*.md")):
            fin = open(f)
            for line in fin.readlines():
                ff = f.replace(d, '')[1:]
                ff = ff.replace(str(year) + "/", "")
                ff = ff.replace(".md",".html")
                fout.write ("[%s](%s)\n\n" % (line[2:].strip(), ff))
                break
        fout.close()


def remove_sci_md(to):
    curr = to
    for topdir in dirs:
        for subdir in sorted(os.listdir(curr + "/" + topdir)):
            if not os.path.isdir(curr + "/" + topdir + "/" + subdir): continue
            if "cover" in subdir or "000" in subdir : continue
            os.chdir(curr + "/" + topdir + "/" + subdir)
            mdfile = curr + "/" + topdir + "/" + subdir + "/" + subdir + ".md"            
            print ('removing', mdfile)
            if os.path.exists(mdfile): os.remove(mdfile)
    
            
if __name__ == "__main__": 

    fr = os.getcwd()
    to = os.environ['HOME'] + "/Documents/dersblog"
    
    if sys.argv[1] == "test":
        if sys.argv[2] != "all": dirs = [sys.argv[2]]
        tmpto = "/tmp/cltest"
        if os.path.exists(tmpto) == False:            
            os.mkdir(tmpto)
            
        py_ignore_list = ['algs_045_probsolve','algs_135_convnet','compscieng_bpp40sph',
                          'compscieng_bpp80radio','phy_005_basics_05','stat_055_linreg',
                          'stat_085_multlev','tser_020_ar','tser_040_rwtst','vision_60track']
        
        frdirs, todirs = copy_files_and_dirs(fr, tmpto, ".git,.pdf,zwork")
        shutil.copy(".gitignore", to + "/.gitignore")         
        os.chdir(tmpto)
        for topdir in dirs:
            print (topdir)
            for subdir in sorted(os.listdir(to + "/" + topdir)):
                if not os.path.isdir(to + "/" + topdir + "/" + subdir): continue
                if "cover" in subdir or "000" in subdir : continue
                mdfile = tmpto + "/" + topdir + "/" + subdir + "/" + subdir + ".md"
                print (mdfile)
                foutname = tmpto + "/" + topdir + "/" + subdir + "/pout1111.py"
                print (foutname)
                fout = open(foutname,"w")
                fout.write("import numpy as np\nimport matplotlib.pyplot as plt\n")
                fname = sys.argv[1]
                content = open(mdfile).read()
                res = re.findall("```python(.*?)```", content, re.DOTALL)
                for x in res: fout.write(x)
                fout.close()
                os.chdir(tmpto + "/" + topdir + "/" + subdir)
                ignores = [x in subdir for x in py_ignore_list]
                if np.any(ignores):
                    print ("ignoring", subdir)
                    continue
                result = subprocess.run(['/home/burak/Documents/env3/bin/python', 'pout1111.py'], capture_output=True)
                if result.returncode != 0:
                    print (result)
                    exit()
                
    if sys.argv[1] == "doc":
        if len(sys.argv) < 3:
            # for single file, command run inside working dir
            currfile = os.path.basename(os.getcwd())
            currdir = os.path.dirname(os.getcwd())
            mdfile = currdir + "/" + currfile + "/" + currfile + ".md"
            htmlfile = currdir + "/" + currfile + "/" + currfile + ".html"
            pdffile = currdir + "/" + currfile + "/" + currfile + ".pdf"
            shutil.copy(mdfile,"/tmp/out.md")
            title = get_title_from_md("/tmp/out.md")
            cmd = 'pandoc --template=/home/burak/Documents/classnotes/template.html -M title="%s" --mathjax=https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS_HTML-full -f markdown -t html /tmp/out.md -o /tmp/out.html' % title
            os.system(cmd)
            cmd = "pandoc %s /home/burak/Documents/classnotes/metadata.yaml -t latex  -fmarkdown-implicit_figures -o %s" % ("/tmp/out.md","/tmp/out.pdf")
            os.system(cmd)
            shutil.copy("/tmp/out.pdf", pdffile) 
            shutil.copy("/tmp/out.html", htmlfile)
            exit()
        if sys.argv[2] == "all":
            # for all documents
            doc_dirs(dirs)
            exit()
        else:
            # for selected subdirectory
            doc_dirs([sys.argv[2]])
            exit()
    
    elif sys.argv[1] == "push":
        frdirs, todirs = copy_files_and_dirs(fr, to, ".git,.pdf,zwork")
        os.chdir(to)
        title_sci(to)
        for topdir in dirs:
            print (topdir)
            for subdir in sorted(os.listdir(to + "/" + topdir)):
                if not os.path.isdir(to + "/" + topdir + "/" + subdir): continue
                if "cover" in subdir or "000" in subdir : continue
                htmlfile = to + "/" + topdir + "/" + subdir + "/" + subdir + ".html"
                mdfile = to + "/" + topdir + "/" + subdir + "/" + subdir + ".md"
                title = get_title_from_md(mdfile)
                html_long = to + "/" + topdir + "/" + subdir + "/" + util.filename_from_title(title) + ".html"                
                print (htmlfile, html_long)
                shutil.copy(htmlfile, html_long)
                
        title_sk(to)
        gen_html_sk()
        remove_sci_md(to)
        exit()

    elif sys.argv[1] == "comb":
        pdfdir = sys.argv[2]
        pdfs = sorted(list(glob.glob(pdfdir + '/*/*.pdf')))
        pdfs = " ".join(pdfs)
        print (pdfs)
        home = os.environ['HOME']
        cmd = "pdfunite " + pdfs + " " + home + "/Downloads/" + pdfdir + ".pdf"
        os.system(cmd)

    elif sys.argv[1] == 'zip':
        os.system("zip /opt/Downloads/dotbkps/classnotes.zip -r /home/burak/Documents/classnotes/.git/")
        
