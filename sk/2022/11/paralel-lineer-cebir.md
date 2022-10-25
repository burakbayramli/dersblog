# Paralel Lineer Cebir

Lineer cebirdeki pek çok işlemi paralel şekilde işletmek mümkün. Altta
bazı örnekler üzerinde göreceğiz. Paralelleştirme yolunda kullanılacak
ana yaklaşım [4]'teki olacak - veri, burada matris verisi, satır satır
işlenecek (her işlem tek bir satırı hafızaya getirecek) ve tüm
satırlar parçalar halinde farklı çekirdeklerde (ya da makinalarda)
paylaştırılacak.

### Matris Çarpımı

Standart matris çarpımını azar azar (incremental) şekilde paralelize
etmek zordur. Bize bir matrisi satır satır işlememizi sağlayacak bir
yaklaşım gerekiyor. [3]'e danışırsak oradaki "satır kombinasyon bakış
açısı" bize uygun gözüküyor, çünkü bu yöntemle A çarpı B deki A'yı
azar azar işlemek mümkündür, her A satırı için bir sonuç satırı
üretilebilecektir. Çarpım yöntemleri [1]'de yazısında da ve
animasyonları ile işlenmiş, bizim istediğimiz alttakidir. Kırmızı
matris A, mavi olan B, sonuç C ise yeşil matris içindedir.

![](carpim1.gif)

A'yi satir satir aldik bu tamam. Fakat B'ye olacak? Ne yazik ki her A
satiri icin B'nin tamami bastan sona gezilmeli. Bundan kacis yok,
zaten matris carpimi O(3) cetrefilligindeki bir operasyondur, standart
kodlama uc tane ic ice dongu icerir, bunun sonucu olarak her satirda
B'nin basa sarilmasi gerekecektir.

Simdi B icin de satir gezme yaklasimi dusunmeden once, problemde bir
basitlestirme yapalim; A, B matrisleri sirasiyla M x D ve D x N
boyutlarinda diyelim, ve farzedelim ki "cok olan" buyukluk M, D
nispeten buyuk ama fazla degil, N ise potansiyel olarak D'den kucuk.

Bu tur verileri mesela Buyuk Veri problemlerine surekli goruyoruz, M
sayisi milyarlarca (satir) olabilir, veri noktalari bunlardir, verinin
degisken boyutu is D, yas, boy, kilo gibi mesela ozellikler (features)
bu degiskenlerde, cok sayida olabilirler ama milyarlarca degil, N ise
daha ufak bir boyut. Ornek uygulama rasgele matris carpimi ile boyut
kucultme olabilir, milyarlarca satir binlerece kolon olabilecek A'yi
bir D x N boyutundaki B ile carpiyoruz, mesela eger N=100 ise carpim
sonucu A x N kolon boyutu azalmis hale geliyor.

Basitleştirme şurada; üstteki türden bir kullanım için B matrisinin
tamamını, her çekirdek için, hafızaya alabiliriz. Eğer B matrisi
milyarlarca satır / kolon içeriyor olsaydı bu olamazdı ama faraziyeye
göre B'nin binlerce satırı ve çok az kolonu olacak. 

B hafızaya alınabilirse artık bazı `numpy` özelliklerinden
faydalabiliriz. Mesela, anımasyonda da görüyoruz, bir A satırının her
hücresi gezilirken oradaki değer alinip bir B satırı ile
çarpılıyordu. Bu çarpımı işlenen tüm A satırı ve tüm B matrisi için
bir kerede yapabiliriz. Alttaki kod örneğine bakalım,

```python
a = np.array([[1,2,3]]).T
B = np.array([[3,4,5],[1,1,1],[2,2,2]])
print (a); print (B)
print (a*B)
```

```text
[[1]
 [2]
 [3]]
[[3 4 5]
 [1 1 1]
 [2 2 2]]
[[3 4 5]
 [2 2 2]
 [6 6 6]]
```

Dikkat `*` kullanildi, `numpy.dot` degil.

Şimdi örnek veriyi üretelim. Bunlar rasgele matrisler olacak. 

```python
M = 1*1000*1000; D = 100; N = 30
A = np.random.rand(M,D)*10
np.savetxt('/tmp/A.csv', A, delimiter=';',fmt='%1.6f')
B = np.random.rand(D,N)*10
np.savetxt('/tmp/B.csv', B, delimiter=';',fmt='%1.6f')
```

Pür `numpy` ile A çarpı B işlemini yapalım, bu işlem hafızada olacaktır.

```python
from datetime import timedelta
from timeit import default_timer as timer

start = timer()
A = np.loadtxt("/tmp/A.csv",delimiter=';')
B = np.loadtxt("/tmp/B.csv",delimiter=';')
C = np.dot(A,B)
np.savetxt('/tmp/C2.csv', C, delimiter=';',fmt='%1.6f')
end = timer()
print('elapsed time', timedelta(seconds=end-start))
```

