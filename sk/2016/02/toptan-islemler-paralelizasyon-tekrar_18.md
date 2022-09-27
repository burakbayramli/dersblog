# Toptan İşlemler, Paralelizasyon, Tekrar Başlatılabilirlik (Restartability)

### Paralel İşlem

IT veri işlemciliğinde çok karşılaşılan bir problem: çok sayıda bir
grup verinin sırayla işlenmesi. İşlemi paralelize edersek (eldeki her
çekirdek için bir veya daha fazla süreç başlatarak) aynı anda daha
fazla veri işleyebiliriz. Fakat paralelize etmeden önce süreçlerin
birbiriyle kordinasyonunu ayarlamak gerekli.

Bir yaklaşım her paralel süreç işlemek istedikleri kayıtı "kitlemeye"
uğraşabilirler, önce gelen kitler, sonrakiler başarısız olup sonraki
kayıdı kitlemeye uğraşırlar, vs. Bu yaklaşımı Kurumsal Java kitabında
işlemiştik.  Bu tabii daha farklı bir dünyaydı, Oracle, satır bazlı
kilitler, vs. Artık anahtar/değer tabanları dünyasındayız, Mongo ile
bir kaydın anahtar üzerinden statüsünü kontrol etmek çok hızlı. Diğer
yaklaşımın da faydalı olacağı yerler olabilir muhakkak. Faydalardan
biri önceden parça sayısı (bilahere kaç sürecin paralel işleyeceği)
tanımlamaya gerek yok, ihtiyaca göre yeni bir süreç başlatılır, yeni
süreç hemen işlenmemiş kayıt / kitleme mekanizmasına dahil olur,
sıradaki kayıdı alıp işlemeye başlar. Fakat çoğunlukla önceden hangi
makinada kaç süreç işleyeceği hakkında iyi bir fikrimiz vardır, bu
durumda külfetli kitleme işlerine girmeye gerek olmayabilir.

Ama en basit olan her paralel sürecin tamamen ayrı bir veri grubu
üzerinde işlem yapması. Yani elde 100 satır var ise 4 süreç
başlatırız, her süreç 25 satır üzerinde, diğerlerinden tamamen
bağımsız bir şekilde iş yapar.

Bir IT problemi daha: kaç süreçli olursa olsun üstte bahsettiğimiz
işlem bizimle alakalı olmayan bir sebepten dolayı çökebilir. Ardından
programı tekrar başlatırsak programın o ana kadar işlediği satırları
atlayıp, işlenmemiş satırlara gitmesini isteriz, bu "kaldığımız yerden
devam" özelliği zamandan tasarruf sağlar.

Önce 1. probleme bir çözüm bulalım. Bir işleyici script düşünelim,
eğer parçalı işlem mantığını kodlayacaksak, şöyle bir komut satırı
arayuzu düşünebiliriz,

python isle.py 0 4

Bu komut script'e veriyi 4 parçaya böldürüp 0. parçayı (çünkü
kullandığımız dil 0-indis bazlı) işlemeye başlar. Unix ortamında
sonuna & koyarak script'i arka planda işletmeye başlatabilirdik,
ardından

python isle.py 1 4 &

ile hemen bir diğer parça üzerinde de işlem başlatırdık. Dikkat:
parçaya bölmek için "işlenecek şeyler" listesi hazırladık, bu liste
her süreçte aynı, o yüzden bir tarafta 1. bir tarafta 2. vs. parçasına
gidebiliyoruz, çünkü liste aynı liste, ayrı parçalarının birbiriyle
alakasının olmadığına eminiz.

