# Python Paketleme

Python paketleme sistemiyle kaynak kodumuzu paketleyerek ona `pip
ınstall` ya da `setup.py install` sonrası herhangi bir dış dizin ya da
yeni bilgisayardan `import` ile erisebilmemiz sağlanır. Paketler
global kurulabilir ama çoğunlukla `virtualenv` benzeri sanal
geliştirme ortamı içinde kurulurlar.

Kurulum için bir `setup.py` gerekir. Mesela `modul1` adında paylaşmak
istediğimiz bir kod var, kodlar `/home/vs/dizin/modul1` altında, bu
dizinde en üst seviyede bir `setup.py` koyarız, 

```
from setuptools import setup

setup(name='modul1',
      version='0.1',
      description='Modul 1 cok onemli seyler yapar',
      url='https://github.com/user/modul1',
      author='Burak Bayramli',
      author_email='dd@post.com',
      license='MIT',
      packages=['modul1'],
      install_requires=[
          'dateutil',
      ],
      zip_safe=False)
```

olabilir. 

Not: Paketleme servisinin isimleme yöntemi sebebiyle kodlarımızın
`modul1` altında bir `modul1` alt dizini içinde olması lazım.

Bu altdizin içinde mutlaka bir `__init__.py` dosyası gerekli, içinde
en basit kullanım için

```python
from .modul1 import *
```

olmalı. Bu sayede `import modul1` deyince `__init__.py` yükleniyor,
yüklenen bu dosya da diğer kod dosyalarımızı yükleyip kullanıma
açıyor. Böylece mesela `modul1/modul1` altında `source.py` diye bir
dosya varsa, onun içinde de `def callme()` gibi bir fonksiyon varsa,
üstteki tanım sayesinde `modul1.callme()` çağrısı artık yapılabilir.

Artık en üst dizinde iken `python setup.py install` ile
kurulum yapabiliriz.

`install_requires` seçeneğine verilen liste install sırasında `pip` ile
otomatik kurulacak ek programların listesidir. Üstteki örnekte
`dateutil` adlı dış Python paketi kurulacaktır.

Eğer `setup.py develop` dersek belli bazı sembolik bağlantılar
sayesinde `modul1` geliştirme dizininde yaptığımız değişiklikler direk
kurulu kütüphane üzerinde etki yaratır. Bu geliştirme (develop) için
çok faydalı.

Eğer global ortamdaysak `install`` çağrısı global, sanal ortamda isek
sanal ortama kurulum yapar. Sanal ortam hakkındaki virtualenv yaziları
[2, 3].

Eğer paket içine veri dosyaları da eklemek istiyorsak, `setup.py` içinde

```
    include_package_data=True,
    package_data={
        "": ["*.zip","*.csv"]
    },
```

eki yapabiliriz. Bu durumda `modul1/modul1` altındaki tüm belirtilen
sonekli dosyalar toparlanıp pakete dahil edilecektir. `setup.py install`
sonrası, mesela benim `/home/burak/Documents/env3` sanal geliştirme
ortamım için kurulum

```
/home/burak/Documents/env3/lib/python3.6/site-packages/modul1-0.1--py3.6.egg
```

dizini altına gitti, oraya baktım, veri dosyaları oraya koyulmuştu. 

Tabii dikkat, bir sorun daha var, paketlenen veriye kod nasıl
erişecek? Bir çözüm işleyen kod dosyasının adresinin kod içinde,

```
data_dir = os.path.dirname(__file__)
```

ile alınması, ve kod içinde tüm veri erişimlerini `data_dir +
"/veri.zip"` olarak değiştirmek. Kod `__file__` anda içinde olunan
dosyanın tüm adresidir, onun baz dizinini alıp veri dosya erişimini
ona göre ayarlıyoruz.

Pip Hazırlığı

Bildiğimiz gibi Python dosyalarının `pip` komutu ile kurulabilmesini
sağlayan bir altyapı var. Bu yapı

https://pypi.org/

adresinde, kodumuzu herkesin kullanımına açmak için oraya da gönderebiliriz.
[1] adresinde daha fazla detay var, fakat eğer `setup.py` kurulumu tam yapılmışsa,
`python setup.py sdist bdist_wheel` ile PyPi için gerekli dosyaları da üretmek
mümkün, bu dosyalar `dist` dizini altında konuluyor.

Nihai paketin PyPi'a gönderilmesi için PyPi'a üye olunması lazım, ve  `twine` adlı
araç gerekli, onu

```
sudo apt install twine
```

ile kurabiliriz.

Kaynaklar

[1] https://realpython.com/pypi-publish-python-package/#preparing-your-package-for-publication

[2] [Yazi](../../2018/08/virtualenv-python-izole-sanal-calsma.md)

[3] http://guide.python-distribute.org/creation.html











