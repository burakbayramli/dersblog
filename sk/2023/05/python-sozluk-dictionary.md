# Python Sözlük (Dictionary) Veri Yapısı

Python sözlük yapısı hafızada anahtar bazlı veriye direk erişim
sağlar.  Basit anahtar - değer ikilisini depolamaya yarar, fakat değer
olarak depolanan şey herhangi bir obje olabilir. Bu özellik sözlüklere
geniş kullanım alanı sağlar.

En basit kullanım,

```python
# bos sozluk yarat
dict1 = {}

# depola
dict1['anahtar1'] = "deger1"

# erisim yap
dict1['anahtar1']
```

```text
Out[1]: 'deger1'
```

Herhangi bir obje depolanır demiştik,

```python
dict1['anahtar2'] = np.array([1,2,3])
dict1['anahtar2']
```

```text
Out[1]: array([1, 2, 3])
```

Tüm anahtarları göstermek için

```python
dict1.keys()
```

```text
Out[1]: dict_keys(['anahtar1', 'anahtar2'])
```

Bu liste gezilebilir, ve bu sırada anahtar kullanılıp değer ekrana basılabilir,

```python
for k in dict1: print (dict1[k])
```

```text
deger1
[1 2 3]
```

Kavrama (comprehension) yani [1] tek satirda hem baska bir listeyi gezip ayni
anda baska bir liste / sozluk yaratma kabiliyeti sozlukler icin de gecerli,

```python
dict2 = { i:x for i,x in enumerate(['ali','veli','ahmet']) }
print (dict2)
```

```text
{0: 'ali', 1: 'veli', 2: 'ahmet'}
```

`i:x` ile anahtar/değer ikilisini başka bir listeyi gezerken tanımladık, ve
bu tanımlar toparlanıp bir yeni sözlük yaratımı için kullanıldı.








### DiskDict



Kaynaklar

[1] [Python Liste Kavraması (List Comprehension)](../../2021/12/python-list-comprehension.html)

[2] [NoSQL](../../2022/11/nosql-diy-python.html)

