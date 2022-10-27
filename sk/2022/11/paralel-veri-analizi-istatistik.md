# Paralel Veri Analizi Istatistik

Sıralama (Sorting)

```python
import numpy as np, random

def chunkmerge():
    N1 = 500; N2 = N1*2
    arr1 = [random.randint(0,100) for i in range(N1)]
    arr2 = [random.randint(0,100) for i in range(N2)]
    arr1 = sorted(arr1)
    arr2 = sorted(arr2)

    N = np.max((len(arr1),len(arr2)))
    res = []
    i=0;j=0
    while i<N1 and j<N2:
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

    arrsorted = sorted(arr1 + arr2)
    print (arrsorted == res)

chunkmerge()   
```

```text
True
```







Kümeleme (KMeans)

Daha önce [1] yazısında bu işi eşle/indirge, Hadoop ortamında nasıl
yapacağımızı gördük. Eğer [2]'deki yöntemi kullanmak istiyorsak, yani
altyapı bir veriyi herhangi bir kritere göre (çoğunlukla basit bloklar
üzerinden) bölmemizi sağlıyor ve her bölüm üzerinde ayrı bir süreç
işliyor, o zaman bazı kavramlarda birkaç değişiklik gerekir. 

Kaynaklar

[1] [Paralel KMeans, Hadoop](2013/10/paralel-kmeans-hadoop.html)

[2] Bayramli, [Paralel, Satır Bazlı Dosya İşlemek](../../2016/02/toptan-islemler-paralelizasyon.html)


