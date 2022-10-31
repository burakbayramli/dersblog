# Paralel Veri Analizi Istatistik

Eşzamanlı olarak veri işleme, analizi tekniklerinin temel yaklaşımını
[2]'de gördük, orada ve bu yazıda kullanacağımız ana yapı şöyle;
İşlenecek çok büyük bir CSV dosyası var, her çekirdek (birden fazla
ise) her makina by dosyaya direk erişebilir, paralel işlemler bu
dosyanın farklı kısımlarını aynı anda işleyebilmek üzerinden
gerçekleşecektir. Tercihimiz her zaman satır satır mesafe katedebilen
algoritmalardır, yani verinin tek bir satırına bakarak bir bir
katmadeğer elde edebilen, sonuca daha yaklaşabilen algoritmalar.

### Sıralama (Sorting)

Yöntem 1

- B tane kutu yaratırız, ve hangi kolon bazında sıralama yapıyorsak,
  mesela bir kimlik (id) diyelim, o kimliklerin büyüklük olarak 1,2,3,
  kutusuna düşmesini sağlarız. Eğer maksimum 1000 kimliği var ise, ve
  N=4 için, kimliklerden 0 ile 250 arası 1'inci kutuya, 251 ile 500
  arası 2'inci kutuya vb gibi gitmeli.

- İlk tarama mesela 4 paralel süreç 4 kutu üzerinden 16 tane dosya
  yaratır.  Dikkat: her kutu için, mesela kutu=1, dort tane paralel
  süreç verinin tamamında 1'inci kutuya düşen verileri bulup çıkartır.

- Ardından paralel olarak yine her kutu için, o kutuya ait olan tüm
  parçaları alırız, hafızada birleştiriz, hafızada sıralarız, ve o
  kutu için diske yazarız.

- Bu bitince sıralanmış tüm kutuların sıralanış dosyalarını alt alta
  ekleriz / yapıştırırız (basit Unix `cat` ile), ve sıralanmış nihai
  dosya elde edilir.

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

1 milyon satırlık bir veri oldu.

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

Şimdi ilk paralel kod, her kutuya düşen satırları paralel olarak bul, kendi
dosyasına yaz.


```python
import os, numpy as np, util

class BucketJob:
    def __init__(self,B,ci):
        self.B = B
        self.ci = ci
        self.bins = np.array([0, 50000, 80000, 130000, 474391])
        print (self.B,self.ci)
        self.fout = open("/tmp/B-%d-%d.csv" % (self.B,self.ci), "w")
    def bucket(self, id): # id hangi kutuya ait?
        return np.argmax(self.bins > id)-1        
    def exec(self,line):
        toks = line.strip().split(',')
        if self.bucket(float(toks[0])) == self.B:
           self.fout.write(line)
    def post(self):
        # diske yaz
        self.fout.close()

# altta seri islem var ama her kutu icin 4 paralel surec baslatilabilir
for B in range(4):
    util.process(file_name='/home/burak/Downloads/input.csv', N=4, hookobj = BucketJob(B,0))
    util.process(file_name='/home/burak/Downloads/input.csv', N=4, hookobj = BucketJob(B,1))
    util.process(file_name='/home/burak/Downloads/input.csv', N=4, hookobj = BucketJob(B,2))
    util.process(file_name='/home/burak/Downloads/input.csv', N=4, hookobj = BucketJob(B,3))        
```

Şimdi her kutu için parçaları hafızaya getir, Pandas üzerinden hafızada sırala,

```python
import pandas as pd, glob
import os, numpy as np, util

# seri islem gosterdik yine fakat her kutu icin paralel bir islem yaratilabilir
for B in range(4):
    dfs = [pd.read_csv('/tmp/B-%d-%d.csv' % (B,i),header=None) for i in range(4)]
    df = pd.concat(dfs,axis=0)
    df = df.sort_values(by=0)
    df.to_csv("/tmp/B-%d-sorted.csv" % B, header=None,index=None)
```

Ve nihai olarak tum kutu parcalarini birlestir,

```
! cat /tmp/B-*-sorted.csv > /tmp/B-final.csv
```

Kutu parçalarını basit alt alta yapıştırma ile birleştirmek işliyor
çünkü her kutu içindeki kimlikler belli bir kutuya gitmiş durumda,
mesela id=1000 kimliği B=0 içinde, id=72000 kimliği ikinci kutu içinde,
ve eğer her kutunun dosyası kendi içinde sıralanmış ise, yapıştırılmış
yeni dosyanin kendiliğinden sıralanmış hale geleceği garantidir.

Tek problem olabilecek su'dur; her kutu icin ustteki ornekte dort tane
parcayi hafizaya getirdik, ve orada siraladik. Ya bu siralama icin
hafiza yeterli olmazsa?

Bu durumda az hafıza ile diskteki dosyaları satır satır birleştirmenin
bir yolu alttadır.

Yöntem 2

