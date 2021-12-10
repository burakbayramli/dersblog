# Python Liste Kavraması (List Comprehension)

Python'un en geç anlaşılan, öğrenilen özelliklerinden biri belki de
budur. Kitap yazarlarının bile hala eski usül liste oluşturmayı
kullanması bunun işareti. Eski usül nasıldır? Mesela 1 ila 10
arasındaki sayıların karesini alacağım, ve bununla yeni bir liste
oluşturacağım. Ana liste,

```python
data = list(range(1,11))
print (data)
```

```text
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

```python
kareler = []
for x in range(1,11):
   kareler.append(x**2)
print (kareler)
```

```text
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

Bir boş liste tanımlandı, ona ekler yapıldı, bir `for` döngüsü var,
vs. Fakat liste oluşturması liste kavrama ile tek bir satırda
yapılabilirdi,

```python
kareler = [x**2 for x in range(1,11)]
print (kareler)
```

```text
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

Yani liste içeriğinin nasıl oluşturulacağını bir nevi liste tanımının
parçası haline getirmiş oluyoruz. 

Kavrama operasyonları çok daha kapsamlı olabiliyor, `if`, `else`,
kullanmak mümkün mesela, hatta içiçe (nested) döngüler bile
kullanılabiliyor.

Sadece çift sayıların karesini alalım, diğerleri olduğu gibi kalsın,

```python
kareler2 = [x**2 if x%2==0 else x for x in range(1,11)]
print (kareler2)
```

```text
[1, 4, 3, 16, 5, 36, 7, 64, 9, 100]
```

Liste kavrama ifadeleri biraz dil sözdizimini tersine çeviriyor sanki,
mesela `for` döngü içine gidecek olan `if` ifadesi şimdi en başta.

İçiçe döngü örneği; 100 ila 105 arasındaki sayılar dış döngü, 1 ile 3
arasındakiler iç döngü olsun, ve içteki listeyi gezerken dıştakine
ekleyelim. Eski usulle bunu

```python
toplamlar = []
for x in range(100,106):
   for y in range(1,4):
      toplamlar.append(x+y)
print (toplamlar)      
```

```text
[101, 102, 103, 102, 103, 104, 103, 104, 105, 104, 105, 106, 105, 106, 107, 106, 107, 108]
```

diye yapardık. Uzun iş.. Her şeyi tek satırda yapabilirdik,

```python
toplamlar = [x+y for x in range(100,106) for y in range(1,4)]
print (toplamlar)
```

```text
[101, 102, 103, 102, 103, 104, 103, 104, 105, 104, 105, 106, 105, 106, 107, 106, 107, 108]
```

Bu temel ile pek çok yöne gidilebilir. Unutmayalım, `enumerate` ile herhangi
bir liste gezimi sırasında üzerinde olunan indis üretilebilir,

```python
for i,x in enumerate(['ali','veli','ahmet']):
   print (i,x)
```

```text
0 ali
1 veli
2 ahmet
```

Ve bu tür bir kullanım liste kavraması için de aynen geçerlidir,

```python
isimler_indisler = [(i,x) for i,x in enumerate(['ali','veli','ahmet'])]
print (isimler_indisler)
```

```text
[(0, 'ali'), (1, 'veli'), (2, 'ahmet')]
```

Böylece bir değişken grubu (tuple) listesi oluşturduk, ve tüm bunları
tek bir satırda yaptık.

Şimdi sıkı durun, değişken grubu listesini Python sözlüğü (dictionary)
haline getirmek mümkündür, bunu da tek satırda yapabilirdik,

```python
isimler_indis_dict = { i:x for i,x in enumerate(['ali','veli','ahmet']) }
print (isimler_indis_dict)
```

```text
{0: 'ali', 1: 'veli', 2: 'ahmet'}
```

Aslında bu kullanıma sözlük kavraması (dictionary comprehension)
deniyor, her neyse, benzer kullanım alanı.