Bu şekilde devam edip 4 tane aynı anda paralel işleyen süreç
başlatarak, veriyi 4 kat daha hızlı işleyebilirdik, tabii bunu derken
işlemi yapan bilgisayarda 4 veya daha fazla mikroişlemci / çekirdek
olduğunu varsayıyoruz. Ama bu yorumu biraz daha genisletelim; eğer
yaptığımız işlemler mikroişlemciyi çok meşgul tutan türden değil ise,
mesela Internet'ten bilgi indirmek (bu durumda network bekleniyor), ya
da sabit disk işlemleri (bu durumda diskin işini bitirmesini
bekleniyor, İngilizce "IO-bound" denen durum) bu durumlarda 4 süreç
için 2 tane mikroişlemci olması bile yeterli olabilir, çünkü daha iyi
performansın önündeki engel mikroişlemci değil. Fakat paralelizasyon
hala faydalı çünkü bir süreç network'u beklerken diğeri verinin kendi
parçası üzerinde ilerleme sağlayabilir.

2. problemin çözümü, mesela işlenecek şeyler bir veri tabanından
geliyorlarsa, tabanda bir status kolonu yaratmak, ve işlenen veri
satırında bu statü belirten kolonu o satır için "işlendi" konumuna
getirmek. Her satır işlenmeden önce bu statüye bakılır, eğer işlenmiş
ise atlanır.

Statü irdelemesi farklı yollardan olabilir; eldeki 10 senet için
kapanış fiyatlarını güncel tutmak isteyen bir program varsa "kaldığı
yerden devam etmek" her senet için eldeki en son tarihten (mesela dün,
iki gün oncesi, vs) o günün tarihine, yani bugüne kadar olan yeni
senet fiyatlarını almaktır. Eğer eksişözlük sitesinden 100 tane sayfa
indirip bu sayfaları HTML olarak bir dizine yazıyorsam, o HTML
dosyasının dizin içinde olup olmaması bir tür statüdür; eğer orada ise
o işlem tamamlanmıştır.

Çöküş ardından tekrar başlatım için pek çok Unix bazlı takip edici programlar var; mesela supervisord - bizim tercihimiz dand. Bu takip edici araçlar sayesinde komut satırından elle biz program başlatmıyoruz, takip edici programlarımızı başlatıyor, onları izliyor,
çökmüs ise tekrar başlatıyor, vs.

Bir örnek olarak bir meteoroloji sitesinden herhangi bir şehir için
hava durumunu indirme programını görelim. Mesela İstanbul için hava
son sıcaklığı alttaki program ile ekrana basabiliriz,

```
import re, requests
from urllib import urlretrieve

url = "http://www.mgm.gov.tr/tahmin/il-ve-ilceler.aspx?m=istanbul"
response = requests.get(url)
response_body = response.content

regex = "sondrm.*?renkMax.*?(\d+).*?C</em>"
res = re.findall(regex, response_body, re.DOTALL)
print res[0]
```

Diyelim ki elimizde bir şehir listesi var. Bu listeyi teker teker
işleyebilirdik. Üstteki programı modülarize ederdik, listedeki her
şehir için bir fonksiyon çağırıp o şehrin verisini alırdık. Fakat
üstte tarif edildiği gibi bu işlemi nasıl paralelize ederdik?

Şöyle

```
import re, os, requests, sys
from urllib import urlretrieve

sehirler = ['bursa','istanbul','afyon','rize','ordu','antalya']
base_dir = '/tmp'

def get_hava(sehir):
    url = "http://www.mgm.gov.tr/tahmin/il-ve-ilceler.aspx?m=%s" % sehir
    response = requests.get(url)
    response_body = response.content
    regex = "sondrm.*?renkMax.*?(\d+).*?C</em>"
    res = re.findall(regex, response_body, re.DOTALL)
    return res

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def process(liste):
    for sehir in liste:
        # bu sehir alinmis, devam et
        f = base_dir + "/" + sehir
        if os.path.isfile(f): continue
        # alinmamis, indir
        hava = get_hava(sehir)[0]
        fout = open(f, "w")
        fout.write(str(hava))
        print sehir, hava
        fout.close()

if __name__ == "__main__":

    nth = int(sys.argv[1])
    n_pieces = int(sys.argv[2])

    # bu takla lazim cunku chunks her parca icindeki
    # oge sayisini baz aliyor
    elems =  int(len(sehirler) / n_pieces)
    liste = list(chunks(sehirler, elems))
    process(liste[nth])
```

