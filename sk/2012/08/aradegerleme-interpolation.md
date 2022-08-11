# Aradeğerleme (Interpolation)

### RBF



### Matriste Boş Değerleri Yakın Değerle Doldurmak 

Eğer içinde nan yani "tanımsız" ve "boş" değerler olan bir vektörümüz
var ise, bu tanımsız değerlerin yerine, yine aynı vektörde, ve o boş
değerin iki yanindaki değere yakın olan bir değerle doldurmak
isteyebiliriz.

Mesela vektor

```
1, nan, nan, 2, 2, nan, 0

olsun, ve nan diyen yerlerde 1 ve 2 arası, sonraki nan yerine 2 ve 0
arası değerler olmalı.

```
data = np.array([1, nan, nan, 2, 2, nan, 0])
print databad_indexes = np.isnan(data)
good_indexes = np.logical_not(bad_indexes)
good_data = data[good_indexes]
interpolated = np.interp(bad_indexes.nonzero()[0], good_indexes.nonzero()[0], good_data)
data[bad_indexes] = interpolated
print data
```

Sonuc

```
[ 1.
          1.33333333  1.66666667  2.
     2.
     1.
        0.
    ]
```

Peki işlemi bir matris üzerinde, ve her kolon için ayrı ayrı yapmak
istersek?

```
def pad(data):
    bad_indexes = np.isnan(data)
    good_indexes = np.logical_not(bad_indexes)
    good_data = data[good_indexes]
    interpolated = np.interp(bad_indexes.nonzero()[0], good_indexes.nonzero()[0], good_data)
    data[bad_indexes] = interpolated
    return dataA = np.array([[1, 20, 300],
              [nan, nan, nan],
              [3, 40, 500]])
A = np.apply_along_axis(pad, 0, A)
```

Sonuc

```
[[   1.   20.  300.]
 [   2.   30.  400.]
 [   3.   40.  500.]]
```

