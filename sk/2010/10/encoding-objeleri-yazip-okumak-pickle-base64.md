# Kodlama (Encoding), Objeleri Yazip Okumak - Pickle, zlib, base64

Pickle

Python pickle servisi herhangi bir nesneyi alip dosyaya yazabilmek
yetenegine sahip. Bir dictionary objemiz oldugunu dusunelim:

```python
dict = {}
dict['a'] = 33
dict['b'] = 55
```

Bu nesneyi soyle dosyaya yazariz

```python
import pickle
pickle.dump(dict, open('dict.pkl', 'wb'))
```

Geri okumak icin

```python
dict= pickle.load(open("dict.pkl","rb"))
f.close()
```

Dikkat: pickle objeleri kendine özel ikisel bir formatta yazar ve
versiyonlar arası uyumsuzluk problemi çıkabilir.  Paketlerarası
versiyon, ya da Python 2 ve 3 arası uyumsuzluklar görülebilir. Bu
sebeple eğer mümkün ise pickle'ları çok kullanmamak en iyisi.

Numpy Matrisini, Sıkıştırarak  ve String Olarak Yazmak

Bir Numpy matrisi cetrefil bir objedir aslinda. Onu Sıkıştırarak bir
metin haline dondurebilir miyiz? Bu lazim olabilir cunku ikisel
(binary) degil bir dosyada, veri tabaninda rahat depolamak icin metin
formati daha kullanisli olabilir ama hala sıkıştırma gerekmektedir. Bu
durumlarda zlib ve base64 kodlamasi kullanilabilir.

```python
import numpy as np, zlib

a1 = np.eye(3) 
a1[0,1] = 3.4423423423423
# liste yap, onu string yap, sonra kodla
a2 = list(a1.reshape(9))
a3 = str(a2).encode('zlib').encode('base64')

print a1
print a2
print 'kodlama', a3

# geriye cevir
d1 = a3.decode('base64').decode('zlib')
d2 = eval(d1)
d3 = np.array(d2).reshape(3,3)

print d1
print d2
print d3
print d3.shape
```

```
[[1.         3.44234234 0.        ]

 [0.         1.         0.        ]

 [0.         0.         1.        ]]

[1.0, 3.4423423423423, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]

kodlama eJyLNtQz0FEw1jMxMTKGIx0FA5AomDCEs1DEYgE2uQqF

[1.0, 3.4423423423423, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]

[1.0, 3.4423423423423, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]

[[1.         3.44234234 0.        ]

 [0.         1.         0.        ]

 [0.         0.         1.        ]]

(3, 3)
```

String tipinden kodlanmış bir metne, oradan geriye nasıl gidilir görelim,

```python
import base64
s = 'bubirkelime'
print (s)
```

```text
bubirkelime
```

```python
b = bytes(s,'utf-8')
print (type(b))
print (b)
```

```text
<class 'bytes'>
b'bubirkelime'
```

```python
e = base64.encodestring(b)
print (e)
```

```text
b'YnViaXJrZWxpbWU=\n'
```

```python
d = base64.decodestring(e)
print (d)
```

```text
b'bubirkelime'
```

Birkaç farklı metin üzerinde aynı kodlama çağrısı işletilince sonda
hep bir `\n` olduğunu farkedebiliriz.. Bu ek aslında gerekli değil,
onu çıkartsak ta geriye kodlama bize aynı sonucu verecektir. 