Artık

```
python hava.py 0 2
python hava.py 1 2
```

ile şehir listesini 2 parçaya bölüp her iki parçayı ayrı ayrı
işleyebileceğiz. Her şehir için hava durumu /tmp altına yazılır, eğer
o şehir /tmp altında var ise, atlanır. Böylece kaldığımız yerden devam
edebiliriz. Mesela birinci programı işletince,

```
bursa 14
istanbul 11
afyon 19
```

gelir. Şimdi /tmp altına gidip afyon dosyasını silelim, ve tekrar
işletelim. Sadece o şehrin indirildiğini göreceğiz.  Böylelikle
paralelizasyon, çöküşten kurtulma gibi problemlerin hepsini çözmüş
oluyoruz.

Eğer bu iki paralel programı dand takibinde başlatmak isterek, bir
hava.conf dosyası yaratırız, içinde

```
hava0: 
   exec: python hava.py 0 2
   restart: forever
hava1: 
   exec: python hava.py 1 2
   restart: forever
```

ve işletmek için

```
python [DAND DIZINI]/dand.py hava.conf
```

Böylece her programımız ayrı süreçler içinde, paralel olarak işletilecektir.

Loglama

Bir takipçi tarafından, paralel şekilde program işletiliyorsa, artık print ile ekrana mesaj basmak yeterli değil, loglama gerekli, yani bir log dosyasına çıktıları güzel bir format ile yazmak. Python'da logging kütüphanesi bu işi çok rahat yapar; script başında import logging ile dahil ederiz, ve örneğimiz için alttaki kodu ekleriz,

```
fmt = '%(asctime)s - %(message)s - %(pathname)s'
fout = '/tmp/hava-%d.log' % int(sys.argv[1])
logging.basicConfig(filename=fout, level=logging.DEBUG, format=fmt)  
```

Artık logging.debug(...) ile yazılan her mesaj o sürecin kendisine ait
log dosyasına yazılacaktır, mesela 0. parça için bu /tmp/hava-0.log
olacak. Eger mesajlar direk ekrana basilsin istiyorsak filename yerine
stream=sys.stdout kullanabiliriz.

Not:

Örnekte meteoroloji sitesinin tüm HTML'i içinden sadece sıcaklık
verisini çekip çıkarttık; yani bir Web kazıma (scraping) işlemi
yaptık.  Kazıma güzel bir isim, sanki duvardan boya kazıyormuş gibi,
HTML'i kazıyıp içindeki veriyi ortaya çıkartıyoruz. Bu işlem için
düzenli ifadeler (regular expression, regex) kullandık. Tüm yazılım
mühendislerine öğrenmelerini şiddetle tavsiye ettiğimiz bir teknik.

Ne Zaman Thread Ne Zaman Süreç?

Thread aynı süreç içinde paralel işlem yapmak için kullanılabilecek
bir teknolojidir; bir kod parçasını, iş ünitesini bir Thread'e vererek
işletebiliriz. Hava durumu örneğinde her şehir için ayrı bir Thread
başlatıyor olabilirdik.

Bir Thread başlatmak çok basittir, kod içinden tek bir çağrı ile
hallolur. Belli sayıda Thread yaratıp işlemleri bu "havuz" üzerinden
de yaptırabilirdik, yani sayı kısıtlaması da mümkündür.

Bu teknolojinin çok kullanışlı olduğu yerler var, mesela Web
sunucuları içinde servise gelen her istek için bir Thread
yaratılabilir, ya da Telekom şirketlerinde gelen bağlantılar ayrı
Thread'ler üzerinden halledilebilir, vs.  Diğer yandan, Thread'lerin
idaresi, takibi süreçlere göre daha zor; başlatılan bir Thread
dışarıdan durdurulamaz, onları işletim sistemi bazında "dışarıdan"
izleyecek araçlar standart değildir. Kıyasla süreçler Unix'in
belkemiğidir, onları takip etme, durdurma, başlatma bağlamında bir
sürü araç vardır. Thread'ler biraz programlama dilinin kendi
dünyasındadır denebilir, dışarıya açık değillerdir.