```
elapsed time 0:01:24.053847
```

Bir milyon satır ve 100 kolonun 100 satır ve 30 kolon içeren B ile
çarpılması 1 dakika 24 saniye aldı.

Aynı işlemi paralel, ve satır satır yaklaşımı ile yapalım, alttaki kod
[4]'teki altyapıyı kullanmıştır,

```python
from multiprocessing import Process
from timeit import default_timer as timer
from datetime import timedelta
import os, numpy as np

def process(afile,bfile,ci,N,obj,skip_lines=0):
    file_size = os.path.getsize(afile)
    obj.afile = afile
    obj.B = np.loadtxt(bfile,delimiter=';')
    obj.ci = ci
    cname = "%s/C-%d.csv" % (os.path.dirname(afile), ci)
    obj.outfile = open(cname, "w")
    
    with open(afile, 'r') as f:
        for j in range(skip_lines): f.readline()
        beg = f.tell()
        f.close()
    chunks = []
    for i in range(N):
        with open(afile, 'r') as f:
            s = int((file_size / N)*(i+1))
            f.seek(s)
            f.readline()
            end_chunk = f.tell()-1
            chunks.append([beg,end_chunk])
            f.close()
        beg = end_chunk+1
    c = chunks[ci]
    with open(afile, 'r') as f:
        f.seek(c[0])
        while True:
            line = f.readline()
            obj.exec(line) # process the line
            if f.tell() > c[1]: break
        f.close()
        obj.post()

class MultJob:
    def __init__(self):
        self.afile = "" # proccessor sets it
        self.B = "" # proccessor sets it
        self.ci = -1 # proccessor sets it
        self.outfile = None # proccessor sets it
    def exec(self,line):        
        vec = np.array([np.float(x) for x in line.strip().split(";")])
        vec = np.reshape(vec, (len(vec),1))
        res = (vec * self.B).sum(axis=0).tolist()  
        res = ";".join(map(str, res))
        self.outfile.write(res)
        self.outfile.write("\n")
        self.outfile.flush()
    def post(self):
        self.outfile.close()
        
dir = '/tmp'
afile = dir + "/" + "A.csv"
bfile = dir + "/" + "B.csv"

start = timer()
   
N = 4 # kac paralel islem var
ps = [Process(target=process,args=(afile, bfile, i, N, MultJob())) for i in range(N)]
for p in ps: p.start()
for p in ps: p.join()
end = timer()
print('elapsed time', timedelta(seconds=end-start))    
```

```
elapsed time 0:00:55.157166
```

```python
cat /tmp/C-*.csv > /tmp/C3.csv
```

Bizim yaklaşım daha hızlı işledi. Acaba sonuçlar birbirine yakın mı?

```python
dir = "/tmp"
C2 = np.loadtxt(dir + "/C2.csv",delimiter=';')
print (C2.shape)
C3 = np.loadtxt(dir + "/C3.csv",delimiter=';')
print (C3.shape)

mdiff = C2.mean()-C3.mean()
sdiff = C2.sum()-C3.sum()
print (mdiff, sdiff)
```

```
(1000000, 30)
(1000000, 30)
6.320988177321851e-11 0.00189208984375
```

Oldukça yakın. Farklılıklar ufak yuvarlama farklılıkları, ya da
verinin her iki yöntem için de okunup yazılırkenki kaybedilebilecek
noktadan sonraki bazı değerleri sebebiyle olabilir.

Çarpım `numpy` ile yapılırken çekirdekleri gözledik, tüm çekirdekler
kullanılıyordu, kullanıcı yorumlarına bakılırsa bazı Python ve `numpy`
versiyonlarında paralellik vardır. Demek ki bizim eşzamanlı kodlama
`numpy` kodlamasını geçti. 

Fakat bir diğer önemli ilerleme şuradadır; Eğer A satır sayısını bir
milyondan iki milyona çıkartacak olsak pür hafıza kullanan yaklaşımlar
kullanılmaz hale gelir çünkü artık A matrisi tamamen bellege sigmaz.
Bu durumda azar azar alıp işleyen üstteki yaklaşım banamısın demez,
çünkü A büyüklüğü ne olursa olsun her seferinde onun sadece tek
satırını işliyoruz, eh zaten B'yi bellege sığar kabul ettik, o zaman
veri ne kadar büyürse büyüsün bizim işlem yapmamız mümkündür. İşte
Büyük Veri bu tür yaklaşımlar sayesinde başedilebilir hale gelmiştir.





Kaynaklar

[1] https://www.adityaagrawal.net/blog/architecture/matrix_multiplication

[2] https://www.geeksforgeeks.org/strassens-matrix-multiplication/

[3] https://burakbayramli.github.io/dersblog/linear/linear_01/ders_1.html

[4] [Paralel, Satır Bazlı Dosya İşlemek](../../2016/02/toptan-islemler-paralelizasyon.html)

