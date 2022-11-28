# NoSQL

Basit dağıtık çalışabilen bir NoSQL taban tasarımı şöyle olabilir.

- Yükü karşılıyabilmek için ayrı servisler başlatılır. N tane servis
  için her anahtar üzerinden i = mod N işletilir, ve o veri için i
  servisine gidilir. Böylece veri bazlı yük dengesi yapılmış olur. 
  
- Her servis ayrı bir Flask süreci işletilir, onun get, set arayüzüne
  REST APİ üzerinden erişilir.
  
- Arka planda Flask paralel değil seri halde çalışır, ve kendi sqlite
  tabanına yazar ve okur, böylece her servisin kendi içindeki çakışma
  problemleri ile uğraşmaya gerek kalmaz.
  
- Bir anahtara tekabül eden herhangi bir obje, ne olursa olsun, yazılıp
  okunabilir, çünkü objeler `pickle` üzerinden string halne getirilirler.

```python
import pickle
a = list(range(10))
a = base64.encodestring(pickle.dumps(a))
print ('kodlama',a)
b = pickle.loads(base64.decodestring(a))
print (b)
```

```text
kodlama b'gANdcQAoSwBLAUsCSwNLBEsFSwZLB0sISwllLg==\n'
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

Üstteki örnekte kodlama metni tabana yazılacaktır.

- Listeleri halletmek kolay; liste ismi, mesela `liste2`, ya da
`müşteriler` gibi, sqlite tabanında ayrı bir kolon olarak yazılır,
sonra bu tekrar eden liste ismine sahip tüm satırlar alinip liste
halinde döndürülebilir.



Kaynaklar

[1] [Obje String Olarak Kodlamak](../../2010/10/encoding-objeleri-yazip-okumak-pickle-base64.html)