Süreçler idare, bakım açısından daha iyi bilinirler, mesela "bir
sürecin çökmesi" durumunda yapılabilecekler bilinir, sürecin geri
döndürdüğü kodlar vardır, "tekrar başlatmak", çıktısını bir dosyaya
yönlendirmek, gibi seçenekler hakkında bir sürü bilgi, tecrübe
mevcuttur. Ve süreçler dilden bağımsızdır. Python, C++, C süreçlerini
istediğimiz Unix aracı ile takip, kontrol edebiliriz.

Python üzerinde Thread'lerin bir negatif durumu şu; Python
yorumlayıcısı süreci tek mikroişlemciye / çekirdeğe bağlıdır; bu
demektir ki süreç içinde yaratılan tüm Thread'ler aynı çekirdekte
işleyecektir. O zaman eğer başka şeyi bekleyen, ona takılıp kalmış kod
yok ise, daha fazla Thread yaratmak bir performans ilerlemesi
sağlamaz. Süreçler ile her sürecin farklı bir çekirdeğe gitme
olasılığı oldukça yüksektir, Unix bu kaynak bölüştürmesini çok doğal
bir şekilde yapar.

Hem süreçler, hem de Thread'ler için ek kodlama gerekir, fakat beni
Thread'ler durumunda hep rahatsız eden şey onların potansiyel olarak
işlemekte olan programın tüm diğer bölümlerine bakabilecek olmaları -
ki bu sebepten dolayıdır ki Thread bazlı hataları ayıklamanın çok saç
baş yoldurucu olduğu hep söylenir; hatayı düzeltmek için onu
tekrarlamak (duplicate) istiyorsunuz mesela ama Thread'lerin kafasına
estiği zaman hata çıkıyor, esmediği zaman çıkmıyor!  Bu mümkün çünkü
Thread'lerin işleme sırası için bir kural yok, eğer bir şekilde, hangi
sırada belli olmadığı şekilde Thread'ler bir noktayı bozmuş ise, bu
durumu tekrar ortaya çıkartmak çok zor olacaktır. Süreçlerin
yaratabileceği hatalar, varsa, gerçekten paylaşılan kaynaklar ile
alakalı olabilir, veri tabanları, mesaj kuyrukları, dosya sistemi,
vs. Fakat bunlar zaten paylaşılan doğal kaynaklardır.

Süreçleri başlatmak daha pahalıdır, Thread'ler çok hızlı bir şekilde
başlatılabilirler. Süreç seçeneğinin negatif tarafını dengeleyen şu
var; toptan işlemler için paralelizasyon yapıyorsak, işin en başında
belli sayıda süreç başlatırız; bu bedeli başta öderiz, ardından iş
bitene kadar o belli sayıda süreci ayakta tutmakla, takip etmekle
haşır neşir oluruz.

<a name='restart'/>

### Tekrar Başlatılabilirlik (Restartability)

Eğer SQL bazlı veri tabanındaki kayıtları işliyorsam en basit yaklaşım
işlenen satırlar üzerinde bir statü kolonu koymak, ve süreç
başladığında 'işlenmemiş satırlar' statüsündeki satırları almak, ve o
satır işlendikten sonra onu 'işlendi' statüsüne getirmek. Bu yaklaşım
daha önce bahsedilen 'satır kitleme' yaklaşımıyla uyumlu, ben işlerken
diğer süreçler bu satırı kitlemeyecek, bir sonraki satıra gidecekler,
ben o sırada işimi yapacağım. İsim bitince statüyü 'işlendi' haline
getireceğim, eh zaten kilit bende, ve bu şekilde elimdeki bir sonraki
satıra bakacağım. Eğer süreci ikinci kez başlatıyorsam ben ya da
benden sonraki süreç statüyü kitler, ve yine işlenmemiş olan satırları
alır, ve işe devam eder.

