# Paralel Veri Analizi Istatistik

Eşzamanlı olarak veri işleme, analizi tekniklerinin temel yaklaşımını
[2]'de gördük, orada ve bu yazıda kullanacağımız ana yapı şöyle;
İşlenecek çok büyük bir CSV dosyası var, her çekirdek (birden fazla
ise) her makina by dosyaya direk erisebilir, paralel işlemler bu
dosyanın farklı kısımlarını ayna anda işleyebilmek üzerinden
gerçekleşecektir. Tercihimiz her zaman satır satır mesafe katedebilen
algoritmalardır, yani verinin tek bir satırına bakarak bir bir
katmadeğer elde edebilen, sonuca daha yaklaşabilen algoritmalar.

### Sıralama (Sorting)

Yontem 1

Eldeki makina, çekirdek N ise, N tane kutu yaratırız, ve hangi kolon
bazında sıralama yapıyorsak, mesela bir kimlik (id) diyelim, o
kimliklerin sırasal olarak 1,2,3, kutusuna düşmesini sağlarız. Eğer
maksimum 1000 kimliği var ise, ve N=4 için, kmliklerden 0 ile 250
arası 1'inci kutuya, 251 ile 500 arası 2'inci kutuya vb gibi gitmeli.
Bu ilk tarama 4 tane yeni daha ufak dosya yaratır.

Ardından paralel olarak her ufak dosyayı hafızada sıralarız.

Bu bitince sıralanmış dosyaları alt alta ekleriz / yapıştırırız
(append) ve sıralanmış dosya elde edilir.

Disk bazlı işlemleri göstermek için sentetik veri üretelim, sadece bir
kimlik (id) kolonu, iki tane isim, adres için metinsel iki kolon.

```python
import util
util.create_sort_synthetic(1000000)
```

```python
! head -5 /tmp/input.csv
```

```text
83473,nnnnnnnnnnnnnnnnnnnn,nnnnnnnnnnnnnnnnnnnn
46657,nnnnnnnnnnnnnnnnnnnn,nnnnnnnnnnnnnnnnnnnn
98157,HHHHHHHHHHHHHHHHHHHH,HHHHHHHHHHHHHHHHHHHH
111152,CCCCCCCCCCCCCCCCCCCC,CCCCCCCCCCCCCCCCCCCC
```

1 milyon satırlık karışık bir veri oldu.

```python
import pandas as pd
df = pd.read_csv("/tmp/input.csv",index_col=0)
```

```python
print (df.index.min(), df.index.max(), np.mean(df.index))
```

```text
0 474390 79792.60683260683
```

Alttaki kodda bu rakamlara bakarak bazı sınırları deneme/yanilma ile
tanımladık, fakat profosyonel ortamda bu sınırları bulmak ta ayrı bir
paralel süreç olabilirdi.


```python
import os, numpy as np, util

class BucketJob:
    def __init__(self):
        self.ci = -1
        self.res = [] # satirlari burada biriktir
        self.bins = np.array([0, 50000, 80000, 130000, 474391])
    def bucket(self, id): # id hangi kutuya ait?
        return np.argmax(self.bins > id)-1        
    def exec(self,line):
        toks = line.strip().split(',')
        if self.bucket(float(toks[0])) == self.ci:
           self.res.append(toks)
    def post(self):
        df = pd.DataFrame(self.res) # birikmis satirlarla DataFrame yarat
        df[0] = pd.to_numeric(df[0])
        df = df.sort_values(by=0) # hafizada sirala
        # diske yaz
        df.to_csv("/tmp/L-%d.csv" % self.ci,index=None,header=None)

# seri isledi ama nihai ortamda paralel isler
util.process(file_name='/tmp/input.csv', ci=0, N=4, hookobj = BucketJob())
util.process(file_name='/tmp/input.csv', ci=1, N=4, hookobj = BucketJob())
util.process(file_name='/tmp/input.csv', ci=2, N=4, hookobj = BucketJob())
util.process(file_name='/tmp/input.csv', ci=3, N=4, hookobj = BucketJob())
```

Artık parçaları pür Unix komutu ile birleştirebiliriz, `L-0.csv`,
`L-1.csv`,..  birbirine yapıştırılıyor yani..

```python
! cat /tmp/L-* > /tmp/Lfinal.csv
```

Sonuç `/tmp/Lfinal.csv` içinde. Sıralanmış bir halde çünkü ilk kutudaki
satırların ikinci kutudaki satırlardan önce geleceğini biliyoruz. Kutulamayı
buna göre yaptık. 

Yöntem 2

Bu yöntem alternatif değil aslında, belki farklı durumlarda
kullanılacak bir yaklaşım. Yöntem 2 bize daha az hafıza ile daha büyük
dosyaları tek makinada sıralama şansı veriyor. Paralellik hala var,
fakat son birleştirme aşaması her ne kadar disk yoğunluklu olsa da tek
bir makinada yapılmalı.

