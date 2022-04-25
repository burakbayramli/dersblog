import os, sys, re, codecs, shutil, markdown
import glob, os, sys

TARGET_DIR = "/home/burak/Documents/dersblog/sk"

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

if __name__ == "__main__": 
 
    if len(sys.argv) < 2:
        print ("options: html | years ")
        exit()

    if sys.argv[1] == 'clean-html2':
        dirs, files = ls(os.getcwd())
        for (f,size) in files:
            if ".md" in f:
                path = os.path.dirname(f)
                fmd = os.path.basename(f)
                fhtml = os.path.basename(f).replace(".md",".html")
                if os.path.isfile(path + "/" + fhtml):
                    print ('Erasing', path + "/" + fhtml)
                    os.remove(path + "/" + fhtml)
        
    if sys.argv[1] == 'html2':

        dirs, files = ls(os.getcwd())
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
                    content = open(path + "/" + fmd).read()
                    res = markdown.markdown(content, extensions=['fenced_code'])
                    fout = open(path + "/" + fhtml, "w")
                    fout.write(res)
                    fout.close()
                
    if sys.argv[1] == 'copy':

        shutil.copy("_config.yml","/home/burak/Documents/dersblog")

        ignore = " --ignore-list=.git,.zip,.pdf,out.html,.apk,.stl,.key"
        fr = os.getcwd()
        cmd = "python /home/burak/Documents/kod/rsync.py '%s' '%s'  --delete 1" % (fr, TARGET_DIR)
        cmd += ignore
        print (cmd)
        os.system(cmd)

    if sys.argv[1] == 'years':
        for year in range(2000,2023):
            if year == 2007: continue
            os.system("echo '# %d\n' > %d/index.md" % (year,year))
            os.system("python -u gen.py %d >> %d/index.md" % (year,year))