Bu yöntem bize daha az hafıza ile daha büyük dosyaları tek makinada
sıralama şansı veriyor. Paralellik hala var, fakat son birleştirme
aşaması her ne kadar disk yoğunluklu olsa da tek bir makinada
yapılmalı. 

2'inci yöntem ile dosyanın ufak parçalarını yine hafızada sıralarız,
diske yazarız, sonra bir süreç o parçaları disk bazlı (satır satır)
okuyarak birleştirir. Sıralanmış parçaların birleşmiş ve hala sıralı
halde olmasını nasıl garantileriz? Bir algoritma,

* Her iki parçanın başına git

* Bir döngü içinde her ikisinin sıradaki en küçük parçasına bak (zaten
  sıralanmış dosyalar için bu en üstteki satır)

* Bu iki öğe arasından en ufak olanını al, yeni listeye ekle, tekrarla

Listeler farklı boylarda olabilir, bir liste öncekinden önce biterse
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

Disk bazlı kod üstteki mantığı dosya satırları için yapar, her iki
dosya açılır, satırlar bu dosyalardan teker teker alınır, döngü içinde
kimlikleri birbiri ile karşılaştırır, hangi dosyadan gelen kimlik daha
küçük ise onun satırı, o dönüşte, çıktıya yazılır, o dosya üzerinde
`readline` çağırılır böylece bir sonraki satıra geçilir. Dosyalardan
biri bitene kadar bu devam eder, sonra kalan dosyanın satırları direk
çıktıya yazılır.

### Kümeleme (KMeans)

Daha önce [1] yazısında bu işi eşle/indirge, Hadoop ortamında nasıl
yapacağımızı gördük. Eğer [2]'deki yöntemi kullanmak istiyorsak, yani
altyapı bir veriyi herhangi bir kritere göre (çoğunlukla basit bloklar
üzerinden) bölmek ve her bölüm üzerinde ayrı bir süreç işletmek
istiyorsak (indirgeme mimarisi kullanmadan), paralel KMeans
algoritması şöyle kodlanabilir. [2]'de bahsettiğimiz gibi takip
ettiğimiz yaklaşım hiçbir şey paylaşma (share nothing)
yaklaşımı. Süreç işe başladığında kendi veri parçasını bilir, ve diğer
süreçlerle iletişimde bulunmaz.

Fakat unutmayalım, KMeans özyineli (recursive) bir algoritmadir,
verinin üzerinden tek bir geçiş (single pass) yeterli değildir. Veri
birkaç kere baştan sonra taranmalıdır.

Bir algoritma şöyle olabilir;

- Her geçişte, döngüde, verinin başına gidilir, ve küme merkezlerinin
  en son ne olduğu `centers.txt` dosyasından tüm süreçler tarafından
  okunur (başta rasgele olabilir). Bu çok ufak bir veridir, anında
  okunabilir.

- Her süreç elindeki verinin her noktasının hangi merkeze yakın
  olduğunu saptar.

- Ardından başa dönülür, biraz önce yapılan üyelik atamasına göre yeni
  küme merkezleri hesaplanır. Bu yeni merkezler `C-0-0`, `C-0-1` gibi
  bir dosyaya yazılır, ki `C-0-1` 0'inci kümenin 1'inci süreç
  tarafından hesaplanmış merkezidir.

- Bu merkezler tabii ki tamamlanmış değildir, bir süreçten gelen
  hesaplardır bunlar, ana takip edici script tüm süreçlerin o
  geçişteki işi bitince, her küme için yarım hesaplanmış merkezleri
  alır, ortalamasını hesaplayıp yeni `centers.txt` dosyasını oluşturur.

- Üstteki adımlar tekrarlanır, ta ki belli bir geçiş sayısı ya da
  "stabiliteye erişim" durumu oluncaya kadar, stabilite derken mesela
  eğer küme merkezlerinde her geçiş sonrası artık büyük değişimler
  olmuyor ise, iş bitmiş kabul edilebilir.

![](kmeans.gif)

Önemli noktaları vurgulayalım, veri satırsal şekilde paylaştırılır,
her sürecin işlediği parçada her kümeden değer olabilir. Her geçişte
işlem paralel olur, fakat bir takip edici script o geçiş bitince bir
sonraki geçişi hazırlamakla sorumludur, her süreçten gelen merkezlerin
ortalaması, bir sonraki geçişin başlatılması bir script'in
sorumluluğundadır. Bu işlemler ağır işlemler değildir bu sebeple seri
işlemelerinde problem yoktur.

Kaynaklar

[1] [Paralel KMeans, Hadoop](2013/10/paralel-kmeans-hadoop.html)

[2] Bayramli, [Paralel, Satır Bazlı Dosya İşlemek](../../2016/02/toptan-islemler-paralelizasyon.html)

[3] Wikipedia, [External Sorting](https://en.wikipedia.org/wiki/External_sorting)

[4] https://en.wikipedia.org/wiki/K-way_merge_algorithm

[5] [Stackoverflow](https://stackoverflow.com/questions/29494594/sorting-data-with-space-contrainsts)