Bu yöntemle dosyanın ufak parçalarını yine hafızada sıralarız, sonra
bir süreç o parçaları disk bazlı (satır satır) birleştirir. Sıralanmış
parçaların birleşmiş ve hala sıralı halde olması için bir algoritma,

* Her iki parçanın başına git

* Bir döngü içinde her ikisinin sıradaki en küçük parçasına bak

* En ufak olanını al, yeni listeye ekle, bunu tekrarla

* Listeler farklı boylarda olabilir, bir liste öncekinden önce biterse
  önemli değil, kalan listeyi olduğu gibi yeni listeye ekle.

Altta bu işlemleri gösteren bir örnek görüyoruz.

![](sort1.png)

Listeden bir öğe alındığında o öğeyi "çıkartılmış" gibi gösterdik,
fakat kodlama bağlamında yapılan bir indisin ilerletilmesinden ibaret.

Tarif edilen birleştirmenin işlediğini alttaki ufak kodda
görebiliriz. İki tane rasgele veri içeren liste yarattık, onları önce
hafızada sıraladık, sonra teker teker her birinden en ufak öğeyi
alarak yeni listeyi oluşturduk, ve yeni liste otomatik olarak
sıralanmış hale geldi.

```python
import numpy as np, random, util

def chunkmerge():
    N1 = 5; N2 = N1*2
    
    # rasgele sayilarla iki liste uret
    arr1 = [random.randint(0,100) for i in range(N1)]
    arr2 = [random.randint(0,100) for i in range(N2)]
    
    arr1 = sorted(arr1) # parcayi hafizada sirala
    arr2 = sorted(arr2) # parcayi hafizada sirala
    print ('liste 1',arr1)
    print ('liste 2',arr2)

    res = [] # sonuclar
    
    i=0; j=0 # her iki listenin farkli indisi var
    while i<N1 and j<N2:
        # her iki listenin islenmemis en kucuk degerine bak, arr1[i], arr2[j]
        # kucuk olanini al
        if arr1[i] < arr2[j]:
            res.append(arr1[i])
            i = i + 1
        else:
            res.append(arr2[j])
            j = j + 1
            
    # kalan ogeleri direk transfer et
    while i<N1:
        res.append(arr1[i])
        i = i + 1
    while j<N2:
        res.append(arr2[j])
        j = j + 1
    print ('siralanmis liste',res)
    # iki listeyi birlestirip klasik sekilde sirala
    arrsorted = sorted(arr1 + arr2)
    # ayni sonuc mu
    print ('Siralama isledi mi?',arrsorted == res)

chunkmerge()   
```

```text
liste 1 [2, 33, 43, 49, 83]
liste 2 [5, 29, 32, 48, 52, 59, 60, 73, 81, 93]
siralanmis liste [2, 5, 29, 32, 33, 43, 48, 49, 52, 59, 60, 73, 81, 83, 93]
Siralama isledi mi? True
```

Nihai kod üstteki mantığı dosya satırları için yapar, iki dosyadan
satırlar teker teker alınır, döngü içinde kimlikleri birbiri ile
karşılaştırır, hangi dosyadan gelen kimlik daha küçük ise onun satırı,
o dönüşte, çıktıya yazılır. Bir dosya bitene kadar bu devam eder, sonra
kalan dosyanin satırları direk çıktıya yazılır. 

Bu yaklaşımla diyeli dört parça L0,L1,L2,L3 yarattık, L0,L1 birleşimi
bir süreçte, L2,L3 birleşimi ayrı bir süreçte yapılabilir. Fakat son kalan
nihai iki dosyanin birleşimi tek bir süreç tarafından yapılmalı.

Satırsal birleştirme tekniği dediğimiz gibi farklı makinalarda tam
paralellikten çok bir makinanın hafızasından fazla büyük bir dosyayı
sıralayabilmesini sağlar.

### Kümeleme (KMeans)

Daha önce [1] yazısında bu işi eşle/indirge, Hadoop ortamında nasıl
yapacağımızı gördük. Eğer [2]'deki yöntemi kullanmak istiyorsak, yani
altyapı bir veriyi herhangi bir kritere göre (çoğunlukla basit bloklar
üzerinden) bölmemizi sağlıyor ve her bölüm üzerinde ayrı bir süreç
işliyor, o zaman bazı kavramlarda birkaç değişiklik gerekir. 

Kaynaklar

[1] [Paralel KMeans, Hadoop](2013/10/paralel-kmeans-hadoop.html)

[2] Bayramli, [Paralel, Satır Bazlı Dosya İşlemek](../../2016/02/toptan-islemler-paralelizasyon.html)

[3] Wikipedia, [External Sorting](https://en.wikipedia.org/wiki/External_sorting)

[4] https://en.wikipedia.org/wiki/K-way_merge_algorithm

[5] https://stackoverflow.com/questions/29494594/sorting-data-with-space-contrainsts

