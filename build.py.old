# -*- coding: utf-8 -*-

#
# __TODO__: for html, put article title inside <title></title>
#
import os, sys, re, codecs, shutil, markdown, json, util

topdirs = ['algs','calc_multi','chaos','compscieng',
           'func_analysis','linear','ode', 'stat',
           'tser','vision','phy']

cfg = """
\\Preamble{xhtml}
\\Configure{HColor}{DarkGray}{\\#1A1A1A}
\\begin{document}
\\EndPreamble
"""

ad = '''
<br/>
<a href='..'>Yukarı</a>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href='../..'>Ana Menü</a>
<br/>
'''

TARGET_DIR = "/home/burak/Documents/dersblog"

def translit_low(c):
    res = c.lower()
    res = res.replace(u'ğ','g')
    res = res.replace(u'ş','s')
    res = res.replace(u'ı','i')
    res = res.replace(u'ç','c')
    res = res.replace(u'ü','u')
    res = res.replace(u'ö','o')
    return res

if __name__ == "__main__": 
 
    if len(sys.argv) < 2:
      print ("options: all | clean | html ")
      exit()  
    
    if sys.argv[1] == 'clean-light':
        os.system("find . -name _region_* | xargs rm -rf ")
        os.system("find . -name '*.log' | xargs rm -rf ")
        os.system("find . -name '*.aux' | xargs rm -rf ")
        os.system("find . -name '*.out' | xargs rm -rf ")
        os.system("find . -name '_minted*' | xargs rm -rf ")
        os.system("find . -name '_preview*' | xargs rm -rf ")
        os.system("find . -name '*ltxpng*' | xargs rm -rf ")

    if sys.argv[1] == 'clean':
        os.system("find . -name _region_* | xargs rm -rf ")
        os.system("find . -name '*.log' | xargs rm -rf ")
        os.system("find . -name '*.pdf' | xargs rm -rf ")
        os.system("find . -name '*.aux' | xargs rm -rf ")
        os.system("find . -name '*.out' | xargs rm -rf ")
        os.system("find . -name '_minted*' | xargs rm -rf ")
        os.system("find . -name '_preview*' | xargs rm -rf ")

    if sys.argv[1] == 'all':
        for x in topdirs:
            if ".git" in x: continue
            if os.path.isdir(x):
                os.chdir(x)
                print ("building", x)
                os.system("python build.py all")
                os.system("python build.py")
                os.chdir("..")

    if sys.argv[1] == 'html':
        
        fr = os.getcwd()
        cmd = "python /home/burak/Documents/kod/rsync.py '%s' '%s' --ignore-list=.md,.git,.zip,.pdf,.apk,.exe,.stl,.pygtex,.key" % (fr, TARGET_DIR)
        print (cmd)
        os.system(cmd)
        shutil.copy(".gitignore", TARGET_DIR)
        shutil.copy("/home/burak/Documents/Dropbox/bkps/googleb21e08d7627545a2.html", TARGET_DIR)        
        lecs = json.loads(open("lecs.conf").read())
        for topdir in topdirs:
            print ('main',topdir)
            print ('pdf', lecs['pdfs'][topdir])
            dir = TARGET_DIR + "/" + topdir
            print ('dir',dir)
            fout = codecs.open(dir + "/index.html",mode="w",encoding="utf-8")
            fout.write("<html>\n")
            fout.write(u"""
            <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            <meta name="description" content="ODE, Fizik, Çok Değişkenli Calculus, Lineer Cebir, Hesapsal Bilim, İstatistik, Fonksiyonel Analiz, Yapay Zeka, Zaman Serisi Analizi ders notlari.">
            <title>%s</title>
            </head>  
            <body>                    
            <p>
            <a href='..'>Ana Menü</a>
            &nbsp;&nbsp;&nbsp;&nbsp;
            <a href='%s'>PDF</a>
            </p>
            <p>
            <h4>%s</h4>
            </p>
            """ % (lecs['titles'][topdir],lecs['pdfs'][topdir],lecs['titles'][topdir]) )
            
            for subdir in sorted(os.listdir(dir)):
                if not os.path.isdir(dir + "/" + subdir): continue
                print ('subdir',subdir)
                if "cover" in subdir or "000" in subdir : continue
                print (dir + "/" + subdir)
                # read tex file, get header
                ff = dir + "/" + subdir + "/" + subdir + ".tex"
                if "__pycache__" in ff: continue
                fin = codecs.open(ff, encoding='utf8')
                content = fin.read()
                title = re.findall(u"begin.*?document.*?\n(.*?)\n",content,re.DOTALL)[0]
                url = translit_low(title)
                url = url.replace(" ","_")
                url = url.replace("(","_")
                url = url.replace("'","_")
                url = url.replace(")","_")
                url = url.replace("/","_")
                url = url.replace("-","")
                url = url.replace(",","")
                url = url.replace("?","")
                url = url.replace("̇","")
                url = url + ".html"
                print ('the url is', subdir + "/" + url)
                
                line = "<a href='%s'>%s</a><br/><br/>" % (subdir + "/" + url, title)
                print (line)
                fout.write(line)
                fout.write("\n")
                fin.close()
                
                print ('chdir', dir + "/" + subdir)                
                os.chdir(dir + "/" + subdir)

                if os.path.isfile(subdir + ".html"): 
                    textime = os.path.getmtime(subdir + ".tex")
                    htmltime = os.path.getmtime(subdir + ".html")
                    if htmltime > textime:
                        print ("HTML exists.. skipping")
                        continue

                texfile = subdir + '.tex'
                htmlfile = subdir + '.html'
                util.tex_mathjax_html(texfile, htmlfile, title)
                shutil.copy(htmlfile, url)
                                
            fout.write("</body>\n")
            fout.write("</html>\n")
            fout.close()
            #break
                      