Peki tek süreçli ve mesela CSV bazlı işlem yapıyorsak yaklaşım ne
olmalı? Mesela `in.csv` içindeki satırları işleyip bir `out.csv`
üreteceğim, bir Web sitesinde sorgulama yapıp yeni bir kolon
ekleyeceğim belki, ve İnternet bağlantısı düşebilir, pek çok şey
olabilir, tekrar başlattığımda kaldığım yerden devam etmek istiyorum.

Burada en kolay yaklaşım şudur, eğer girdi verisinde baştan sonra
doğru artan bir İD, kimlik satırı varsa (ki yoksa biz ekleyebiliriz)
satır satır işlem yaparken önce çıktıdaki en son işlenmiş kimliği
alırız, yoksa sıfır kabul ederiz, ve girdide bu son kimlikten büyük
olan satırları alıp işlem yaparız.

Bu numaranın Python, CSV bazlı işlemesi için kritik hareketler şunlar,
işlenen her satır çıktı mesela `write` yazıldıktan sonra muhakkak
`flush` ile diske yazımı zorlanmalı, ve çıktı dosyası (ilk başlatım
sonrası) her defasında `w` ile değil `a` ile açılmalı. Böylece, ilk
hareketle, süreç patlarsa o yazılan satırı kurtarmus oluruz, ve bir
sonraki işletim ondan sonraki satıra geçebilir, ikinci hareketle çıktı
dosyasına ek yapmış oluruz, önceki sonuçları ezmeyiz.

Örnek üzerinde görelim, standart Pandas bazlı satır satır işlemi kalıbı,

```python
import pandas as pd
df = pd.read_csv('in.csv')
for idx,row in df.iterrows():
    print (row['id'],row['name'],row['value'])
```

```text
1 n1 30
2 n2 10
3 n3 33
4 n4 8
5 nx 39
6 nu 57
7 ne 22
8 na 12
9 nn 31
10 ni 1
11 n18 2
```

Oldukça basmakalıp. Bu tema ile bir script şöyle olabilir,

```python
import numpy as np, time, pandas as pd, sys, os

def ext_proc(x):
    # dis web sitesi baglantisi bu olsun, degil ama
    # yapay kodlarla oymus gibi yapalim
    time.sleep(np.random.rand()) # suni bekleme ekledik
    return x + np.random.rand() # rasgele deger dondur

infile = "in.csv"; outfile = "/tmp/out.csv"

if len(sys.argv)>1 and sys.argv[1] == "init":
    os.remove(outfile)
    fout = open(outfile,"w")
    fout.write("id,name,value,newval\n")
    fout.close()    

dfi = pd.read_csv(infile)
dfo = pd.read_csv(outfile)
if len(dfo) > 0: # ilk baslatimda cikti bos, onu kontrol et
    dfi = dfi[dfi.id > dfo.id.max()]
print (dfi)

fout = open(outfile,"a")
for idx,row in dfi.iterrows():
    newval = ext_proc(row['value'])
    line = "%s,%s,%s,%s\n" % (row['id'],row['name'],row['value'],newval)
    print (line)
    fout.write(line)
    fout.flush()
fout.close()
```

İlk başlatımda `init` seçeneği ile işletiriz, böylece `out.csv` düzgün
şekilde yaratılır. İşlem olurken programı yarıda keselim, sonra `init`
olmadan tekrar başlatalım. Bu başlatımın kalınan yerden devam ettiğini
göreceğiz, yeni işlenen satırlar çıktının sonuna eklenecek.

Dikkat edersek `dfi[dfi.id > dfo.id.max()]` filtresi ile girdi verisinin
çıktı verisindeki en büyük id'den daha büyük olanlarını almış oluyoruz,
böylece o satırlar işlenmiyor, ve çıktıya sürekli ekler yapılıyor.

