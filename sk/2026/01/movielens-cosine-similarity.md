# Movielens Filmleri, Kosinus Benzerligi, Tavsiyeler

Kosinüs benzerliği konusu [1]'de işlendi. Bu benzerlik ölçütü iki
vektörün birbirine çok boyutlu açısal yakınlığını hesaplar. Bunun için
tek gereken bu iki vektörün arasındaki noktasal çarpım, ve her iki
vektörün büyülüklerinin (norm) çarpımı.

[1] belgesinde bu hesabın hızlı yapılabilmesi için seyrek matris
kavramından bahsedildi. Fakat aslında biz python kütüphanelerinden
gelen seyrek matris formatları yerine kendi seyrek matris (vektör)
yapımızı oluşturabiliriz.

İlerlemeden önce noktasal çarpımın ne olduğunu hatırlayalım, aynı
boyuttaki iki vektörün birbirine tekabül eden her değeri çarpılır ve
bu çarpımlar birbirine toplanır.

```python
a = np.array([2,4,6,7,4,9,4,3,2,5,6,3,1,2])
b = np.array([1,3,6,8,1,1,4,3,3,4,1,5,4,9])

float (np.sum([x*y for x,y in zip(a,b)]))
```

```text
Out[1]: 213.0
```

Üstteki kodda `zip` ile her iki vektörün öğeleri gezildi, ve tarif
edilen işlemler yapıldı.

Fakat şimdi Movielens film not verisini düşünelim. Bu kayıtlarda
binlerce film var, ve herhangi bir kullanıcının tüm filmleri seyredip
not vermiş olması imkansız. Seyretmiş olsa bile not vermemiş olabilir.
Çoğunlukla bir kullanıcı 10-15 filme not vermiştir, belki
yüzlerce. Her durumda da not sayısı az. Yani üstteki örnek veri
aslında suna benzeyebilir,

```python
a = np.array([2,0,6,0,0,0,0,0,0,0,0,0,0,0,3,1,2])
b = np.array([0,3,1,0,0,0,0,0,0,0,3,3,4,1,1,2,0])

float (np.sum([x*y for x,y in zip(a,b)]))
```

```text
Out[1]: 11.0
```

Görüldüğü her iki vektörde de gibi bir sürü sıfır var. Noktasal
çarpımda sıfır çarpı herhangi bir diğer sıfır olduğu için, herhangi
bir hücrede sıfır varsa o noktadaki hesap sıfır olur, toplama etkisi
olmaz. Ve dikkat üstteki örnekte sıfır olmayan çoğu değer çakışmıyor
(ancak o zaman toplama katkı olabilir), mesela `a` 1'inci öğe 2 ama
`b` aynı öğe sıfır, 'b' 2'inci öğe 3 ama onun eşi `a` uzerinde sıfır,
demek ki ilk iki öğenin toplama hiçbir katkısı olmayacak. Keşke sıfır
olan hücreleri direk atlayabilseydik, değil mi?

Seyrek matris formatları bunu yapmamızı sağlar. Kütüphane
`scipy.sparse` içinde bu amaç için pek çok kodlar vardır. Fakat biz
kendi pişirdiğimiz kodlar ile de aynı sonucu elde edebiliriz.

Bir vektör yerine bir sözlük (dictionary) yapısı kullanarak bunu
yapabilirdik. Sözlük anahtarı üstteki vektörde sıfır olmayan değerin
indisi olabilir. Yeni "vektörlerimiz" alttaki gibi olur,

```python
da = dict({0: 2, 2:6, 14:3, 15:1, 16:2})
db = dict({1: 3, 2:1, 10:3, 11:3, 12:4, 13:1, 14:1, 15:2})
```

```python
res = sum(db[key]*da.get(key, 0) for key in db)
print (res)
```

```text
11
```





```python
content = open("movrecom.py").read()
print(content.replace('\n', '\r\n'))
```

```text
#
# Recommend movies based on Grouplens ratings file
#
# https://grouplens.org/datasets/movielens/latest/
#
# Download the full file, and unzip in a known
# location update the d variable below
#
from scipy.sparse import csr_matrix
import scipy.sparse.linalg, json
import pandas as pd, numpy as np
import os, sys, re, csv

csv.field_size_limit(sys.maxsize)

d = "/opt/Downloads/ml-32m"


def sim():
    fin = d + "/user_movie.txt"
    picks = pd.read_csv(os.environ['HOME'] + '/Documents/kod/movpicks.csv',index_col=0).to_dict('index')
    skips = pd.read_csv(os.environ['HOME'] + '/Documents/kod/movskips.csv',index_col=0).to_dict('index')
    mov = pd.read_csv(d + "/movies.csv",index_col="title")['movieId'].to_dict()
    genre = pd.read_csv(d + "/movies.csv",index_col="movieId")['genres'].to_dict()
    mov_id_title = pd.read_csv(d + "/movies.csv",index_col="movieId")['title'].to_dict()
    picks_json = dict((mov[p],float(picks[p]['rating'])) for p in picks if p in mov)
    picks_norm = np.sqrt(sum(v**2 for v in picks_json.values()))
    res = []
    with open(fin) as csvfile:   
        rd = csv.reader(csvfile,delimiter='|')
        for i,row in enumerate(rd):
            jrow = json.loads(row[1])
            jrow_norm = np.sqrt(sum(v**2 for v in jrow.values()))
            dp = sum(jrow[key]*picks_json.get(int(key), 0) for key in jrow)
            dp = dp / ((picks_norm*jrow_norm)+1e-10)
            res.append([row[0],dp])
            if i % 1e4 == 0: print (i,dp)
          

    df = pd.DataFrame(res).set_index(0)
    df = df.sort_values(by=1,ascending=False).head(400)
    df = df.to_dict()[1]

    recoms = []
    with open(fin) as csvfile:   
        rd = csv.reader(csvfile,delimiter='|')
        for i,row in enumerate(rd):
            jrow = json.loads(row[1])
            if str(row[0]) in df:
                for movid,rating in jrow.items():
                    if int(movid) not in mov_id_title: continue 
                    fres = re.findall('\((\d\d\d\d)\)', mov_id_title[int(movid)])
                    if rating >= 4 and \
                       mov_id_title[int(movid)] not in picks and \
                       mov_id_title[int(movid)] not in skips and \
                       'Animation' not in genre[int(movid)] and \
                       'Documentary' not in genre[int(movid)] and \
                       len(fres)>0 and int(fres[0]) > 2010: \
                       recoms.append([mov_id_title[int(movid)],rating*df[row[0]]])

    df = pd.DataFrame(recoms)
    df = df.sort_values(1,ascending=False)
    df = df.drop_duplicates(0)
    df.to_csv("/opt/Downloads/movierecom3.csv",index=None,header=False)
        
if __name__ == "__main__":  
    
    if len(sys.argv) < 2:
        print ("Usage movrecom.py [sim]")
        exit()

    if sys.argv[1] == "sim":
        sim()
                

```





[devam edecek]

Kodlar

[movprep.py](../../stat/stat_140_pmf/movprep.py)


Kaynaklar

[1] Bayramli, <a href="../../../stat/stat_137_collab/stat_137_collab.html">Toplu Tavsiye (Collaborative Filtering), Filmler, SVD ile Boyut İndirgeme</a>

